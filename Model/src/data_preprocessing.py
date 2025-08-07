"""
Credit Score Data Preprocessing Module
Handles data loading, cleaning, feature engineering and preparation for model training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
import logging
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreditScoreDataPreprocessor:
    """
    A comprehensive data preprocessing class for credit score prediction data
    """
    
    def __init__(self):
        """Initialize the preprocessor with scalers and encoders"""
        self.standard_scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.numerical_features = [
            'age', 'employment_stability_months', 'monthly_income', 'monthly_rent', 
            'monthly_cashflow', 'rent_payment_consistency', 'utility_payment_consistency',
            'phone_payment_consistency', 'insurance_payment_consistency', 'num_subscriptions',
            'subscription_payment_consistency', 'minimum_bank_balance', 'monthly_savings',
            'savings_goal_completion_rate', 'p2p_monthly_volume', 'risky_p2p_ratio', 'monthly_overdrafts'
        ]
        self.categorical_features = ['state', 'education_level', 'employment_type', 'loan_approval']
        self.boolean_features = []  # No boolean features in new dataset
        
    def load_data(self, csv_path: str) -> pd.DataFrame:
        """
        Load data from CSV file with validation
        
        Args:
            csv_path (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Data loaded successfully. Shape: {df.shape}")
            logger.info(f"Columns found: {list(df.columns)}")
            
            # Validate expected columns for credit invisibility dataset
            expected_columns = [
                'age', 'state', 'education_level', 'employment_type', 'employment_stability_months',
                'monthly_income', 'monthly_rent', 'monthly_cashflow', 'rent_payment_consistency',
                'utility_payment_consistency', 'phone_payment_consistency', 'insurance_payment_consistency',
                'num_subscriptions', 'subscription_payment_consistency', 'minimum_bank_balance',
                'monthly_savings', 'savings_goal_completion_rate', 'p2p_monthly_volume', 'risky_p2p_ratio',
                'monthly_overdrafts'
            ]
            
            missing_columns = set(expected_columns) - set(df.columns)
            if missing_columns:
                logger.warning(f"Missing expected columns: {missing_columns}")
            
            # Check for missing values
            missing_info = df.isnull().sum()
            if missing_info.sum() > 0:
                logger.info(f"Missing values detected: {missing_info[missing_info > 0].to_dict()}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and convert data types according to specifications
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with corrected data types
        """
        df_copy = df.copy()
        
        # Convert boolean features - handle string values
        for col in self.boolean_features:
            if col in df_copy.columns:
                # Convert string representations to boolean
                df_copy[col] = df_copy[col].astype(str).str.lower()
                df_copy[col] = df_copy[col].map({'true': True, 'false': False, '1': True, '0': False})
                df_copy[col] = df_copy[col].fillna(False).astype(bool)
        
        # Convert numerical features with better error handling
        for col in self.numerical_features:
            if col in df_copy.columns:
                # Convert to numeric, handling any string values
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
                
                if col in ['avg_utility_payment_delay', 'age']:
                    # For integer columns, convert to Int64 (nullable integer)
                    df_copy[col] = df_copy[col].astype('Int64')
                # Float columns remain as float64
        
        # Convert categorical features
        for col in self.categorical_features:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].astype(str).astype('category')
        
        logger.info("Data types validated and converted")
        logger.info(f"Data types: {df_copy.dtypes.to_dict()}")
        
        return df_copy
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values using appropriate strategies
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with imputed missing values
        """
        df_copy = df.copy()
        
        logger.info("Handling missing values...")
        
        # Check missing values before processing
        missing_before = df_copy.isnull().sum()
        if missing_before.sum() > 0:
            logger.info(f"Missing values before imputation: {missing_before[missing_before > 0].to_dict()}")
        
        # Handle numerical features with KNN imputation
        numerical_cols = [col for col in self.numerical_features if col in df_copy.columns]
        if numerical_cols:
            # Create a separate dataframe for imputation (only numerical columns)
            numerical_data = df_copy[numerical_cols].copy()
            
            # Convert Int64 to float64 for KNN imputation
            for col in numerical_data.columns:
                if numerical_data[col].dtype == 'Int64':
                    numerical_data[col] = numerical_data[col].astype('float64')
            
            imputer = KNNImputer(n_neighbors=5)
            imputed_values = imputer.fit_transform(numerical_data)
            
            # Put imputed values back
            for i, col in enumerate(numerical_cols):
                df_copy[col] = imputed_values[:, i]
                
                # Convert back to Int64 for integer columns
                if col in ['avg_utility_payment_delay', 'age']:
                    df_copy[col] = df_copy[col].round().astype('Int64')
        
        # Handle categorical features with mode
        for col in self.categorical_features:
            if col in df_copy.columns and df_copy[col].isnull().any():
                mode_value = df_copy[col].mode()
                mode_value = mode_value[0] if not mode_value.empty else 'Unknown'
                df_copy[col] = df_copy[col].fillna(mode_value)
        
        # Handle boolean features
        for col in self.boolean_features:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].fillna(False)
        
        # Check missing values after processing
        missing_after = df_copy.isnull().sum()
        if missing_after.sum() > 0:
            logger.warning(f"Remaining missing values: {missing_after[missing_after > 0].to_dict()}")
        else:
            logger.info("All missing values handled successfully")
        
        return df_copy
    
    def detect_outliers(self, df: pd.DataFrame, method: str = 'iqr') -> Dict[str, List]: 
        #detecting data that lies outside the normal range
        """
        Detect outliers in numerical features
        
        Args:
            df (pd.DataFrame): Input dataframe
            method (str): Method to use ('iqr' or 'zscore')
            
        Returns:
            Dict[str, List]: Dictionary with outlier indices for each feature
        """
        outliers = {}
        
        for col in self.numerical_features:
            if col in df.columns:
                if method == 'iqr':
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers[col] = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
                
                elif method == 'zscore':
                    z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                    outliers[col] = df[z_scores > 3].index.tolist()
        
        logger.info(f"Outliers detected using {method} method")
        return outliers
    
    def create_feature_interactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create meaningful feature interactions for credit invisibility data
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with new interaction features
        """
        df_copy = df.copy()
        
        # Payment reliability score - average of all payment consistencies
        payment_cols = ['rent_payment_consistency', 'utility_payment_consistency', 
                       'phone_payment_consistency', 'insurance_payment_consistency',
                       'subscription_payment_consistency']
        available_payment_cols = [col for col in payment_cols if col in df_copy.columns]
        if available_payment_cols:
            df_copy['overall_payment_reliability'] = df_copy[available_payment_cols].mean(axis=1)
        
        # Income to rent ratio (housing affordability)
        if 'monthly_income' in df_copy.columns and 'monthly_rent' in df_copy.columns:
            df_copy['income_to_rent_ratio'] = df_copy['monthly_income'] / (df_copy['monthly_rent'] + 1)  # +1 to avoid division by zero
        
        # Financial cushion (income minus essential expenses)
        if 'monthly_income' in df_copy.columns and 'monthly_rent' in df_copy.columns:
            estimated_essentials = df_copy['monthly_rent'] + 300  # rent + estimated utilities/food
            df_copy['financial_cushion'] = (df_copy['monthly_income'] - estimated_essentials) / df_copy['monthly_income']
            df_copy['financial_cushion'] = df_copy['financial_cushion'].clip(lower=-1, upper=1)
        
        # Savings efficiency (how well they save relative to available income)
        if 'monthly_savings' in df_copy.columns and 'monthly_cashflow' in df_copy.columns:
            df_copy['savings_efficiency'] = df_copy['monthly_savings'] / (df_copy['monthly_cashflow'] + 1)
            df_copy['savings_efficiency'] = df_copy['savings_efficiency'].clip(lower=0, upper=2)
        
        # Risk behavior score (combines risky P2P and overdrafts)
        risk_factors = []
        if 'risky_p2p_ratio' in df_copy.columns:
            risk_factors.append(df_copy['risky_p2p_ratio'])
        if 'monthly_overdrafts' in df_copy.columns:
            # Normalize overdrafts to 0-1 scale
            max_overdrafts = df_copy['monthly_overdrafts'].max()
            if max_overdrafts > 0:
                risk_factors.append(df_copy['monthly_overdrafts'] / max_overdrafts)
        
        if risk_factors:
            df_copy['risk_behavior_score'] = sum(risk_factors) / len(risk_factors)
        
        # Employment stability factor
        if 'employment_stability_months' in df_copy.columns and 'age' in df_copy.columns:
            # Normalize by age to get relative stability
            df_copy['employment_stability_ratio'] = df_copy['employment_stability_months'] / (df_copy['age'] * 12 + 1)
            df_copy['employment_stability_ratio'] = df_copy['employment_stability_ratio'].clip(upper=1)
        
        logger.info("Feature interactions created for credit invisibility data")
        return df_copy
    
    def encode_categorical_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Encode categorical features using appropriate methods
        
        Args:
            df (pd.DataFrame): Input dataframe
            fit (bool): Whether to fit encoders or use existing ones
            
        Returns:
            pd.DataFrame: Dataframe with encoded categorical features
        """
        df_copy = df.copy()
        
        # Define ordinal mappings for credit invisibility data
        ordinal_mappings = {
            'education_level': {'high_school': 0, 'some_college': 1, 'bachelors': 2, 'graduate': 3}
        }
        
        # Apply ordinal encoding for ordinal features
        for col, mapping in ordinal_mappings.items():
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].astype(str).map(mapping)
                df_copy[col] = df_copy[col].fillna(0).astype(int)  # Default to lowest category and convert to int
        
        # One-hot encode nominal categorical features
        nominal_features = ['employment_type', 'state', 'loan_approval']
        for col in nominal_features:
            if col in df_copy.columns:
                if fit:
                    # Create dummy variables
                    dummies = pd.get_dummies(df_copy[col], prefix=col, drop_first=True)
                    df_copy = pd.concat([df_copy.drop(col, axis=1), dummies], axis=1)
                    # Store column names for later use
                    self.feature_names.extend(dummies.columns.tolist())
        
        logger.info("Categorical features encoded")
        return df_copy
    
    def scale_features(self, df: pd.DataFrame, fit: bool = True, exclude_targets: bool = True) -> pd.DataFrame:
        """
        Scale numerical features using StandardScaler
        
        Args:
            df (pd.DataFrame): Input dataframe
            fit (bool): Whether to fit scaler or use existing one
            exclude_targets (bool): Whether to exclude target variables from scaling
            
        Returns:
            pd.DataFrame: Dataframe with scaled features
        """
        df_copy = df.copy()
        
        # Target variables to exclude from scaling
        target_vars = ['credit_score', 'loan_approval'] if exclude_targets else []
        
        # Get numerical columns that exist in the dataframe and are actually numeric
        numerical_cols = []
        for col in df_copy.columns:
            if df_copy[col].dtype in ['int64', 'float64', 'Int64', 'Float64']:
                if col not in target_vars:  # Exclude target variables
                    numerical_cols.append(col)
        
        logger.info(f"Scaling {len(numerical_cols)} numerical columns: {numerical_cols}")
        if target_vars:
            excluded_targets = [col for col in target_vars if col in df_copy.columns]
            if excluded_targets:
                logger.info(f"Excluding target variables from scaling: {excluded_targets}")
        
        if numerical_cols:
            # Convert Int64 to float64 for scaling
            scaling_data = df_copy[numerical_cols].copy()
            for col in numerical_cols:
                if scaling_data[col].dtype == 'Int64':
                    scaling_data[col] = scaling_data[col].astype('float64')
            
            if fit:
                scaled_features = self.standard_scaler.fit_transform(scaling_data)
            else:
                scaled_features = self.standard_scaler.transform(scaling_data)
            
            # Replace original columns with scaled versions
            df_copy[numerical_cols] = scaled_features
        
        logger.info("Features scaled successfully")
        return df_copy
    
    def prepare_train_val_test_split(self, df: pd.DataFrame, target_column: str = None, 
                                   train_size: float = 0.6, val_size: float = 0.2, test_size: float = 0.2,
                                   random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
        """
        Split data into training, validation, and testing sets
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_column (str): Name of target column (if None, returns X splits with None for y splits)
            train_size (float): Proportion of data for training (default: 0.6)
            val_size (float): Proportion of data for validation (default: 0.2)
            test_size (float): Proportion of data for testing (default: 0.2)
            random_state (int): Random state for reproducibility
            
        Returns:
            Tuple: X_train, X_val, X_test, y_train, y_val, y_test
        """
        # Validate that proportions sum to 1.0
        if not np.isclose(train_size + val_size + test_size, 1.0):
            raise ValueError(f"train_size ({train_size}) + val_size ({val_size}) + test_size ({test_size}) must sum to 1.0")
        
        if target_column and target_column in df.columns:
            # Define all target columns to exclude from features
            target_columns = ['credit_score', 'loan_approval']
            available_targets = [col for col in target_columns if col in df.columns]
            
            # Drop all target columns from features
            X = df.drop(available_targets, axis=1)
            y = df[target_column]
            
            # First split: separate test set
            X_temp, X_test, y_temp, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, 
                stratify=y if y.dtype == 'object' else None
            )
            
            # Second split: separate train and validation from remaining data
            # Adjust val_size for the remaining data after test split
            remaining_val_proportion = val_size / (train_size + val_size)
            X_train, X_val, y_train, y_val = train_test_split(
                X_temp, y_temp, test_size=remaining_val_proportion, random_state=random_state,
                stratify=y_temp if y_temp.dtype == 'object' else None
            )
        else:
            X = df
            
            # First split: separate test set
            X_temp, X_test = train_test_split(X, test_size=test_size, random_state=random_state)
            
            # Second split: separate train and validation from remaining data
            remaining_val_proportion = val_size / (train_size + val_size)
            X_train, X_val = train_test_split(X_temp, test_size=remaining_val_proportion, random_state=random_state)
            
            y_train, y_val, y_test = None, None, None
        
        logger.info(f"Data split completed - Training: {X_train.shape}, Validation: {X_val.shape}, Test: {X_test.shape}")
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def prepare_train_test_split(self, df: pd.DataFrame, target_column: str = None, 
                               test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split data into training and testing sets (backward compatibility method)
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_column (str): Name of target column (if None, returns X_train, X_test, None, None)
            test_size (float): Proportion of data for testing
            random_state (int): Random state for reproducibility
            
        Returns:
            Tuple: X_train, X_test, y_train, y_test
        """
        train_size = 1.0 - test_size
        X_train, X_val, X_test, y_train, y_val, y_test = self.prepare_train_val_test_split(
            df, target_column, train_size=train_size, val_size=0.0, test_size=test_size, random_state=random_state
        )
        
        # Combine train and val sets for backward compatibility
        if X_val is not None and len(X_val) > 0:
            X_train = pd.concat([X_train, X_val], ignore_index=True)
            if y_train is not None and y_val is not None:
                y_train = pd.concat([y_train, y_val], ignore_index=True)
        
        logger.info(f"Data split completed (backward compatibility). Training set: {X_train.shape}, Test set: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def preprocess_pipeline(self, csv_path: str, target_column: str = None, 
                          create_interactions: bool = True, handle_outliers: bool = False,
                          train_size: float = 0.6, val_size: float = 0.2, test_size: float = 0.2) -> Tuple:
        """
        Complete preprocessing pipeline with train/validation/test split
        
        Args:
            csv_path (str): Path to CSV file
            target_column (str): Name of target column
            create_interactions (bool): Whether to create feature interactions
            handle_outliers (bool): Whether to handle outliers
            train_size (float): Proportion of data for training (default: 0.6)
            val_size (float): Proportion of data for validation (default: 0.2)  
            test_size (float): Proportion of data for testing (default: 0.2)
            
        Returns:
            Tuple: X_train, X_val, X_test, y_train, y_val, y_test, preprocessing_report
        """
        logger.info("Starting preprocessing pipeline...")
        
        # Load data
        df = self.load_data(csv_path)
        
        # Validate data types
        df = self.validate_data_types(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Detect outliers (for reporting)
        outliers = self.detect_outliers(df)
        
        # Handle outliers if requested
        if handle_outliers:
            # Simple outlier capping at 95th percentile
            for col in self.numerical_features:
                if col in df.columns and col in outliers and len(outliers[col]) > 0:
                    upper_cap = df[col].quantile(0.95)
                    lower_cap = df[col].quantile(0.05)
                    df[col] = df[col].clip(lower=lower_cap, upper=upper_cap)
        
        # Create feature interactions
        if create_interactions:
            df = self.create_feature_interactions(df)
        
        # Encode categorical features
        df = self.encode_categorical_features(df, fit=True)
        
        # Scale features
        df = self.scale_features(df, fit=True)
        
        # Split data into train/val/test
        X_train, X_val, X_test, y_train, y_val, y_test = self.prepare_train_val_test_split(
            df, target_column, train_size, val_size, test_size
        )
        
        # Create preprocessing report
        preprocessing_report = {
            'original_shape': df.shape,
            'train_shape': X_train.shape,
            'val_shape': X_val.shape,
            'test_shape': X_test.shape,
            'split_proportions': {'train': train_size, 'val': val_size, 'test': test_size},
            'outliers_detected': {k: len(v) for k, v in outliers.items()},
            'features_created': list(df.columns),
            'missing_values_handled': True,
            'categorical_encoded': True,
            'features_scaled': True
        }
        
        logger.info("Preprocessing pipeline completed successfully")
        return X_train, X_val, X_test, y_train, y_val, y_test, preprocessing_report
    
    def preprocess_pipeline_simple(self, csv_path: str, target_column: str = None, 
                                  create_interactions: bool = True, handle_outliers: bool = False,
                                  test_size: float = 0.2) -> Tuple:
        """
        Simple preprocessing pipeline with train/test split (backward compatibility)
        
        Args:
            csv_path (str): Path to CSV file
            target_column (str): Name of target column
            create_interactions (bool): Whether to create feature interactions
            handle_outliers (bool): Whether to handle outliers
            test_size (float): Proportion of data for testing
            
        Returns:
            Tuple: X_train, X_test, y_train, y_test, preprocessing_report
        """
        # Use the main pipeline with validation size = 0
        train_size = 1.0 - test_size
        X_train, X_val, X_test, y_train, y_val, y_test, report = self.preprocess_pipeline(
            csv_path, target_column, create_interactions, handle_outliers,
            train_size=train_size, val_size=0.0, test_size=test_size
        )
        
        # Update report format for backward compatibility
        report['final_shape'] = (X_train.shape[0] + X_test.shape[0], X_train.shape[1])
        
        return X_train, X_test, y_train, y_test, report

def validate_data_ranges(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Validate that data values are within expected ranges
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        Dict[str, List[str]]: Validation issues found
    """
    issues = {'warnings': [], 'errors': []}
    
    # Check ratio features (should be between 0 and 1)
    ratio_features = ['rent_on_time_rate', 'savings_ratio', 'loan_repayment_consistency', 'digital_payment_activity']
    for col in ratio_features:
        if col in df.columns:
            if df[col].min() < 0 or df[col].max() > 1:
                issues['errors'].append(f"{col} contains values outside [0,1] range")
    
    # Check age (reasonable range)
    if 'age' in df.columns:
        if df['age'].min() < 18 or df['age'].max() > 100:
            issues['warnings'].append("Age values outside typical range [18,100]")
    
    # Removed dependents_count validation as requested
    
    return issues

if __name__ == "__main__":
    """
    Main execution block - runs when file is executed directly
    """
    print("🚀 Starting Credit Score Data Preprocessing...")
    
    # Initialize preprocessor
    preprocessor = CreditScoreDataPreprocessor()
    
    # Path to your dataset
    data_path = r"..\data\financial_dataset.csv"
    
    try:
        print(f"📂 Processing data from: {data_path}")
        
        # Run complete preprocessing pipeline
        X_train, X_val, X_test, y_train, y_val, y_test, report = preprocessor.preprocess_pipeline(
            csv_path=data_path,
            target_column='credit_score',  # Using credit_score as primary target
            create_interactions=True,
            handle_outliers=False,
            train_size=0.6,
            val_size=0.2,
            test_size=0.2
        )
        
        # Display results
        print("\n✅ Preprocessing completed successfully!")
        print("\n📊 Dataset Information:")
        print(f"   • Training set: {X_train.shape}")
        print(f"   • Validation set: {X_val.shape}")
        print(f"   • Test set: {X_test.shape}")
        
        if y_train is not None:
            print(f"\n🎯 Target Variable (credit_score):")
            print(f"   • Training target: {y_train.shape}")
            print(f"   • Mean credit score: {y_train.mean():.1f}")
            print(f"   • Credit score range: {y_train.min():.0f} - {y_train.max():.0f}")
        
        print(f"\n🔧 Features created: {len(X_train.columns)} total")
        print(f"   • Feature names: {list(X_train.columns)}")
        
        print(f"\n📈 Preprocessing Report:")
        for key, value in report.items():
            if key != 'features_created':  # Skip long feature list
                print(f"   • {key}: {value}")
        
        # Show sample of processed data
        print(f"\n👀 Sample processed data (first 3 rows):")
        print(X_train.head(3))
        
        if y_train is not None:
            print(f"\n🎯 Sample target values:")
            print(f"   • Credit scores: {y_train.head(3).values}")
        
    except FileNotFoundError:
        print(f"❌ Error: Dataset not found at {data_path}")
        print("Please ensure your CSV file is at: data/financial_dataset.csv")
    except Exception as e:
        print(f"❌ Error during preprocessing: {str(e)}")
        print("Check your data format and column names.")
