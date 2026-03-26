# Dataset Setup

## Overview

The dataset for this project is **not stored in GitHub** due to size limitations.

Each team member must download and place the dataset locally.

---

## 📁 Local Development Setup

After cloning the repository:

1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset)
2. Place it in:

data/raw/

Example:

data/raw/credit_card_transactions.csv

---

## ⚠️ Important

- The `data/raw/` folder is **ignored by Git**
- Do NOT commit dataset files
- Only code and configs should be pushed

---

## 🧪 Sample Data

A small sample dataset may be included in:

data/sample/

This is used for:
- testing
- quick development
- fallback if full dataset is missing

---

## ☁️ AWS / EMR Setup

The full dataset will be uploaded to S3:

Example:

s3://your-bucket-name/credit-card-transactions/

Cluster config will use:

configs/cluster.yaml

---

## 🔐 Credentials

- Do NOT commit Kaggle API keys
- Do NOT commit AWS credentials
- Use environment variables or local configuration only

---

## ✅ Summary

| Environment | Data Source |
|------------|------------|
| Local      | data/raw/ |
| Fallback   | data/sample/ |
| AWS EMR    | S3 |