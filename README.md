<div align="center">

# Credit Card Fraud Detection

A full end-to-end fraud analytics and machine learning project built entirely in notebooks, covering exploratory data analysis, feature engineering, predictive modeling, explainability, and causal inference.

<p align="center">
  <img src="https://img.shields.io/github/repo-size/Nomusa990822/YOUR-EXACT-REPO-NAME?style=for-the-badge&logo=github&color=0f172a" />
  <img src="https://img.shields.io/github/languages/code-size/Nomusa990822/YOUR-EXACT-REPO-NAME?style=for-the-badge&logo=github&color=1d4ed8" />
  <img src="https://img.shields.io/github/last-commit/Nomusa990822/YOUR-EXACT-REPO-NAME?style=for-the-badge&logo=git&color=0891b2" />
  <img src="https://img.shields.io/github/commit-activity/m/Nomusa990822/YOUR-EXACT-REPO-NAME?style=for-the-badge&logo=github&color=0ea5e9" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/languages/count/Nomusa990822/YOUR-EXACT-REPO-NAME?style=for-the-badge&logo=github&color=155e75" />
  <img src="https://img.shields.io/github/top-language/Nomusa990822/YOUR-EXACT-REPO-NAME?style=for-the-badge&logo=jupyter&color=0369a1" />
  <img src="https://img.shields.io/github/issues/Nomusa990822/YOUR-EXACT-REPO-NAME?style=for-the-badge&logo=github&color=082f49" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-0f172a?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-1d4ed8?style=for-the-badge&logo=jupyter" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-0891b2?style=for-the-badge&logo=pandas" />
  <img src="https://img.shields.io/badge/Scikit--Learn-Modeling-0ea5e9?style=for-the-badge&logo=scikitlearn" />
  <img src="https://img.shields.io/badge/XGBoost-Optimization-155e75?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SHAP-Explainability-0369a1?style=for-the-badge" />
  <img src="https://img.shields.io/badge/DoubleML-Causal%20Inference-082f49?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Notebook%20Pipeline-0f172a?style=for-the-badge" />
</p>

</div>

---

## Overview

This repository presents a notebook-based fraud detection pipeline built on a large credit card transaction dataset. The project was designed to move beyond basic classification and develop a more complete analytics workflow that answers five major questions:

1. What patterns define fraudulent behavior in the raw data?
2. Which engineered features improve fraud detection most?
3. Which predictive models perform best on an imbalanced classification problem?
4. Why does the final model make the decisions it makes?
5. Which important variables are merely predictive, and which show evidence of causal influence?

The project is intentionally organized as a sequence of notebooks so that each stage is transparent, reproducible, and easy to review.

---

## Project Objectives

- Perform high-quality exploratory data analysis on fraud transactions
- Build strong fraud-relevant engineered features
- Train and compare multiple machine learning models
- Optimize the best model for precision-recall trade-offs
- Explain predictions globally and locally using SHAP
- Extend the project beyond prediction into causal analysis with Double Machine Learning

---

## Notebook Pipeline

**1. `01_eda.ipynb`**
Exploratory data analysis focused on understanding transaction behavior, class imbalance, temporal risk patterns, geographic fraud concentration, category-level behavior, demographic trends, and core fraud signals.

**2. `02_feature_engineering.ipynb`**
Feature engineering notebook that transforms raw transactional data into a richer modeling dataset, including behavioral, temporal, customer-level, merchant-level, location-level, and category-based risk features.

**3. `03_modeling_and_optimization.ipynb`**
Model development notebook where baseline models are trained, tuned, evaluated, compared, and optimized for the fraud detection objective.

**4. `04_explainability.ipynb`**
Explainability notebook that uses SHAP and error analysis to understand global feature importance, local decision patterns, false positives, false negatives, and probability behavior around the final threshold.

**5. `05_doubleML.ipynb`**
Causal analysis notebook that applies Double Machine Learning to estimate the causal impact of selected high-value fraud-related features.

---

## Repository Structure

```text
Credit-Card-Fraud-Detection/
│
├── 01_eda.ipynb
├── 02_feature_engineering.ipynb
├── 03_modeling_and_optimization.ipynb
├── 04_explainability.ipynb
├── 05_doubleML.ipynb
├── requirements.txt
└── README.md
```
---

## End-to-End Workflow

```mermaid
flowchart TD
    A[Raw Fraud Dataset] --> B[01 EDA]
    B --> C[Fraud Pattern Discovery]
    C --> D[02 Feature Engineering]
    D --> E[Engineered Training and Test Features]
    E --> F[03 Modeling and Optimization]
    F --> G[Baseline Models]
    G --> H[Tuned Final Model]
    H --> I[04 Explainability]
    I --> J[SHAP Global and Local Explanations]
    I --> K[Error Analysis]
    H --> L[05 DoubleML]
    L --> M[Causal Effect Estimation]
```
---

## System Architecture

