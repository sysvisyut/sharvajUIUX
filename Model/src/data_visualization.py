"""
Streamlined Data Visualization Module for Credit Score Prediction
Contains only: Feature relationships, Confusion matrix, Prediction vs actual values, Training curves
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class StreamlinedVisualizer:
    """
    Streamlined visualization class containing only required plots:
    - Feature relationships
    - Confusion matrix 
    - Prediction vs actual values
    - Training accuracy and loss curves
    """
    
    def __init__(self, figsize=(12, 8)):
        """Initialize the visualizer with default figure size"""
        self.figsize = figsize
        # Define common numerical and categorical features for financial data
        self.numerical_features = ['age', 'annual_income', 'monthly_cashflow', 'debt_to_income_ratio',
                                 'num_bank_accounts', 'num_credit_cards', 'interest_rate',
                                 'num_of_loans', 'num_of_delayed_payment', 'changed_credit_limit',
                                 'num_credit_inquiries', 'credit_mix', 'outstanding_debt',
                                 'credit_utilization_ratio', 'payment_of_min_amount',
                                 'total_emi_per_month', 'amount_invested_monthly', 'payment_behaviour',
                                 'monthly_balance', 'credit_score']
    
    def plot_feature_relationships(self, df: pd.DataFrame, target_col: str = 'credit_score') -> None:
        """
        Plot relationships between numerical features and target variable
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_col (str): Target column name
        """
        if target_col and target_col not in df.columns:
            print(f"Target column '{target_col}' not found in dataframe.")
            return
        
        numerical_cols = [col for col in self.numerical_features if col in df.columns and col != target_col]
        
        if not numerical_cols:
            print("No numerical features found for relationship analysis.")
            return
        
        # Scatter plots against target
        rows = (len(numerical_cols) + 2) // 3
        fig, axes = plt.subplots(rows, 3, figsize=(18, 6*rows))
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
        
        for i, col in enumerate(numerical_cols):
            axes[i].scatter(df[col], df[target_col], alpha=0.6, s=30)
            axes[i].set_xlabel(col)
            axes[i].set_ylabel(target_col)
            axes[i].set_title(f'{col} vs {target_col}', fontweight='bold')
            axes[i].grid(True, alpha=0.3)
            
            # Add correlation coefficient
            if df[col].dtype in [np.number] and df[target_col].dtype in [np.number]:
                corr_coef = df[col].corr(df[target_col])
                axes[i].text(0.05, 0.95, f'r = {corr_coef:.3f}',
                           transform=axes[i].transAxes, fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # Hide empty subplots
        for i in range(len(numerical_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle(f'Feature Relationships with {target_col}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_confusion_matrix(self, y_true, y_pred, classes=None, title="Confusion Matrix"):
        """
        Plot confusion matrix for classification problems
        """
        cm = confusion_matrix(y_true, y_pred)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                   xticklabels=classes if classes else ['No', 'Yes'],
                   yticklabels=classes if classes else ['No', 'Yes'])
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Predicted Label', fontsize=12)
        ax.set_ylabel('True Label', fontsize=12)
        
        accuracy = np.trace(cm) / np.sum(cm)
        ax.text(0.02, 0.98, f'Accuracy: {accuracy:.3f}', 
                transform=ax.transAxes, fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
                verticalalignment='top')
        
        plt.tight_layout()
        plt.show()
        return cm
    
    def plot_prediction_vs_actual(self, y_true, y_pred, title="Predictions vs Actual Values"):
        """
        Plot predicted vs actual values for regression problems
        """
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        # Scatter plot
        ax.scatter(y_true, y_pred, alpha=0.6, s=30, color='steelblue')
        
        # Perfect prediction line
        min_val = min(min(y_true), min(y_pred))
        max_val = max(max(y_true), max(y_pred))
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        ax.set_xlabel('Actual Values', fontsize=12)
        ax.set_ylabel('Predicted Values', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Calculate and display metrics
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(mse)
        
        metrics_text = f'R² = {r2:.3f}\nRMSE = {rmse:.3f}\nMAE = {mae:.3f}'
        ax.text(0.05, 0.95, metrics_text, transform=ax.transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
                verticalalignment='top')
        
        plt.tight_layout()
        plt.show()
        
        return {'MSE': mse, 'MAE': mae, 'R2': r2, 'RMSE': rmse}
    
    def plot_training_history(self, train_scores, val_scores, metric_name="Loss", 
                            train_accuracies=None, val_accuracies=None):
        """
        Plot training and validation loss/accuracy curves
        """
        if train_accuracies is not None and val_accuracies is not None:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        else:
            fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
            ax2 = None
        
        # Plot loss/metric
        epochs = range(1, len(train_scores) + 1)
        ax1.plot(epochs, train_scores, 'bo-', label=f'Training {metric_name}', linewidth=2)
        ax1.plot(epochs, val_scores, 'ro-', label=f'Validation {metric_name}', linewidth=2)
        ax1.set_xlabel('Epochs', fontsize=12)
        ax1.set_ylabel(metric_name, fontsize=12)
        ax1.set_title(f'Training and Validation {metric_name}', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot accuracy if provided
        if ax2 is not None:
            ax2.plot(epochs, train_accuracies, 'bo-', label='Training Accuracy', linewidth=2)
            ax2.plot(epochs, val_accuracies, 'ro-', label='Validation Accuracy', linewidth=2)
            ax2.set_xlabel('Epochs', fontsize=12)
            ax2.set_ylabel('Accuracy', fontsize=12)
            ax2.set_title('Training and Validation Accuracy', fontsize=14, fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def evaluate_model_performance(model, X_test, y_test, feature_names=None, 
                             train_history=None, model_type='regression'):
    """
    Main function to evaluate model performance with streamlined visualizations
    
    Args:
        model: Trained model object
        X_test: Test features
        y_test: Test labels
        feature_names: List of feature names (optional)
        train_history: Training history dict with keys: 'train_loss', 'val_loss', 'train_accuracy', 'val_accuracy'
        model_type: 'regression' or 'classification'
    """
    visualizer = StreamlinedVisualizer()
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    print("🔍 Generating Streamlined Model Evaluation Plots...")
    
    # Check if classification or regression
    unique_true = np.unique(y_test)
    is_classification = len(unique_true) <= 10 and all(isinstance(x, (int, str)) for x in unique_true)
    
    if is_classification:
        print("\n📊 Classification Model Evaluation:")
        visualizer.plot_confusion_matrix(y_test, y_pred, title="Confusion Matrix")
        print("\n📋 Classification Report:")
        print(classification_report(y_test, y_pred))
    else:
        print("\n📊 Regression Model Evaluation:")
        metrics = visualizer.plot_prediction_vs_actual(y_test, y_pred, "Credit Score Predictions vs Actual")
        print(f"\n📋 Regression Metrics:")
        for metric, value in metrics.items():
            print(f"   • {metric}: {value:.4f}")
    
    # Plot training history if provided
    if train_history is not None:
        if 'train_loss' in train_history and 'val_loss' in train_history:
            train_acc = train_history.get('train_accuracy')
            val_acc = train_history.get('val_accuracy')
            visualizer.plot_training_history(
                train_history['train_loss'], 
                train_history['val_loss'],
                'Loss',
                train_acc,
                val_acc
            )
    
    print("\n✅ Model evaluation completed!")

def plot_feature_relationships(df: pd.DataFrame, target_col: str = 'credit_score') -> None:
    """
    Standalone function to plot feature relationships
    
    Args:
        df (pd.DataFrame): Input dataframe
        target_col (str): Target column name
    """
    visualizer = StreamlinedVisualizer()
    visualizer.plot_feature_relationships(df, target_col)

if __name__ == "__main__":
    """
    Main execution block
    """
    print("🎯 Streamlined Data Visualization Module")
    print("Available visualizations:")
    print("   • Feature Relationships")
    print("   • Confusion Matrix (for classification)")
    print("   • Predictions vs Actual Values (for regression)")  
    print("   • Training/Validation Loss and Accuracy Curves")
    print("\nUse the respective functions to generate these plots.")

    # Example: Visualize feature relationships if run directly
    try:
        # Try to load a sample dataset from the typical location
        df = pd.read_csv(r"C:\FT2\CodeZilla_FT2\Model\data\financial_dataset.csv")
        print(f"\nLoaded sample data with shape: {df.shape}")
        plot_feature_relationships(df, target_col="credit_score")
    except Exception as e:
        print(f"\n[INFO] Could not load sample data for visualization: {e}")
