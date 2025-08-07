"""
Data Visualization Module for Credit Score Prediction
Provides comprehensive visualization functions for EDA and model insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class CreditScoreVisualizer:
    """
    A comprehensive visualization class for credit score data analysis
    """
    
    def __init__(self, figsize=(12, 8)):
        """Initialize the visualizer with default figure size"""
        self.figsize = figsize
        self.categorical_features = ['education_level', 'region_type', 'employment_type', 'loan_approval']
        self.numerical_features = [
            'rent_on_time_rate', 'avg_utility_payment_delay', 'monthly_cashflow',
            'savings_ratio', 'loan_repayment_consistency', 'digital_payment_activity',
            'age', 'dependents_count', 'credit_score'
        ]
        self.boolean_features = ['has_existing_loans']
        self.target_features = ['credit_score', 'loan_approval']
    
    def data_overview(self, df: pd.DataFrame) -> None:
        """
        Display comprehensive data overview
        
        Args:
            df (pd.DataFrame): Input dataframe
        """
        print("="*60)
        print("CREDIT SCORE DATA OVERVIEW")
        print("="*60)
        
        print(f"\nDataset Shape: {df.shape}")
        print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\n📊 DATA TYPES:")
        print(df.dtypes.value_counts())
        
        print("\n🔍 MISSING VALUES:")
        missing_data = df.isnull().sum()
        missing_percent = 100 * missing_data / len(df)
        missing_table = pd.DataFrame({
            'Missing Count': missing_data,
            'Percentage': missing_percent
        })
        missing_table = missing_table[missing_table['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        if not missing_table.empty:
            print(missing_table)
        else:
            print("No missing values found!")
        
        print("\n📈 NUMERICAL FEATURES SUMMARY:")
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            print(df[numerical_cols].describe().round(3))
        
        print("\n📋 CATEGORICAL FEATURES SUMMARY:")
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            print(f"\n{col}:")
            print(df[col].value_counts().head())
    
    def plot_missing_values(self, df: pd.DataFrame) -> None:
        """
        Visualize missing values pattern
        
        Args:
            df (pd.DataFrame): Input dataframe
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Missing values heatmap
        sns.heatmap(df.isnull(), cbar=True, cmap='viridis', ax=axes[0])
        axes[0].set_title('Missing Values Heatmap', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Features')
        axes[0].set_ylabel('Records')
        
        # Missing values bar plot
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        if not missing_data.empty:
            missing_data.plot(kind='bar', ax=axes[1], color='coral')
            axes[1].set_title('Missing Values Count by Feature', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Features')
            axes[1].set_ylabel('Missing Count')
            axes[1].tick_params(axis='x', rotation=45)
        else:
            axes[1].text(0.5, 0.5, 'No Missing Values!', ha='center', va='center', 
                        transform=axes[1].transAxes, fontsize=16)
            axes[1].set_title('Missing Values Status', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def plot_numerical_distributions(self, df: pd.DataFrame, cols: int = 3) -> None:
        """
        Plot distributions of numerical features
        
        Args:
            df (pd.DataFrame): Input dataframe
            cols (int): Number of columns in subplot grid
        """
        numerical_cols = [col for col in self.numerical_features if col in df.columns]
        if not numerical_cols:
            print("No numerical features found to plot.")
            return
        
        rows = (len(numerical_cols) + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        axes = axes.flatten() if rows > 1 else [axes] if rows == 1 else axes
        
        for i, col in enumerate(numerical_cols):
            # Histogram with KDE
            sns.histplot(data=df, x=col, kde=True, ax=axes[i], alpha=0.7)
            axes[i].set_title(f'Distribution of {col}', fontweight='bold')
            axes[i].grid(True, alpha=0.3)
            
            # Add statistics text
            mean_val = df[col].mean()
            median_val = df[col].median()
            axes[i].axvline(mean_val, color='red', linestyle='--', alpha=0.7, label=f'Mean: {mean_val:.3f}')
            axes[i].axvline(median_val, color='green', linestyle='--', alpha=0.7, label=f'Median: {median_val:.3f}')
            axes[i].legend()
        
        # Hide empty subplots
        for i in range(len(numerical_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle('Numerical Features Distribution Analysis', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()
    
    def plot_categorical_distributions(self, df: pd.DataFrame) -> None:
        """
        Plot distributions of categorical features
        
        Args:
            df (pd.DataFrame): Input dataframe
        """
        categorical_cols = [col for col in self.categorical_features + self.boolean_features if col in df.columns]
        if not categorical_cols:
            print("No categorical features found to plot.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        for i, col in enumerate(categorical_cols[:4]):  # Limit to 4 features
            if col in df.columns:
                value_counts = df[col].value_counts()
                
                # Bar plot
                sns.countplot(data=df, x=col, ax=axes[i], order=value_counts.index)
                axes[i].set_title(f'Distribution of {col}', fontweight='bold', fontsize=12)
                axes[i].tick_params(axis='x', rotation=45)
                
                # Add count annotations
                for p in axes[i].patches:
                    axes[i].annotate(f'{int(p.get_height())}', 
                                   (p.get_x() + p.get_width()/2., p.get_height()), 
                                   ha='center', va='bottom', fontweight='bold')
        
        # Hide unused subplots
        for i in range(len(categorical_cols), 4):
            axes[i].set_visible(False)
        
        plt.suptitle('Categorical Features Distribution Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_target_analysis(self, df: pd.DataFrame) -> None:
        """
        Analyze target variables: credit_score and loan_approval
        
        Args:
            df (pd.DataFrame): Input dataframe with target columns
        """
        if 'credit_score' not in df.columns and 'loan_approval' not in df.columns:
            print("No target variables (credit_score, loan_approval) found in the dataset.")
            return
        
        # Create subplot structure
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Target Variables Analysis', fontsize=16, fontweight='bold')
        
        # Credit Score Analysis
        if 'credit_score' in df.columns:
            # Credit score distribution
            axes[0, 0].hist(df['credit_score'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0, 0].axvline(df['credit_score'].mean(), color='red', linestyle='--', 
                              label=f'Mean: {df["credit_score"].mean():.0f}')
            axes[0, 0].set_title('Credit Score Distribution')
            axes[0, 0].set_xlabel('Credit Score')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].legend()
            
            # Credit score by employment type
            if 'employment_type' in df.columns:
                df.boxplot(column='credit_score', by='employment_type', ax=axes[0, 1])
                axes[0, 1].set_title('Credit Score by Employment Type')
                axes[0, 1].set_xlabel('Employment Type')
                axes[0, 1].set_ylabel('Credit Score')
            
            # Credit score vs monthly cashflow
            if 'monthly_cashflow' in df.columns:
                axes[0, 2].scatter(df['monthly_cashflow'], df['credit_score'], alpha=0.6, color='green')
                axes[0, 2].set_title('Credit Score vs Monthly Cashflow')
                axes[0, 2].set_xlabel('Monthly Cashflow')
                axes[0, 2].set_ylabel('Credit Score')
        
        # Loan Approval Analysis
        if 'loan_approval' in df.columns:
            # Loan approval distribution
            approval_counts = df['loan_approval'].value_counts()
            axes[1, 0].pie(approval_counts.values, labels=approval_counts.index, autopct='%1.1f%%', 
                          colors=['lightcoral', 'lightgreen'])
            axes[1, 0].set_title('Loan Approval Distribution')
            
            # Loan approval by education level
            if 'education_level' in df.columns:
                approval_by_education = pd.crosstab(df['education_level'], df['loan_approval'])
                approval_by_education.plot(kind='bar', ax=axes[1, 1], color=['lightcoral', 'lightgreen'])
                axes[1, 1].set_title('Loan Approval by Education Level')
                axes[1, 1].set_xlabel('Education Level')
                axes[1, 1].set_ylabel('Count')
                axes[1, 1].legend(title='Loan Approval')
                axes[1, 1].tick_params(axis='x', rotation=45)
            
            # Credit score vs loan approval
            if 'credit_score' in df.columns:
                approved = df[df['loan_approval'] == 'Yes']['credit_score']
                rejected = df[df['loan_approval'] == 'No']['credit_score']
                
                axes[1, 2].hist([approved, rejected], bins=30, alpha=0.7, 
                               label=['Approved', 'Rejected'], color=['lightgreen', 'lightcoral'])
                axes[1, 2].set_title('Credit Score Distribution by Loan Approval')
                axes[1, 2].set_xlabel('Credit Score')
                axes[1, 2].set_ylabel('Frequency')
                axes[1, 2].legend()
        
        # Hide unused subplots
        for i in range(2):
            for j in range(3):
                if not axes[i, j].has_data():
                    axes[i, j].set_visible(False)
        
        plt.tight_layout()
        plt.show()
    
    def plot_correlation_matrix(self, df: pd.DataFrame, method: str = 'pearson') -> None:
        """
        Plot correlation matrix for numerical features
        
        Args:
            df (pd.DataFrame): Input dataframe
            method (str): Correlation method ('pearson', 'spearman', 'kendall')
        """
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) < 2:
            print("Not enough numerical features for correlation analysis.")
            return
        
        # Calculate correlation matrix
        corr_matrix = df[numerical_cols].corr(method=method)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Generate heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=.5, ax=ax, fmt='.3f')
        
        ax.set_title(f'Feature Correlation Matrix ({method.title()})', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # Print highly correlated pairs
        print(f"\n🔗 HIGHLY CORRELATED FEATURES (|r| > 0.7):")
        high_corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.7:
                    high_corr_pairs.append({
                        'Feature 1': corr_matrix.columns[i],
                        'Feature 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
        
        if high_corr_pairs:
            for pair in high_corr_pairs:
                print(f"{pair['Feature 1']} ↔ {pair['Feature 2']}: {pair['Correlation']:.3f}")
        else:
            print("No highly correlated features found.")
    
    def plot_outliers_analysis(self, df: pd.DataFrame) -> None:
        """
        Analyze and visualize outliers in numerical features
        
        Args:
            df (pd.DataFrame): Input dataframe
        """
        numerical_cols = [col for col in self.numerical_features if col in df.columns]
        if not numerical_cols:
            print("No numerical features found for outlier analysis.")
            return
        
        rows = (len(numerical_cols) + 2) // 3
        fig, axes = plt.subplots(rows, 3, figsize=(18, 6*rows))
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
        
        for i, col in enumerate(numerical_cols):
            # Box plot for outlier detection
            sns.boxplot(y=df[col], ax=axes[i])
            axes[i].set_title(f'Outliers in {col}', fontweight='bold')
            axes[i].grid(True, alpha=0.3)
            
            # Calculate and display outlier statistics
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
            outlier_count = len(outliers)
            outlier_percentage = (outlier_count / len(df)) * 100
            
            axes[i].text(0.02, 0.98, f'Outliers: {outlier_count} ({outlier_percentage:.1f}%)',
                        transform=axes[i].transAxes, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Hide empty subplots
        for i in range(len(numerical_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle('Outlier Analysis for Numerical Features', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_feature_relationships(self, df: pd.DataFrame, target_col: str = None) -> None:
        """
        Plot relationships between features and target (if provided)
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_col (str): Target column name
        """
        if target_col and target_col not in df.columns:
            print(f"Target column '{target_col}' not found in dataframe.")
            return
        
        numerical_cols = [col for col in self.numerical_features if col in df.columns]
        
        if target_col:
            # Scatter plots against target
            rows = (len(numerical_cols) + 2) // 3
            fig, axes = plt.subplots(rows, 3, figsize=(18, 6*rows))
            axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
            
            for i, col in enumerate(numerical_cols):
                if col != target_col:
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
        else:
            # Pairplot for feature relationships
            if len(numerical_cols) <= 8:  # Limit to avoid overcrowding
                sns.pairplot(df[numerical_cols], diag_kind='kde', height=2)
                plt.suptitle('Feature Relationships Matrix', fontsize=16, fontweight='bold', y=1.02)
                plt.show()
            else:
                print("Too many features for pairplot. Use correlation matrix instead.")
    
    def visualize_all(self, df: pd.DataFrame, target_col: str = None) -> None:
        """
        Run all visualization functions in sequence
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_col (str): Target column name
        """
        print("🎨 Starting comprehensive data visualization...")
        
        # Data overview
        self.data_overview(df)
        
        # Missing values
        self.plot_missing_values(df)
        
        # Distributions
        self.plot_numerical_distributions(df)
        self.plot_categorical_distributions(df)
        
        # Target variable analysis
        self.plot_target_analysis(df)
        
        # Correlation analysis
        self.plot_correlation_matrix(df)
        
        # Outlier analysis
        self.plot_outliers_analysis(df)
        
        # Feature relationships
        self.plot_feature_relationships(df, target_col)
        
        print("✅ Visualization complete!")

def visualize_financial_data(df: pd.DataFrame, target_col: str = 'credit_score') -> None:
    """
    Main function to visualize financial dataset with target variables
    
    Args:
        df (pd.DataFrame): Financial dataset with credit_score and loan_approval columns
        target_col (str): Primary target column name (default: 'credit_score')
    """
    visualizer = CreditScoreVisualizer()
    visualizer.visualize_all(df, target_col=target_col)

if __name__ == "__main__":
    """
    Main execution block - runs when file is executed directly
    """
    print("🎨 Starting Financial Data Visualization...")
    
    # Load the enhanced dataset
    data_path = r"..\data\financial_dataset.csv"
    
    try:
        print(f"📂 Loading data from: {data_path}")
        df = pd.read_csv(data_path)
        
        print(f"✅ Data loaded successfully! Shape: {df.shape}")
        print(f"📊 Columns: {list(df.columns)}")
        
        # Run comprehensive visualization
        visualize_financial_data(df, target_col='credit_score')
        
        print("\n🎉 Visualization completed! Check the generated plots.")
        
    except FileNotFoundError:
        print(f"❌ Error: Dataset not found at {data_path}")
        print("Please ensure your CSV file exists or run the preprocessing script first.")
    except Exception as e:
        print(f"❌ Error during visualization: {str(e)}")
        print("Check your data format and dependencies.")
