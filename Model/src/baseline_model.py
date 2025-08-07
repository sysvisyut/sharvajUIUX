"""
Baseline Model for Credit Score Prediction
Simple Linear Regression model to establish baseline performance
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import preprocessing pipeline and visualization
from data_preprocessing import CreditScoreDataPreprocessor
from data_visualization import evaluate_model_performance, plot_feature_relationships

class BaselineLinearModel:
    """
    Baseline Linear Regression Model for Credit Score Prediction
    """
    
    def __init__(self):
        """Initialize the baseline model"""
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.feature_names = None
        self.training_metrics = {}
        self.validation_metrics = {}
        self.test_metrics = {}
        
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Train the linear regression model
        
        Args:
            X_train: Training features
            y_train: Training target (credit scores)
            X_val: Validation features (optional)
            y_val: Validation target (optional)
        """
        print("🔧 Training Linear Regression Baseline Model...")
        
        # Store feature names
        if hasattr(X_train, 'columns'):
            self.feature_names = list(X_train.columns)
        
        # Train the model
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        
        # Calculate training metrics
        y_train_pred = self.model.predict(X_train)
        self.training_metrics = self._calculate_metrics(y_train, y_train_pred, "Training")
        
        # Calculate validation metrics if provided
        if X_val is not None and y_val is not None:
            y_val_pred = self.model.predict(X_val)
            self.validation_metrics = self._calculate_metrics(y_val, y_val_pred, "Validation")
        
        print("✅ Model training completed!")
        self._print_metrics()
        
    def predict(self, X):
        """
        Make predictions using the trained model
        
        Args:
            X: Features to predict on
            
        Returns:
            numpy array of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be trained before making predictions!")
        
        # Check for NaN values before prediction
        if hasattr(X, 'isnull'):
            nan_count = X.isnull().sum().sum()
            if nan_count > 0:
                print(f"⚠️ Warning: Found {nan_count} NaN values in prediction data")
                # Fill NaN values with median for numerical columns
                X = X.fillna(X.median(numeric_only=True))
                print("✅ NaN values filled with column medians")
        
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data
        
        Args:
            X_test: Test features
            y_test: Test target values
            
        Returns:
            dict: Test metrics
        """
        if not self.is_fitted:
            raise ValueError("Model must be trained before evaluation!")
        
        print("📊 Evaluating model on test data...")
        
        # Check for NaN values before prediction
        if hasattr(X_test, 'isnull'):
            nan_count = X_test.isnull().sum().sum()
            if nan_count > 0:
                print(f"⚠️ Warning: Found {nan_count} NaN values in test data")
                print("NaN values by column:")
                nan_cols = X_test.isnull().sum()
                for col, count in nan_cols[nan_cols > 0].items():
                    print(f"   • {col}: {count}")
                
                # Fill NaN values with median for numerical columns
                X_test = X_test.fillna(X_test.median(numeric_only=True))
                print("✅ NaN values filled with column medians")
        
        # Make predictions
        y_test_pred = self.predict(X_test)
        
        # Calculate metrics
        self.test_metrics = self._calculate_metrics(y_test, y_test_pred, "Test")
        
        # Plot results
        self._plot_predictions(y_test, y_test_pred, "Test Set")
        
        return self.test_metrics
    
    def _calculate_metrics(self, y_true, y_pred, dataset_name):
        """Calculate regression metrics"""
        metrics = {
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred),
            'r2': r2_score(y_true, y_pred)
        }
        
        print(f"\n📈 {dataset_name} Metrics:")
        print(f"   • MSE: {metrics['mse']:.2f}")
        print(f"   • RMSE: {metrics['rmse']:.2f}")
        print(f"   • MAE: {metrics['mae']:.2f}")
        print(f"   • R²: {metrics['r2']:.4f}")
        
        return metrics
    
    def _print_metrics(self):
        """Print all available metrics"""
        print("\n" + "="*50)
        print("MODEL PERFORMANCE SUMMARY")
        print("="*50)
        
        if self.training_metrics:
            print(f"Training R²: {self.training_metrics['r2']:.4f}")
            print(f"Training RMSE: {self.training_metrics['rmse']:.2f}")
            
        if self.validation_metrics:
            print(f"Validation R²: {self.validation_metrics['r2']:.4f}")
            print(f"Validation RMSE: {self.validation_metrics['rmse']:.2f}")
            
        if self.test_metrics:
            print(f"Test R²: {self.test_metrics['r2']:.4f}")
            print(f"Test RMSE: {self.test_metrics['rmse']:.2f}")
    
    def _plot_predictions(self, y_true, y_pred, title="Predictions"):
        """Plot actual vs predicted values"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Scatter plot: Actual vs Predicted
        axes[0].scatter(y_true, y_pred, alpha=0.6, color='blue', s=30)
        
        # Perfect prediction line
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        axes[0].set_xlabel('Actual Credit Score')
        axes[0].set_ylabel('Predicted Credit Score')
        axes[0].set_title(f'Actual vs Predicted - {title}')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Add R² score to plot
        r2 = r2_score(y_true, y_pred)
        axes[0].text(0.05, 0.95, f'R² = {r2:.4f}', transform=axes[0].transAxes,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # Residual plot
        residuals = y_true - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.6, color='green', s=30)
        axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2)
        axes[1].set_xlabel('Predicted Credit Score')
        axes[1].set_ylabel('Residuals (Actual - Predicted)')
        axes[1].set_title(f'Residual Plot - {title}')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def get_feature_importance(self):
        """
        Get feature importance (coefficients) from the linear model
        
        Returns:
            pandas DataFrame: Feature importance
        """
        if not self.is_fitted:
            raise ValueError("Model must be trained before getting feature importance!")
        
        if self.feature_names is None:
            feature_names = [f'Feature_{i}' for i in range(len(self.model.coef_))]
        else:
            feature_names = self.feature_names
        
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': self.model.coef_,
            'Abs_Coefficient': np.abs(self.model.coef_)
        }).sort_values('Abs_Coefficient', ascending=False)
        
        return importance_df
    
    def plot_feature_importance(self, top_n=10):
        """Plot feature importance"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before plotting feature importance!")
        
        importance_df = self.get_feature_importance()
        
        # Plot top N features
        plt.figure(figsize=(12, 8))
        top_features = importance_df.head(top_n)
        
        colors = ['red' if coef < 0 else 'blue' for coef in top_features['Coefficient']]
        plt.barh(range(len(top_features)), top_features['Coefficient'], color=colors, alpha=0.7)
        
        plt.yticks(range(len(top_features)), top_features['Feature'])
        plt.xlabel('Coefficient Value')
        plt.title(f'Top {top_n} Feature Importance (Linear Regression Coefficients)')
        plt.grid(True, alpha=0.3)
        
        # Add legend
        import matplotlib.patches as mpatches
        positive_patch = mpatches.Patch(color='blue', alpha=0.7, label='Positive Impact')
        negative_patch = mpatches.Patch(color='red', alpha=0.7, label='Negative Impact')
        plt.legend(handles=[positive_patch, negative_patch])
        
        plt.tight_layout()
        plt.show()
        
        # Print feature importance
        print("\n🔍 Top Feature Importance:")
        for idx, row in top_features.iterrows():
            impact = "increases" if row['Coefficient'] > 0 else "decreases"
            print(f"   • {row['Feature']}: {row['Coefficient']:.4f} ({impact} credit score)")
    
    def save_model(self, filepath=r"C:\FT2\CodeZilla_FT2\Model\saved_models"):
        """Save the trained model"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before saving!")
        
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"baseline_linear_model_{timestamp}.joblib"
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        
        # Save model data
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'training_metrics': self.training_metrics,
            'validation_metrics': self.validation_metrics,
            'test_metrics': self.test_metrics
        }
        
        joblib.dump(model_data, filepath)
        print(f"💾 Model saved to: {filepath}")
        
        return filepath
    
    def load_model(self, filepath):
        """Load a saved model"""
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.training_metrics = model_data.get('training_metrics', {})
        self.validation_metrics = model_data.get('validation_metrics', {})
        self.test_metrics = model_data.get('test_metrics', {})
        self.is_fitted = True
        
        print(f"📂 Model loaded from: {filepath}")

def train_baseline_model():
    """
    Main function to train baseline linear regression model
    """
    print("🚀 Starting Baseline Model Training Pipeline...")
    
    # Initialize preprocessor
    preprocessor = CreditScoreDataPreprocessor()
    
    # Path to dataset
    data_path = r"C:\FT2\CodeZilla_FT2\Model\data\financial_dataset.csv"    
    try:
        print(f"📂 Loading and preprocessing data from: {data_path}")
        
        # Run preprocessing pipeline
        X_train, X_val, X_test, y_train, y_val, y_test, report = preprocessor.preprocess_pipeline(
            csv_path=data_path,
            target_column='credit_score',
            create_interactions=True,
            handle_outliers=False,
            train_size=0.6,
            val_size=0.2,
            test_size=0.2
        )
        
        print(f"✅ Data preprocessing completed!")
        print(f"   • Training set: {X_train.shape}")
        print(f"   • Validation set: {X_val.shape}")
        print(f"   • Test set: {X_test.shape}")
        
        # Check for NaN values in preprocessed data
        print("\n🔍 Checking for NaN values after preprocessing:")
        print(f"   • Training set NaNs: {X_train.isnull().sum().sum()}")
        print(f"   • Validation set NaNs: {X_val.isnull().sum().sum()}")
        print(f"   • Test set NaNs: {X_test.isnull().sum().sum()}")
        
        # If there are NaN values, show which columns
        if X_test.isnull().sum().sum() > 0:
            print("   • NaN columns in test set:")
            nan_cols = X_test.isnull().sum()
            for col, count in nan_cols[nan_cols > 0].items():
                print(f"     - {col}: {count}")
        
        # Initialize and train baseline model
        baseline_model = BaselineLinearModel()
        
        # Train the model
        baseline_model.train(X_train, y_train, X_val, y_val)
        
        # Evaluate on test set
        test_metrics = baseline_model.evaluate(X_test, y_test)
        
        # Show feature importance
        baseline_model.plot_feature_importance(top_n=15)
        
        # Plot feature relationships with target
        print("\n📊 Generating Feature Relationships Visualization...")
        try:
            # Combine train data for relationship analysis
            combined_data = pd.concat([X_train, y_train], axis=1)
            plot_feature_relationships(combined_data, target_col='credit_score')
        except Exception as e:
            print(f"⚠️  Warning: Could not generate feature relationships: {str(e)}")
        
        # Generate comprehensive model evaluation visualizations
        print("\n🎯 Generating Model Evaluation Visualizations...")
        try:
            # Clean test data before passing to visualization
            X_test_clean = X_test.fillna(X_test.median(numeric_only=True))
            
            evaluate_model_performance(
                model=baseline_model.model,
                X_test=X_test_clean,
                y_test=y_test,
                feature_names=list(X_test_clean.columns) if hasattr(X_test_clean, 'columns') else None,
                model_type='regression'
            )
        except Exception as e:
            print(f"⚠️  Warning: Could not generate advanced visualizations: {str(e)}")
        
        # Save the model
        model_path = baseline_model.save_model("../models/baseline_linear_regression.joblib")
        
        print("\n🎉 Baseline model training completed successfully!")
        print(f"📊 Final Test R²: {test_metrics['r2']:.4f}")
        print(f"📊 Final Test RMSE: {test_metrics['rmse']:.2f}")
        
        return baseline_model, test_metrics
        
    except FileNotFoundError:
        print(f"❌ Error: Dataset not found at {data_path}")
        print("Please ensure your CSV file exists or run the data enhancement script first.")
        return None, None
    except Exception as e:
        print(f"❌ Error during model training: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    """
    Main execution block - runs when file is executed directly
    """
    model, metrics = train_baseline_model()
