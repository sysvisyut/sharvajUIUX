"""
Comprehensive XGBoost Model for Credit Score Prediction
Includes hyperparameter tuning, proper feature importance, and full model pipeline
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import preprocessing pipeline and visualization
from data_preprocessing import CreditScoreDataPreprocessor
from data_visualization import evaluate_model_performance, plot_feature_relationships, StreamlinedVisualizer

class XGBoostCreditScoreModel:
    """
    Complete XGBoost model with hyperparameter tuning for credit score prediction
    """
    
    def __init__(self, enable_hyperparameter_tuning=True, n_iter=20):
        """
        Initialize the XGBoost model
        
        Args:
            enable_hyperparameter_tuning (bool): Whether to perform hyperparameter tuning
            n_iter (int): Number of iterations for RandomizedSearchCV
        """
        self.enable_hyperparameter_tuning = enable_hyperparameter_tuning
        self.n_iter = n_iter
        self.model = None
        self.best_params = None
        self.feature_names = None
        self.preprocessor = CreditScoreDataPreprocessor()
        
        # Default parameters (optimized for memory efficiency)
        self.default_params = {
            'objective': 'reg:squarederror',
            'n_estimators': 200,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'min_child_weight': 1,
            'gamma': 0,
            'reg_alpha': 0.1,
            'reg_lambda': 1,
            'random_state': 42,
            'verbosity': 0,
            'n_jobs': 1  # Single thread to avoid memory issues
        }
        
        # Hyperparameter search space
        self.param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [4, 6, 8],
            'learning_rate': [0.05, 0.1, 0.15],
            'subsample': [0.7, 0.8, 0.9],
            'colsample_bytree': [0.7, 0.8, 0.9],
            'min_child_weight': [1, 3, 5],
            'gamma': [0, 0.1, 0.2],
            'reg_alpha': [0, 0.1, 0.3],
            'reg_lambda': [1, 1.5, 2]
        }
    
    def load_and_preprocess_data(self, data_path, target_column='credit_score'):
        """
        Load and preprocess the data
        
        Args:
            data_path (str): Path to the dataset
            target_column (str): Name of the target column
            
        Returns:
            tuple: Preprocessed train, validation, and test sets
        """
        print(f"📂 Loading and preprocessing data from: {data_path}")
        
        # Run preprocessing pipeline
        X_train, X_val, X_test, y_train, y_val, y_test, report = self.preprocessor.preprocess_pipeline(
            csv_path=data_path,
            target_column=target_column,
            create_interactions=True,
            handle_outliers=False,
            train_size=0.6,
            val_size=0.2,
            test_size=0.2
        )
        
        self.feature_names = X_train.columns.tolist()
        
        print(f"✅ Data preprocessing completed!")
        print(f"   • Training set: {X_train.shape}")
        print(f"   • Validation set: {X_val.shape}")
        print(f"   • Test set: {X_test.shape}")
        print(f"   • Number of features: {len(self.feature_names)}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def hyperparameter_tuning(self, X_train, y_train, X_val, y_val):
        """
        Perform hyperparameter tuning using RandomizedSearchCV
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
            
        Returns:
            dict: Best parameters found
        """
        print(f"🔧 Starting Hyperparameter Tuning (n_iter={self.n_iter})...")
        
        # Create base model
        base_model = xgb.XGBRegressor(
            objective='reg:squarederror',
            random_state=42,
            verbosity=0,
            n_jobs=1
        )
        
        # Setup randomized search with memory-efficient parameters
        random_search = RandomizedSearchCV(
            estimator=base_model,
            param_distributions=self.param_grid,
            n_iter=self.n_iter,
            scoring='neg_mean_squared_error',
            cv=3,  # Reduced CV folds to save memory
            verbose=1,
            random_state=42,
            n_jobs=1
        )
        
        # Fit the search
        random_search.fit(X_train, y_train)
        
        self.best_params = random_search.best_params_
        best_score = -random_search.best_score_
        
        print(f"✅ Hyperparameter tuning completed!")
        print(f"   • Best CV Score (MSE): {best_score:.2f}")
        print(f"   • Best Parameters:")
        for param, value in self.best_params.items():
            print(f"     - {param}: {value}")
        
        return self.best_params
    
    def train_model(self, X_train, y_train, X_val, y_val, use_best_params=True):
        """
        Train the XGBoost model
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
            use_best_params (bool): Whether to use best parameters from tuning
        """
        print(f"🚀 Training XGBoost Model...")
        
        # Choose parameters
        if use_best_params and self.best_params:
            params = {**self.default_params, **self.best_params}
            print(f"   • Using tuned parameters")
        else:
            params = self.default_params
            print(f"   • Using default parameters")
        
        # Initialize and train model
        self.model = xgb.XGBRegressor(**params)
        
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_val, y_val)],
            verbose=False
        )
        
        print(f"✅ Model training completed!")
    
    def evaluate_model(self, X_train, X_val, X_test, y_train, y_val, y_test):
        """
        Evaluate the model performance
        
        Args:
            X_train, X_val, X_test: Feature sets
            y_train, y_val, y_test: Target sets
            
        Returns:
            dict: Evaluation metrics
        """
        print(f"📈 Evaluating Model Performance...")
        
        # Make predictions
        y_train_pred = self.model.predict(X_train)
        y_val_pred = self.model.predict(X_val)
        y_test_pred = self.model.predict(X_test)
        
        # Calculate metrics
        def calculate_metrics(y_true, y_pred, dataset_name):
            metrics = {
                'mse': mean_squared_error(y_true, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
                'mae': mean_absolute_error(y_true, y_pred),
                'r2': r2_score(y_true, y_pred)
            }
            
            print(f"   📊 {dataset_name} Metrics:")
            print(f"      • MSE: {metrics['mse']:.2f}")
            print(f"      • RMSE: {metrics['rmse']:.2f}")
            print(f"      • MAE: {metrics['mae']:.2f}")
            print(f"      • R²: {metrics['r2']:.4f}")
            
            return metrics
        
        train_metrics = calculate_metrics(y_train, y_train_pred, "Training")
        val_metrics = calculate_metrics(y_val, y_val_pred, "Validation")
        test_metrics = calculate_metrics(y_test, y_test_pred, "Test")
        
        # Summary
        print("\n" + "="*60)
        print("XGBOOST MODEL PERFORMANCE SUMMARY")
        print("="*60)
        print(f"Training   → R²: {train_metrics['r2']:.4f} | RMSE: {train_metrics['rmse']:.2f}")
        print(f"Validation → R²: {val_metrics['r2']:.4f} | RMSE: {val_metrics['rmse']:.2f}")
        print(f"Test       → R²: {test_metrics['r2']:.4f} | RMSE: {test_metrics['rmse']:.2f}")
        print("="*60)
        
        return {
            'train': train_metrics,
            'validation': val_metrics,
            'test': test_metrics,
            'predictions': {
                'y_train_pred': y_train_pred,
                'y_val_pred': y_val_pred,
                'y_test_pred': y_test_pred
            }
        }
    
    def analyze_feature_importance(self, plot_top_n=15):
        """
        Analyze and visualize feature importance
        
        Args:
            plot_top_n (int): Number of top features to plot
            
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        print(f"🎯 Analyzing Feature Importance...")
        
        if self.model is None:
            print("❌ Model not trained yet!")
            return None
        
        # Get feature importances
        feature_importances = self.model.feature_importances_
        
        # Create importance dataframe
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': feature_importances
        }).sort_values('Importance', ascending=False)
        
        # Check if importances are valid
        total_importance = importance_df['Importance'].sum()
        if total_importance == 0:
            print("⚠️ Warning: All feature importances are zero!")
            return importance_df
        
        # Display top features
        print(f"🔍 Top {plot_top_n} Feature Importance:")
        top_features = importance_df.head(plot_top_n)
        for idx, row in top_features.iterrows():
            percentage = (row['Importance'] / total_importance) * 100
            print(f"   • {row['Feature']}: {row['Importance']:.4f} ({percentage:.1f}%)")
        
        # Plot feature importance
        plt.figure(figsize=(12, 10))
        colors = plt.cm.viridis(np.linspace(0, 1, len(top_features)))
        bars = plt.barh(range(len(top_features)), top_features['Importance'], color=colors, alpha=0.8)
        
        plt.yticks(range(len(top_features)), top_features['Feature'])
        plt.xlabel('Feature Importance', fontsize=12)
        plt.title(f'Top {plot_top_n} Feature Importance (XGBoost)', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        max_importance = top_features['Importance'].max()
        for i, (bar, importance) in enumerate(zip(bars, top_features['Importance'])):
            plt.text(bar.get_width() + max_importance * 0.01, 
                    bar.get_y() + bar.get_height()/2, 
                    f'{importance:.4f}', va='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.show()
        
        return importance_df
    
    def generate_visualizations(self, X_train, X_test, y_train, y_test, y_test_pred):
        """
        Generate comprehensive visualizations
        
        Args:
            X_train, X_test: Feature sets
            y_train, y_test: Target sets  
            y_test_pred: Test predictions
        """
        print(f"📊 Generating Comprehensive Visualizations...")
        
        try:
            # 1. Feature relationships with target
            print(f"   • Feature relationships...")
            combined_data = pd.concat([X_train, y_train], axis=1)
            plot_feature_relationships(combined_data, target_col='credit_score')
        except Exception as e:
            print(f"   ⚠️ Could not generate feature relationships: {str(e)}")
        
        try:
            # 2. Model evaluation visualizations
            print(f"   • Model evaluation plots...")
            evaluate_model_performance(
                model=self.model,
                X_test=X_test,
                y_test=y_test,
                feature_names=self.feature_names,
                model_type='regression'
            )
        except Exception as e:
            print(f"   ⚠️ Could not generate model evaluation plots: {str(e)}")
        
        try:
            # 3. Binary classification analysis
            print(f"   • Binary classification analysis...")
            median_score = y_test.median()
            y_test_binary = (y_test > median_score).astype(int)
            y_pred_binary = (y_test_pred > median_score).astype(int)
            
            visualizer = StreamlinedVisualizer()
            visualizer.plot_confusion_matrix(
                y_test_binary, 
                y_pred_binary, 
                classes=['Low Credit Score', 'High Credit Score'],
                title="XGBoost Binary Credit Score Classification"
            )
        except Exception as e:
            print(f"   ⚠️ Could not generate binary classification plots: {str(e)}")
    
    def save_model(self, filepath="../models/xgboost_credit_score_model_final.joblib"):
        """
        Save the trained model
        
        Args:
            filepath (str): Path to save the model
        """
        if self.model is None:
            print("❌ No model to save!")
            return
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model with metadata
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'best_params': self.best_params,
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        joblib.dump(model_data, filepath)
        print(f"💾 Model saved to: {filepath}")
    
    def run_complete_pipeline(self, data_path):
        """
        Run the complete XGBoost pipeline
        
        Args:
            data_path (str): Path to the dataset
            
        Returns:
            dict: Complete results including model, metrics, and importance
        """
        print("🚀 Starting Complete XGBoost Pipeline...")
        print("="*60)
        
        try:
            # 1. Load and preprocess data
            X_train, X_val, X_test, y_train, y_val, y_test = self.load_and_preprocess_data(data_path)
            
            # 2. Hyperparameter tuning (if enabled)
            if self.enable_hyperparameter_tuning:
                self.hyperparameter_tuning(X_train, y_train, X_val, y_val)
            else:
                print("🔧 Skipping hyperparameter tuning (using default parameters)")
            
            # 3. Train model
            self.train_model(X_train, y_train, X_val, y_val)
            
            # 4. Evaluate model
            results = self.evaluate_model(X_train, X_val, X_test, y_train, y_val, y_test)
            
            # 5. Feature importance analysis
            importance_df = self.analyze_feature_importance()
            
            # 6. Generate visualizations
            self.generate_visualizations(
                X_train, X_test, y_train, y_test, 
                results['predictions']['y_test_pred']
            )
            
            # 7. Save model
            self.save_model()
            
            print("\n🎉 XGBoost Pipeline Completed Successfully!")
            print(f"📊 Final Test R²: {results['test']['r2']:.4f}")
            print(f"📊 Final Test RMSE: {results['test']['rmse']:.2f}")
            
            return {
                'model': self.model,
                'results': results,
                'importance': importance_df,
                'best_params': self.best_params
            }
            
        except Exception as e:
            print(f"❌ Pipeline failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """
    Main function to run the XGBoost model
    """
    # Configuration
    DATA_PATH = r"C:\FT2\CodeZilla_FT2\Model\data\financial_dataset.csv"
    ENABLE_HYPERPARAMETER_TUNING = True  # Set to False for faster execution
    N_ITER = 15  # Number of hyperparameter combinations to try
    
    # Initialize and run model
    xgb_model = XGBoostCreditScoreModel(
        enable_hyperparameter_tuning=ENABLE_HYPERPARAMETER_TUNING,
        n_iter=N_ITER
    )
    
    # Run complete pipeline
    results = xgb_model.run_complete_pipeline(DATA_PATH)
    
    if results:
        print("\n" + "="*60)
        print("🏆 FINAL RESULTS SUMMARY")
        print("="*60)
        test_metrics = results['results']['test']
        print(f"Best Test R²: {test_metrics['r2']:.4f}")
        print(f"Best Test RMSE: {test_metrics['rmse']:.2f}")
        print(f"Best Test MAE: {test_metrics['mae']:.2f}")
        
        if results['best_params']:
            print(f"\nBest Hyperparameters:")
            for param, value in results['best_params'].items():
                print(f"  {param}: {value}")
        
        print("="*60)


if __name__ == "__main__":
    main()