```mermaid
flowchart LR
    A[Raw Transaction Data] --> B[EDA Layer]
    B --> C[Feature Engineering Layer]
    C --> D[Modeling Layer]
    D --> E[Optimization Layer]
    E --> F[Explainability Layer]
    E --> G[Causal Inference Layer]

    C1[Temporal Features]
    C2[Behavioral Features]
    C3[Customer Aggregates]
    C4[Merchant Risk Features]
    C5[Category Risk Features]
    C6[Geographic Risk Features]

    C --> C1
    C --> C2
    C --> C3
    C --> C4
    C --> C5
    C --> C6
```

---

## Notebook Dependency Map

```mermaid 
graph TD
    N1[01 EDA] --> N2[02 Feature Engineering]
    N2 --> N3[03 Modeling and Optimization]
    N3 --> N4[04 Explainability]
    N2 --> N5[05 DoubleML]
```

---

## Core Methods Used

**1. Exploratory Data Analysis**

- Class balance analysis
- Distribution analysis
- Log-transformed amount analysis
- Temporal fraud profiling
- State and city concentration analysis
- Category and gender comparisons
- Geographic plotting
- Correlation analysis

**2. Feature Engineering**

- Transaction amount transformations
- High-value transaction flags
- Customer historical aggregates
- Same-day transaction behavior
- Merchant risk statistics
- Category-level fraud context
- Geographic risk summaries
- Night transaction behavior
- Age band and population band indicators

**3. Predictive Modeling**

- Logistic Regression
- Random Forest
- XGBoost

**4. Model Optimization**

- Hyperparameter tuning
- Threshold optimization
- Precision-recall trade-off analysis
- Final model comparison

**5. Explainability**

- Global feature importance
- SHAP summary plots
- SHAP dependence analysis
- High-risk and low-risk local case analysis
- False positive and false negative profiling

**6. Causal Analysis**

- Double Machine Learning
- Partially Linear Regression framework
- Multiple feature causal effect estimation

---

## Key Project Highlights

* Handles an extreme class imbalance problem in a principled way
* Uses fraud-sensitive metrics such as Precision, Recall, F1-score, ROC-AUC, and PR-AUC
* Moves from descriptive analysis to predictive modeling to causal interpretation
* Demonstrates both model performance and model transparency
* Includes threshold tuning instead of relying on default classification cutoffs
* Distinguishes between predictive importance and causal relevance

---

## Recommended Reading Order

For the clearest understanding of the project, review the notebooks in this order:

- ```01_eda.ipynb```
- ```02_feature_engineering.ipynb```
- ```03_modeling_and_optimization.ipynb```
- ```04_explainability.ipynb```
- ```05_doubleML.ipynb```

---

## Example Analytical Questions Answered
* Which transaction patterns are most associated with fraud?
* How does fraud risk vary across hours, days, and months?
* Which states, cities, and categories are most exposed?
* Which engineered features matter most for model performance?
* Which model offers the strongest precision-recall balance?
* What kinds of transactions become false positives and false negatives?
* Which top predictive drivers also show evidence of causal importance?

---
## Technical Themes Demonstrated

* Large-scale tabular fraud analytics
* Imbalanced binary classification
* Feature engineering for behavioral risk
* Interpretable machine learning
* Threshold optimization
* Error analysis
* Causal machine learning

---

## Modeling Decision Pipeline

```mermaid
flowchart TD
    A[Engineered Features] --> B[Baseline Models]
    B --> C[Metric Comparison]
    C --> D[Best Candidate Selection]
    D --> E[Hyperparameter Tuning]
    E --> F[Threshold Search]
    F --> G[Final Optimized Model]
    G --> H[Explainability]
    G --> I[Business Interpretation]
```

---

## Explainability Logic

```mermaid 
flowchart TD
    A[Final Optimized Model] --> B[Global SHAP Importance]
    A --> C[Local SHAP Explanations]
    A --> D[Prediction Probability Analysis]
    A --> E[False Negative Analysis]
    A --> F[False Positive Analysis]
    B --> G[Most Influential Features]
    C --> H[Case-Level Decision Drivers]
    D --> I[Threshold Separation]
    E --> J[Missed Fraud Pattern]
    F --> K[Over-Flagged Legitimate Pattern]
```
---

## Causal Inference Logic

```mermaid
flowchart TD
    A[Top Predictive Features from SHAP] --> B[Select Candidate Treatments]
    B --> C[DoubleML PLR Framework]
    C --> D[Control for High-Dimensional Confounders]
    D --> E[Estimate Causal Effect]
    E --> F[Compare Predictive Importance vs Causal Influence]
```
---

## Project Deliverables
- A structured five-notebook fraud pipeline
- Engineered modeling datasets
- Baseline and optimized classification models
- Explainability analysis of the final model
- Causal effect estimates for selected fraud drivers

---

## Future Improvements

* Sequence modeling for transaction history
* Graph-based fraud detection
* Real-time scoring simulation
* Calibration diagnostics
* Drift monitoring across time periods
* Advanced uplift or treatment heterogeneity analysis

---

## Author

**Nomusa Shongwe**
Data Science | Machine Learning | Fraud Analytics | Explainable AI | Causal Inference

---

## License
This project is released under the MIT License.
