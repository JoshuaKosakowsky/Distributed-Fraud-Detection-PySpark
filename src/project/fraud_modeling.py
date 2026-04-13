from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def split_by_label(train_df: DataFrame, label_col: str = "is_fraud"):
    """
    Split a training dataframe into fraud and non-fraud subsets.
    """
    fraud_df = train_df.filter(F.col(label_col) == 1)
    nonfraud_df = train_df.filter(F.col(label_col) == 0)
    return fraud_df, nonfraud_df


def undersample_training(
    fraud_train_df: DataFrame,
    nonfraud_train_df: DataFrame,
    label_col: str = "is_fraud",
    seed: int = 5420
) -> DataFrame:
    """
    Undersample majority class to approximately match the minority class.
    """
    fraud_count = fraud_train_df.count()
    nonfraud_count = nonfraud_train_df.count()

    if nonfraud_count == 0:
        raise ValueError("Non-fraud training set is empty.")

    under_fraction = fraud_count / nonfraud_count

    sampled_nonfraud = nonfraud_train_df.sample(
        withReplacement=False,
        fraction=float(under_fraction),
        seed=seed
    )

    return fraud_train_df.union(sampled_nonfraud).orderBy(F.rand(seed=seed))


def oversample_training(
    fraud_train_df: DataFrame,
    nonfraud_train_df: DataFrame,
    label_col: str = "is_fraud",
    seed: int = 5420
) -> DataFrame:
    """
    Oversample minority class with replacement to approximately match the majority class.
    """
    fraud_count = fraud_train_df.count()
    nonfraud_count = nonfraud_train_df.count()

    if fraud_count == 0:
        raise ValueError("Fraud training set is empty.")

    over_ratio = nonfraud_count / fraud_count

    sampled_fraud = fraud_train_df.sample(
        withReplacement=True,
        fraction=float(over_ratio),
        seed=seed
    )

    return nonfraud_train_df.union(sampled_fraud).orderBy(F.rand(seed=seed))


def hybrid_sample_training(
    fraud_train_df: DataFrame,
    nonfraud_train_df: DataFrame,
    fraud_multiplier: float = 5.0,
    seed: int = 5420
) -> DataFrame:
    """
    Hybrid sampling:
    - oversample fraud to a target size
    - undersample non-fraud to match that target
    """
    fraud_count = fraud_train_df.count()

    target_fraud_count = int(fraud_count * fraud_multiplier)

    hybrid_fraud = (
        fraud_train_df.sample(
            withReplacement=True,
            fraction=float(fraud_multiplier),
            seed=seed
        )
        .limit(target_fraud_count)
    )

    hybrid_nonfraud = (
        nonfraud_train_df
        .orderBy(F.rand(seed=seed))
        .limit(target_fraud_count)
    )

    return hybrid_fraud.union(hybrid_nonfraud).orderBy(F.rand(seed=seed))


def fit_and_score_model(model_pipeline, train_df: DataFrame, test_df: DataFrame) -> DataFrame:
    """
    Fit a pipeline/model on train_df and return predictions on test_df.
    """
    model = model_pipeline.fit(train_df)
    predictions = model.transform(test_df)
    return predictions


def summarize_binary_predictions(
    pred_df: DataFrame,
    label_col: str = "is_fraud",
    pred_col: str = "prediction",
    model_name: str = "Model"
) -> dict:
    """
    Compute TN, FP, FN, TP and fraud-focused / non-fraud-focused metrics.
    """
    cm = (
        pred_df.groupBy(label_col, pred_col)
        .count()
        .orderBy(label_col, pred_col)
    )

    counts = {
        (int(row[label_col]), int(row[pred_col])): row["count"]
        for row in cm.collect()
    }

    tn = counts.get((0, 0), 0)
    fp = counts.get((0, 1), 0)
    fn = counts.get((1, 0), 0)
    tp = counts.get((1, 1), 0)

    fraud_precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    fraud_recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fraud_f1 = (
        2 * fraud_precision * fraud_recall / (fraud_precision + fraud_recall)
        if (fraud_precision + fraud_recall) > 0 else 0.0
    )

    nonfraud_recall = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    return {
        "model": model_name,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "fraud_precision": fraud_precision,
        "fraud_recall": fraud_recall,
        "fraud_f1": fraud_f1,
        "nonfraud_recall": nonfraud_recall
    }


def build_comparison_df(spark, summaries: list) -> DataFrame:
    """
    Convert a list of metric dictionaries into a Spark DataFrame.
    """
    rows = [
        (
            s["model"],
            int(s["tn"]),
            int(s["fp"]),
            int(s["fn"]),
            int(s["tp"]),
            float(round(s["fraud_precision"], 4)),
            float(round(s["fraud_recall"], 4)),
            float(round(s["fraud_f1"], 4)),
            float(round(s["nonfraud_recall"], 4)),
        )
        for s in summaries
    ]

    return spark.createDataFrame(
        rows,
        schema=[
            "model",
            "tn",
            "fp",
            "fn",
            "tp",
            "fraud_precision",
            "fraud_recall",
            "fraud_f1",
            "nonfraud_recall"
        ]
    )

def show_summary(spark, summary: dict):
    """
    Display a single experiment summary as a one-row Spark table.
    """
    build_comparison_df(spark, [summary]).show(truncate=False)

def run_experiment(
    model_pipeline,
    train_df: DataFrame,
    test_df: DataFrame,
    model_name: str,
    label_col: str = "is_fraud",
    pred_col: str = "prediction"
):
    """
    Fit, score, and summarize one experiment.
    """
    preds = fit_and_score_model(model_pipeline, train_df, test_df)
    summary = summarize_binary_predictions(
        preds,
        label_col=label_col,
        pred_col=pred_col,
        model_name=model_name
    )
    return preds, summary