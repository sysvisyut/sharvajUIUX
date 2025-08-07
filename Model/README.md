# Credit Score Prediction Model

This project implements an alternative credit scoring system that helps students and individuals with limited credit history by using non-traditional data sources like rent payment history, education level, utility payments, and digital financial behavior.

## Project Overview

Traditional credit scoring systems rely heavily on credit history, which creates barriers for:
- Students and young adults
- New immigrants
- People with limited banking relationships
- Individuals from underbanked communities

Our model uses alternative data sources to provide more inclusive credit scoring while maintaining compliance with RBI guidelines and the Digital Personal Data Protection (DPDP) Act 2023.

## Features Used for Credit Scoring

| Feature | Type | Description |
|---------|------|-------------|
| `rent_on_time_rate` | Float (0-1) | % of months rent paid on time |
| `avg_utility_payment_delay` | Integer | Average days late in paying utility bills |
| `education_level` | Categorical | Highest education level achieved |
| `monthly_cashflow` | Float | Average monthly income minus expenses (₹) |
| `savings_ratio` | Float (0-1) | Portion of income saved monthly |
| `region_type` | Categorical | Urban, Semi-urban, Rural classification |
| `employment_type` | Categorical | Employment category |
| `has_existing_loans` | Boolean | Current loan status |
| `loan_repayment_consistency` | Float (0-1) | Past EMI payment consistency |
| `digital_payment_activity` | Float (0-1) | % of expenses via digital payments |
| `age` | Integer | User age |
| `dependents_count` | Integer | Number of financial dependents |

## Project Structure (as of now)

```
Model/
├── src/
│   ├── data_preprocessing.py    # Data cleaning and preprocessing
│   ├── data_visualization.py    # Streamlined model evaluation plots
│   ├── model_training.py        # Model training scripts (to be added)
│   ├── model_evaluation.py      # Model evaluation utilities (to be added)
│   └── utils.py                 # Utility functions and compliance tools
├── notebooks/                   # Jupyter notebooks for analysis
├── Compliance/                  # Regulatory compliance documentation
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Preprocessing

```python
from src.data_preprocessing import CreditScoreDataPreprocessor

# Initialize preprocessor
preprocessor = CreditScoreDataPreprocessor()

# Load and preprocess data
X_train, X_test, y_train, y_test, report = preprocessor.preprocess_pipeline(
    csv_path="path/to/your/data.csv",
    target_column="credit_score",  # if available
    create_interactions=True,
    handle_outliers=True
)
```

### Data Visualization

```python
from src.data_visualization import plot_feature_relationships, evaluate_model_performance

# Load your data
import pandas as pd
df = pd.read_csv("path/to/your/data.csv")

# Plot feature relationships with target
plot_feature_relationships(df, target_col="credit_score")

# Evaluate trained model performance
evaluate_model_performance(
    model=trained_model,
    X_test=X_test,
    y_test=y_test,
    train_history=training_history,  # optional
    model_type='regression'
)
```

### Utility Functions

```python
from src.utils import DataValidator, FeatureEngineering, ComplianceUtils

# Validate data schema
validator = DataValidator()
validation_results = validator.validate_schema(df, expected_schema)

# Create advanced features
engineer = FeatureEngineering()
df_enhanced = engineer.create_risk_scores(df)

# Ensure compliance
compliance = ComplianceUtils()
anonymized_df = compliance.anonymize_data(df, sensitive_columns=['user_id'])
```

## Key Features

### 1. Comprehensive Data Preprocessing
- Automated data type validation
- Smart missing value imputation using KNN
- Outlier detection and handling
- Feature scaling and encoding
- Business rule validation

### 2. Advanced Feature Engineering
- Risk score creation
- Categorical interactions
- Binned features for non-linear relationships
- Payment reliability indices

### 3. Rich Visualizations
- Distribution analysis
- Correlation heatmaps
- Outlier detection plots
- Interactive dashboards with Plotly
- Feature relationship analysis

### 4. Compliance & Security
- Data anonymization utilities
- Audit logging
- Consent validation
- RBI guideline compliance checks

### 5. Model Utilities
- Alternative credit score calculation
- Traditional score comparison
- Credit band categorization
- Configuration management

## Compliance Features

### RBI Guidelines
- Transparent scoring methodology
- Explainable feature contributions
- Regular model validation
- Bias detection and mitigation

### DPDP Act 2023 Compliance
- Consent-based data collection
- Data minimization principles
- User rights implementation (access, correction, deletion)
- Secure data handling and storage

### Account Aggregator Framework
- Integration ready for AA-based data collection
- Consent artifact management
- Secure data transmission protocols

## Best Practices Implemented

1. **Data Quality**: Comprehensive validation and cleaning
2. **Feature Engineering**: Domain-expert guided feature creation
3. **Preprocessing**: Robust handling of missing values and outliers
4. **Visualization**: Interactive and comprehensive EDA tools
5. **Compliance**: Built-in regulatory compliance features
6. **Documentation**: Comprehensive code documentation
7. **Modularity**: Clean, reusable code architecture

## Model Training Approach (Next Steps)

### Recommended Models
1. **Tree-based models**: XGBoost, LightGBM, CatBoost
2. **Traditional ML**: Random Forest, Gradient Boosting
3. **Deep Learning**: TabNet, TabTransformer (for large datasets)

### Evaluation Strategy
- Cross-validation with stratification
- Fairness metrics monitoring
- SHAP/LIME for explainability
- A/B testing framework

## Future Enhancements

1. **Real-time Scoring API**: Flask/FastAPI implementation
2. **Model Monitoring**: Drift detection and retraining
3. **Advanced Features**: Alternative data integration
4. **Regulatory Updates**: Continuous compliance monitoring

## Contributing

1. Follow PEP 8 style guidelines
2. Add comprehensive docstrings
3. Include unit tests for new features
4. Update documentation

## License

This project is designed for educational and research purposes. Ensure compliance with local regulations before production use.

## Contact

For questions about regulatory compliance or technical implementation, please refer to the documentation in the `Compliance/` folder.
