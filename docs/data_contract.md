# Data Contract: Credit Card Transactions Fraud Dataset

---

## Overview

This document defines the expected structure, data types, and quality rules for the raw transaction dataset used in the fraud detection project.

The purpose of this contract is to ensure that data loaded into the PySpark pipeline is:

- structurally consistent
- compatible with the defined Spark schema
- suitable for downstream feature engineering, analysis, and modeling

This contract applies to the **raw input dataset** before transformation, feature engineering, or model resampling.

---

## Dataset Source

- **Name:** Credit Card Transactions Dataset (Priyam Choksi)
- **Format:** CSV
- **Volume:** ~1.3 million records
- **Primary Label Column:** `is_fraud`
- **Source Link:** [Credit Card Transactions Dataset](https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset)

---

## Spark Schema

The raw dataset is expected to conform to the following schema:

| Column Name | Spark Type | Nullable | Description |
|---|---|---:|---|
| `Unnamed: 0` | `LongType` | Yes | Original row index from source file |
| `trans_date_trans_time` | `TimestampType` | Yes | Transaction timestamp |
| `cc_num` | `StringType` | Yes | Credit card number identifier |
| `merchant` | `StringType` | Yes | Merchant name |
| `category` | `StringType` | Yes | Merchant transaction category |
| `amt` | `DoubleType` | Yes | Transaction amount |
| `first` | `StringType` | Yes | Customer first name |
| `last` | `StringType` | Yes | Customer last name |
| `gender` | `StringType` | Yes | Customer gender |
| `street` | `StringType` | Yes | Customer street address |
| `city` | `StringType` | Yes | Customer city |
| `state` | `StringType` | Yes | Customer state |
| `zip` | `StringType` | Yes | Customer ZIP code |
| `lat` | `DoubleType` | Yes | Customer latitude |
| `long` | `DoubleType` | Yes | Customer longitude |
| `city_pop` | `IntegerType` | Yes | Population of customer city |
| `job` | `StringType` | Yes | Customer job title |
| `dob` | `DateType` | Yes | Customer date of birth |
| `trans_num` | `StringType` | Yes | Transaction identifier |
| `unix_time` | `LongType` | Yes | Unix timestamp of transaction |
| `merch_lat` | `DoubleType` | Yes | Merchant latitude |
| `merch_long` | `DoubleType` | Yes | Merchant longitude |
| `is_fraud` | `IntegerType` | Yes | Fraud label (`0` = non-fraud, `1` = fraud) |
| `merch_zipcode` | `StringType` | Yes | Merchant ZIP code |

---

## Contract Scope

This contract governs the **raw ingested dataset only**.

It does **not** apply to:
- transformed datasets
- encoded feature sets
- train/test splits
- oversampled training data
- model output datasets

Those downstream datasets may intentionally differ from the raw contract.

---

## Required Fields for Modeling

Although many fields are technically nullable in the Spark schema for ingestion flexibility, the following columns are considered **required for usable analytical and modeling records**:

- `trans_date_trans_time`
- `category`
- `amt`
- `is_fraud`

These fields are required because they are either:
- core business identifiers,
- necessary for time-based feature engineering,
- necessary for transaction behavior analysis, or
- directly required for supervised fraud modeling.

Records missing these values may be dropped or excluded during cleaning, depending on pipeline rules.

---

## Field Expectations and Validation Rules

### `is_fraud`
- Must contain only:
  - `0` for legitimate transactions
  - `1` for fraudulent transactions
- Null values are not acceptable for modeling

### `amt`
- Must be numeric
- Must be greater than 0
- Extremely large values may be retained if valid, but should be reviewed as potential anomalies

### `category`
- Expected to be populated for modeling and exploratory analysis
- Should represent a meaningful merchant transaction category
- Null or blank values may be treated as invalid for modeling records

### `trans_date_trans_time`
- Must be parseable as a timestamp
- Should align logically with `unix_time`
- Future timestamps would be considered suspicious in a production setting, but may still be accepted in this historical dataset if present and validated

### Geographic Fields
- `lat`, `long`, `merch_lat`, and `merch_long` should be valid numeric coordinates when present
- Missing coordinates may reduce feature engineering quality but do not necessarily invalidate the entire raw record unless required by a specific modeling stage

---

## Nullability vs. Business Use

The Spark schema allows nullable fields to support ingestion robustness, but nullable in schema does **not** mean optional for business use.

This distinction exists because:

- ingestion should not fail immediately for every imperfect row
- data cleaning rules can decide whether to drop, impute, or retain records
- some columns are essential for modeling even if technically nullable in raw form

---

## Duplicate Policy

### Raw Dataset
Duplicate transactions are **not expected** in the raw source data.

In particular:
- duplicate `trans_num` values should be flagged for investigation
- exact duplicate rows should also be flagged

### Training Data
Duplicates may later appear **intentionally** during model preparation due to oversampling of the minority fraud class.

This is acceptable because:
- the duplication is a modeling strategy
- it occurs after ingestion and cleaning
- it does not indicate source data quality failure

Therefore, duplicate checks in this contract apply only to the **raw dataset**, not resampled training sets.

---

## Data Quality Checks

The pipeline should validate the following during ingestion or early preprocessing:

- schema matches expected Spark schema
- row count is greater than zero
- required modeling fields are present
- `is_fraud` contains only valid labels
- `amt` is numeric and positive
- duplicate `trans_num` values are checked
- null counts are profiled for major fields
- fraud class distribution is reviewed due to expected class imbalance

---

## Expected Class Distribution

The dataset is expected to be **highly imbalanced**, with legitimate transactions greatly outnumbering fraudulent ones.

This imbalance is a known characteristic of fraud detection data and is not considered a contract violation.

Class imbalance will be addressed later in the ML pipeline using methods such as:

- oversampling
- undersampling
- class weighting

---

## Handling Contract Violations

Possible responses to contract violations include:

### Critical Failures
These may stop the pipeline:
- unreadable file
- missing expected columns
- invalid schema
- missing `is_fraud` column
- empty dataset

### Non-Critical Failures
These may be logged and handled during cleaning:
- null values in non-essential columns
- invalid or missing geographic values
- blank descriptive fields

### Review Conditions
These should be flagged for investigation:
- duplicate `trans_num`
- unexpected label values in `is_fraud`
- abnormal numeric ranges
- timestamp inconsistencies

---

## Storage Expectations

Raw and processed data may be stored in the following locations:

- Local development: `data/raw`
- Cloud storage: Amazon S3

The same schema and validation expectations should apply regardless of storage location.

---

## Version

- **Version:** 1.0
- **Project:** Fraud Detection in Large-Scale Financial Transactions