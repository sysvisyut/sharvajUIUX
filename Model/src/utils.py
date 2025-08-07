"""
Utility functions for the Credit Score Prediction Model
Includes helper functions for data validation, feature engineering, and model utilities
"""

import pandas as pd
import numpy as np
import json
import yaml
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import logging
import hashlib
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Data validation utilities for credit score prediction
    """
    
    @staticmethod
    def validate_schema(df: pd.DataFrame, expected_schema: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate dataframe against expected schema
        
        Args:
            df (pd.DataFrame): Input dataframe
            expected_schema (Dict[str, str]): Expected column types
            
        Returns:
            Dict[str, Any]: Validation results
        """
        results = {
            'is_valid': True,
            'missing_columns': [],
            'extra_columns': [],
            'type_mismatches': [],
            'warnings': []
        }
        
        # Check for missing columns
        expected_cols = set(expected_schema.keys())
        actual_cols = set(df.columns)
        
        results['missing_columns'] = list(expected_cols - actual_cols)
        results['extra_columns'] = list(actual_cols - expected_cols)
        
        # Check data types
        for col, expected_type in expected_schema.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                if not DataValidator._is_compatible_type(actual_type, expected_type):
                    results['type_mismatches'].append({
                        'column': col,
                        'expected': expected_type,
                        'actual': actual_type
                    })
        
        # Set overall validity
        results['is_valid'] = (
            len(results['missing_columns']) == 0 and 
            len(results['type_mismatches']) == 0
        )
        
        return results
    
    @staticmethod
    def _is_compatible_type(actual: str, expected: str) -> bool:
        """Check if actual type is compatible with expected type"""
        compatibility_map = {
            'float': ['float64', 'float32', 'int64', 'int32'],
            'int': ['int64', 'int32', 'Int64'],
            'bool': ['bool'],
            'object': ['object', 'category'],
            'category': ['object', 'category']
        }
        
        return actual in compatibility_map.get(expected, [expected])
    
    @staticmethod
    def validate_business_rules(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Validate business rules for credit score features
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            List[Dict[str, Any]]: List of validation violations
        """
        violations = []
        
        # Rule 1: Ratio features should be between 0 and 1
        ratio_features = ['rent_on_time_rate', 'savings_ratio', 'loan_repayment_consistency', 'digital_payment_activity']
        for feature in ratio_features:
            if feature in df.columns:
                invalid_rows = df[(df[feature] < 0) | (df[feature] > 1)]
                if not invalid_rows.empty:
                    violations.append({
                        'rule': f'{feature} should be between 0 and 1',
                        'violation_count': len(invalid_rows),
                        'sample_values': invalid_rows[feature].head().tolist()
                    })
        
        # Rule 2: Age should be reasonable (18-100)
        if 'age' in df.columns:
            invalid_age = df[(df['age'] < 18) | (df['age'] > 100)]
            if not invalid_age.empty:
                violations.append({
                    'rule': 'Age should be between 18 and 100',
                    'violation_count': len(invalid_age),
                    'sample_values': invalid_age['age'].head().tolist()
                })
        
        # Rule 3: Dependents count should be non-negative
        if 'dependents_count' in df.columns:
            invalid_dependents = df[df['dependents_count'] < 0]
            if not invalid_dependents.empty:
                violations.append({
                    'rule': 'Dependents count should be non-negative',
                    'violation_count': len(invalid_dependents),
                    'sample_values': invalid_dependents['dependents_count'].head().tolist()
                })
        
        # Rule 4: Payment delay should be non-negative
        if 'avg_utility_payment_delay' in df.columns:
            invalid_delay = df[df['avg_utility_payment_delay'] < 0]
            if not invalid_delay.empty:
                violations.append({
                    'rule': 'Average utility payment delay should be non-negative',
                    'violation_count': len(invalid_delay),
                    'sample_values': invalid_delay['avg_utility_payment_delay'].head().tolist()
                })
        
        return violations

class FeatureEngineering:
    """
    Advanced feature engineering utilities
    """
    
    @staticmethod
    def create_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create composite risk scores from existing features
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with new risk score features
        """
        df_copy = df.copy()
        
        # Payment Risk Score (0-1, lower is better)
        if 'rent_on_time_rate' in df_copy.columns and 'loan_repayment_consistency' in df_copy.columns:
            df_copy['payment_risk_score'] = 1 - ((df_copy['rent_on_time_rate'] + df_copy['loan_repayment_consistency']) / 2)
        
        # Financial Stability Score (higher is better)
        if 'monthly_cashflow' in df_copy.columns and 'savings_ratio' in df_copy.columns:
            # Normalize monthly cashflow to 0-1 range
            cashflow_normalized = (df_copy['monthly_cashflow'] - df_copy['monthly_cashflow'].min()) / \
                                (df_copy['monthly_cashflow'].max() - df_copy['monthly_cashflow'].min())
            df_copy['financial_stability_score'] = (cashflow_normalized + df_copy['savings_ratio']) / 2
        
        # Digital Adoption Score
        if 'digital_payment_activity' in df_copy.columns:
            df_copy['digital_adoption_score'] = df_copy['digital_payment_activity']
        
        # Demographic Risk Score
        if 'age' in df_copy.columns and 'dependents_count' in df_copy.columns:
            # Normalize age (peak earning years 30-50 get lower risk)
            age_risk = np.abs(df_copy['age'] - 40) / 40  # Distance from age 40
            dependent_risk = df_copy['dependents_count'] / df_copy['dependents_count'].max()
            df_copy['demographic_risk_score'] = (age_risk + dependent_risk) / 2
        
        return df_copy
    
    @staticmethod
    def create_categorical_interactions(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features between categorical variables
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with interaction features
        """
        df_copy = df.copy()
        
        # Education-Employment interaction
        if 'education_level' in df_copy.columns and 'employment_type' in df_copy.columns:
            df_copy['education_employment'] = df_copy['education_level'].astype(str) + '_' + df_copy['employment_type'].astype(str)
        
        # Region-Employment interaction
        if 'region_type' in df_copy.columns and 'employment_type' in df_copy.columns:
            df_copy['region_employment'] = df_copy['region_type'].astype(str) + '_' + df_copy['employment_type'].astype(str)
        
        return df_copy
    
    @staticmethod
    def create_binned_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create binned versions of continuous features
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with binned features
        """
        df_copy = df.copy()
        
        # Age bins
        if 'age' in df_copy.columns:
            df_copy['age_group'] = pd.cut(df_copy['age'], 
                                        bins=[0, 25, 35, 50, 65, 100], 
                                        labels=['Young', 'Adult', 'Middle-aged', 'Senior', 'Elderly'])
        
        # Income bins (using monthly_cashflow as proxy)
        if 'monthly_cashflow' in df_copy.columns:
            df_copy['income_tier'] = pd.qcut(df_copy['monthly_cashflow'], 
                                           q=5, 
                                           labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        
        # Savings ratio bins
        if 'savings_ratio' in df_copy.columns:
            df_copy['savings_category'] = pd.cut(df_copy['savings_ratio'], 
                                               bins=[0, 0.1, 0.2, 0.3, 1.0], 
                                               labels=['Low Saver', 'Moderate Saver', 'Good Saver', 'High Saver'])
        
        return df_copy

class ModelUtilities:
    """
    Utility functions for model training and evaluation
    """
    
    @staticmethod
    def calculate_alternative_credit_score(df_row: pd.Series, weights: Dict[str, float] = None) -> int:
        """
        Calculate alternative credit score using our features
        
        Args:
            df_row (pd.Series): Single row of data
            weights (Dict[str, float]): Feature weights
            
        Returns:
            int: Credit score (300-850 range)
        """
        if weights is None:
            weights = {
                'rent_on_time_rate': 0.25,  # Primary indicator of payment history
                'loan_repayment_consistency': 0.20,  # Key for repayment behavior
                'savings_ratio': 0.10,  # Reflects financial discipline
                'digital_payment_activity': 0.08,  # Secondary financial behavior
                'monthly_cashflow': 0.15,  # Critical for repayment capacity
                'avg_utility_payment_delay': 0.08,  # Specific payment history
                'education_level': 0.05,  # Contextual personal factor
                'employment_type': 0.05,  # Contextual stability factor
                'region_type': 0.02,  # Minimal direct impact
                'has_existing_loans': 0.02  # Minor risk indicator
            }
        
        score = 300  # Base score
        weighted_score = 0
        
        # Positive contributors
        positive_features = [
            'rent_on_time_rate', 'loan_repayment_consistency', 'savings_ratio',
            'digital_payment_activity'
        ]
        
        for feature in positive_features:
            if feature in df_row.index and not pd.isna(df_row[feature]):
                weighted_score += df_row[feature] * weights.get(feature, 0)
        
        # Negative contributors (need normalization)
        if 'avg_utility_payment_delay' in df_row.index and not pd.isna(df_row['avg_utility_payment_delay']):
            # Convert delay to 0-1 scale (0 days = 1.0, 30+ days = 0.0)
            delay_score = max(0, 1 - (df_row['avg_utility_payment_delay'] / 30))
            weighted_score += delay_score * weights.get('avg_utility_payment_delay', 0)
        
        # Categorical features (simplified scoring)
        education_scores = {'None': 0.0, 'Primary': 0.2, 'Secondary': 0.4, 'UG': 0.8, 'PG': 1.0, 'PhD': 1.0}
        if 'education_level' in df_row.index:
            edu_score = education_scores.get(df_row['education_level'], 0.5)
            weighted_score += edu_score * weights.get('education_level', 0)
        
        employment_scores = {'Unemployed': 0.0, 'Gig': 0.4, 'Self-employed': 0.6, 'Salaried': 1.0}
        if 'employment_type' in df_row.index:
            emp_score = employment_scores.get(df_row['employment_type'], 0.5)
            weighted_score += emp_score * weights.get('employment_type', 0)
        
        # Convert weighted score to final score
        final_score = score + int(weighted_score * 550)  # Scale to 300-850 range
        
        return min(max(final_score, 300), 850)  # Ensure within valid range

    
    @staticmethod
    def create_credit_score_bands(scores: np.ndarray) -> np.ndarray:
        """
        Convert credit scores to categorical bands
        
        Args:
            scores (np.ndarray): Credit scores
            
        Returns:
            np.ndarray: Credit score bands
        """
        bands = np.full(scores.shape, 'Unknown', dtype=object)
        bands[scores >= 750] = 'Excellent'
        bands[(scores >= 700) & (scores < 750)] = 'Good'
        bands[(scores >= 650) & (scores < 700)] = 'Fair'
        bands[(scores >= 600) & (scores < 650)] = 'Poor'
        bands[scores < 600] = 'Very Poor'
        
        return bands

class ConfigManager:
    """
    Configuration management utilities
    """
    
    def __init__(self, config_path: str = None):
        """Initialize config manager"""
        self.config_path = config_path or "config.yaml"
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_path} not found. Using defaults.")
            return self.get_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file"""
        with open(self.config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'data': {
                'input_file': "data/financial_dataset.csv",
                'train_size': 0.6,
                'val_size': 0.2,
                'test_size': 0.2,
                'random_state': 42
            },
            'preprocessing': {
                'handle_outliers': True,
                'create_interactions': True,
                'scaling_method': 'standard'
            },
            'model': {
                'type': 'xgboost',
                'hyperparameters': {
                    'n_estimators': 100,
                    'max_depth': 6,
                    'learning_rate': 0.1
                }
            },
            'evaluation': {
                'cv_folds': 5,
                'metrics': ['rmse', 'mae', 'r2']
            }
        }

class ComplianceUtils:
    """
    Utilities for ensuring compliance with regulations
    """
    
    @staticmethod
    def anonymize_data(df: pd.DataFrame, sensitive_columns: List[str] = None) -> pd.DataFrame:
        """
        Anonymize sensitive data
        
        Args:
            df (pd.DataFrame): Input dataframe
            sensitive_columns (List[str]): Columns to anonymize
            
        Returns:
            pd.DataFrame: Anonymized dataframe
        """
        df_copy = df.copy()
        
        if sensitive_columns is None:
            sensitive_columns = []
        
        for col in sensitive_columns:
            if col in df_copy.columns:
                # Hash the values
                df_copy[col] = df_copy[col].apply(
                    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:10] if pd.notna(x) else x
                )
        
        return df_copy
    
    @staticmethod
    def create_audit_log(action: str, data_info: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """
        Create audit log entry
        
        Args:
            action (str): Action performed
            data_info (Dict[str, Any]): Information about data processed
            user_id (str): User ID (if available)
            
        Returns:
            Dict[str, Any]: Audit log entry
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'data_info': data_info,
            'user_id': user_id or 'system'
        }
        
        return log_entry
    
    @staticmethod
    def validate_consent(user_consents: Dict[str, bool]) -> bool:
        """
        Validate user consent for data processing
        
        Args:
            user_consents (Dict[str, bool]): User consent flags
            
        Returns:
            bool: Whether all required consents are given
        """
        required_consents = [
            'data_collection',
            'data_processing',
            'credit_scoring',
            'data_storage'
        ]
        
        return all(user_consents.get(consent, False) for consent in required_consents)

def load_financial_dataset(file_path: str = "data/financial_dataset.csv") -> pd.DataFrame:
    """
    Load the financial dataset from the specified path
    
    Args:
        file_path (str): Path to the financial dataset CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Financial dataset loaded successfully. Shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        logger.error(f"Dataset not found at: {file_path}")
        raise FileNotFoundError(f"Please ensure the dataset exists at: {file_path}")
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        raise

# Example configuration file content
EXAMPLE_CONFIG = """
# Credit Score Prediction Model Configuration

data:
  input_file: "data/financial_dataset.csv"
  output_directory: "results/"
  train_size: 0.6
  val_size: 0.2  
  test_size: 0.2
  random_state: 42

preprocessing:
  handle_missing_values: true
  handle_outliers: true
  create_interactions: true
  scaling_method: "standard"  # standard, minmax, robust
  encoding_method: "mixed"    # onehot, ordinal, mixed

model:
  type: "xgboost"  # xgboost, lightgbm, catboost, random_forest
  hyperparameters:
    n_estimators: 100
    max_depth: 6
    learning_rate: 0.1
    random_state: 42

evaluation:
  cv_folds: 5
  metrics: ["rmse", "mae", "r2"]
  save_predictions: true

compliance:
  anonymize_sensitive_data: true
  audit_logging: true
  consent_validation: true

feature_weights:
  rent_on_time_rate: 0.20
  loan_repayment_consistency: 0.15
  savings_ratio: 0.15
  digital_payment_activity: 0.10
  monthly_cashflow: 0.10
  avg_utility_payment_delay: 0.10
  education_level: 0.08
  employment_type: 0.07
  region_type: 0.03
  has_existing_loans: 0.02
"""

if __name__ == "__main__":
    # Example usage
    print("Credit Score Model Utilities Loaded Successfully!")
    print("Data file expected at: data/financial_dataset.csv")
