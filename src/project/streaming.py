from pathlib import Path
import threading
import time
import random
import shutil
import pandas as pd


def prepare_stream_batches(
    source_csv: str,
    batch_dir: str,
    rows_per_file: int = 500,
    overwrite: bool = False
):
    source_path = Path(source_csv)
    batch_path = Path(batch_dir)

    batch_path.mkdir(parents=True, exist_ok=True)

    if overwrite:
        for f in batch_path.glob("*"):
            f.unlink()

    existing = list(batch_path.glob("*.csv"))
    if existing and not overwrite:
        print("Batches already exist. Skipping creation.")
        return

    print("Creating batch files...")

    for i, chunk in enumerate(pd.read_csv(source_path, chunksize=rows_per_file), start=1):
        out_file = batch_path / f"batch_{i:04d}.csv"
        chunk.to_csv(out_file, index=False)

    print("Batch creation complete.")


def run_stream_producer(
    batch_dir: str,
    streaming_dir: str,
    timeout_seconds: int = 1800,
    min_delay: int = 1,
    max_delay: int = 6,
    min_files_per_push: int = 1,
    max_files_per_push: int = 10,
    loop_batches: bool = True,
    stop_event: threading.Event | None = None,
    clear_streaming_dir: bool = False,
):
    """
    Simulate a streaming producer by copying CSV batch files into the streaming input folder.

    Parameters
    ----------
    batch_dir : str
        Directory containing pre-split batch CSV files.
    streaming_dir : str
        Directory watched by Spark Structured Streaming.
    timeout_seconds : int
        Maximum runtime before producer stops automatically.
    min_delay, max_delay : int
        Random delay range (seconds) between pushes.
    min_files_per_push, max_files_per_push : int
        Random number of files copied per push.
    loop_batches : bool
        If True, restart at the first batch after reaching the end.
    stop_event : threading.Event | None
        Optional event used to stop the producer early.
    clear_streaming_dir : bool
        If True, clears the streaming directory before starting.
        Usually False if reset is already handled elsewhere.
    """
    batch_path = Path(batch_dir)
    stream_path = Path(streaming_dir)

    if not batch_path.exists():
        raise FileNotFoundError(f"Batch directory not found: {batch_path}")

    stream_path.mkdir(parents=True, exist_ok=True)

    if clear_streaming_dir:
        for f in stream_path.glob("*"):
            if f.is_file():
                f.unlink()

    batch_files = sorted(batch_path.glob("*.csv"))
    total = len(batch_files)

    if total == 0:
        raise FileNotFoundError(f"No CSV batch files found in: {batch_path}")

    start_time = time.time()
    i = 0
    emitted = 0

    print("Starting stream producer...")

    while True:
        if stop_event is not None and stop_event.is_set():
            print("Stop signal received. Producer stopping.")
            break

        if time.time() - start_time >= timeout_seconds:
            print("Timeout reached. Stopping.")
            break

        delay = random.randint(min_delay, max_delay)
        num_files = random.randint(min_files_per_push, max_files_per_push)

        end = min(i + num_files, total)
        files = batch_files[i:end]
        i = end

        if not files:
            if loop_batches:
                i = 0
                continue
            print("No more batch files to send. Producer stopping.")
            break

        for f in files:
            if stop_event is not None and stop_event.is_set():
                print("Stop signal received during file copy. Producer stopping.")
                return

            emitted += 1
            dst = stream_path / f"stream_{emitted:05d}.csv"
            shutil.copy2(f, dst)

        print(f"Sent {len(files)} files | Total: {emitted}")

        if i >= total:
            if loop_batches:
                i = 0
            else:
                print("All batch files sent. Producer stopping.")
                break

        # Sleep in small increments so stop_event can interrupt quickly
        slept = 0
        while slept < delay:
            if stop_event is not None and stop_event.is_set():
                print("Stop signal received during delay. Producer stopping.")
                return
            time.sleep(1)
            slept += 1