# MSBX 5420 Final Project  
## Detecting and Preventing Credit Card Fraud Through Code-Based Solutions  
### Distributed Data Modeling & Analysis with PySpark  

---

## Course Information
**Course:** MSBX 5420 – Unstructured and Distributed Data Modeling & Analysis  
**Institution:** University of Colorado Boulder  

---

## Project Team
- Lora Abeyta
- Stephanie Furst
- Joshua Kosakowsky

---

## Project Overview

This project develops a **scalable, distributed fraud detection framework** using PySpark to analyze large-scale credit card transaction data.

The objective is to identify fraudulent behavior within a highly imbalanced dataset by leveraging:

- Distributed data processing
- Feature engineering
- Class imbalance mitigation strategies
- Machine learning models
- Evaluation metrics aligned to real-world fraud detection tradeoffs

The project emphasizes **practical decision-making**, particularly the balance between fraud detection and minimizing false positives.

---

## Repository Navigation

### Core Notebooks

- ```notebooks/01_eda_local.ipynb```  
  Exploratory Data Analysis (EDA) and initial data understanding

- ```notebooks/03_ml_fraud_modeling.ipynb```  
  Model development, parameter tuning, and evaluation

- ```emr/Credit_Card_Fraud_Detection_Case_Study.ipynb```  
  Integrated workflow combining EDA, feature engineering, and modeling for execution on Docker or AWS EMR

---

### Source Code
- ```src/project/transform.py```  
  Data cleaning and feature engineering

- ```src/project/fraud_modeling.py```  
  Reproducible machine learning workflows, including training, tuning, and evaluation

- ```src/project/spark_session.py```  
  Spark session configuration

  - ```src/project/schemas.py```  
  Explicit schema definitions for structured data processing

- ```src/project/config.py```  
  Centralized configuration management

---

### Configuration
- ```configs/local.yaml```  
  Local execution parameters

- ```configs/cluster.yaml```  
  AWS EMR execution parameters

---

### Outputs
- ```data/models/```  
  Saved model outputs and experiment results (Parquet)

---

## Data Description

The dataset consists of **~1.3 million credit card transactions** with a binary fraud label:

- ```is_fraud = 1``` → Fraudulent transaction  
- ```is_fraud = 0``` → Legitimate transaction  

Key characteristics:
- Severe class imbalance (fraud << non-fraud)
- Transactional, temporal, and geographic features
- Realistic fraud detection constraints

---

## Methodology

### 1. Data Processing
- Distributed ingestion using PySpark
- Schema enforcement and data cleaning
- Transformation into analysis-ready format

---

### 2. Feature Engineering
Key engineered features include:

- Temporal indicators (hour, day, weekend, night activity)
- Transaction amount transformations (log scaling, high-amount flags, relative comparisons)
- Geographic distance proxy between user and merchant

These features are designed to reflect **behavioral fraud patterns**.

---

### 3. Handling Class Imbalance
Multiple strategies were evaluated:

- Undersampling majority class  
- Oversampling minority class  
- Hybrid sampling approaches  
- Class weighting in models  

The goal was to improve fraud detection without overwhelming false positives.

---

### 4. Modeling Approaches

#### Logistic Regression
- Interpretable baseline model  
- Tuned using:
  - Regularization (regParam)
  - Elastic Net mixing
  - Iterations
  - Classification threshold  

#### Random Forest
- Nonlinear model capturing complex interactions  
- Tuned using:
  - Number of trees  
  - Minimum instances per node  
  - Feature subset strategy  
  - Maximum tree depth  
 
---

### 5. Evaluation Metrics

Given the business context, standard accuracy is insufficient.

Primary metrics:

- **Fraud Recall**  
  Ability to detect fraudulent transactions

- **Fraud Precision**  
  Accuracy of fraud predictions

- **F1 Score**  
  Balance between precision and recall

- **Non-Fraud Recall**  
  Ensures legitimate transactions are not incorrectly declined

---

## Key Insights

- Class imbalance significantly impacts model performance
- Threshold tuning is critical for aligning with business goals
- Feature engineering improves model separability
- Random Forest demonstrates stronger fraud detection performance, with increased computational cost
- Tradeoffs between recall and precision must be carefully managed

---

## Pipeline Flow

Data flows through the following stages:

Ingest → Transform → Feature Engineering → Model Training → Evaluation → Output

All major outputs are saved for reproducibility and visualization.

---

## Results and Outputs

Model outputs and experiment results are stored as parquet files in:

- ```data/models/lr_param_tuning```  
- ```data/models/lr_threshold_tuning```  
- ```data/models/rf_param_tuning```  
- ```data/models/rf_depth_tuning```  
- ```data/models/final_model_comparison```  

These outputs support downstream analysis and visualization.

---

## Project Scope

This project includes:

- Distributed data processing with PySpark  
- Feature engineering for fraud detection  
- Machine learning model development and tuning  
- Evaluation using business-relevant metrics  
- Scalable execution on AWS EMR  
- Structured streaming simulation  

---

## Notes for Review

- Notebooks are organized in logical execution order
- Core logic is modularized in ```src/project/```  
- Outputs are persisted for reproducibility  
- Visualizations are separated for clarity and presentation
- The Credit Card Fraud Detection Case Study notebook provides a consolidated workflow for EMR-based execution, combining EDA and modeling into a single pipeline  

---

## Conclusion

This project demonstrates how distributed data systems and machine learning can be combined to address real-world fraud detection challenges.

The approach prioritizes:

- Scalability  
- Interpretability  
- Practical decision-making  

while maintaining strong analytical rigor.

---
