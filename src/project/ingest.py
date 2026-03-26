from pyspark.sql import SparkSession, DataFrame
import os


def ingest(spark: SparkSession, path: str) -> DataFrame:
    """
    Ingest data from:
    - Local path (data/raw/)
    - S3 (s3://...)
    - Fallback to sample data if not found
    """

    print(f"[INGEST] Attempting to read from: {path}")

    # -------------------------
    # Case 1: S3 path
    # -------------------------
    if path.startswith("s3://"):
        print("[INGEST] Detected S3 path")
        return spark.read.option("header", True).csv(path)

    # -------------------------
    # Case 2: Local path exists
    # -------------------------
    if os.path.exists(path):
        print("[INGEST] Found local dataset")
        return spark.read.option("header", True).csv(path)

    # -------------------------
    # Case 3: Fallback sample
    # -------------------------
    sample_path = "data/sample/sample.csv"

    if os.path.exists(sample_path):
        print("[INGEST] Using sample dataset fallback")
        return spark.read.option("header", True).csv(sample_path)

    # -------------------------
    # Fail cleanly
    # -------------------------
    raise FileNotFoundError(
        f"""
        Dataset not found.

        Checked:
        - {path}
        - {sample_path}

        Please download the dataset and place it in data/raw/
        or configure an S3 path.
        """
    )