"""
Data Enhancement Script - Add Target Variables
Adds credit_score and loan_approval columns to financial_dataset.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

def calculate_credit_score(row):
    """
    Calculate credit score (300-850) based on financial indicators
    Higher scores indicate better creditworthiness
    """
    # Base score
    score = 500
    
    # Payment reliability factors (40% weight)
    score += row['rent_on_time_rate'] * 140  # 0-140 points
    score -= row['avg_utility_payment_delay'] * 5  # Penalty for delays
    if not pd.isna(row['loan_repayment_consistency']):
        score += row['loan_repayment_consistency'] * 80  # 0-80 points
    
    # Financial stability factors (30% weight)
    score += min(row['monthly_cashflow'] / 1000, 50)  # Cap at 50 points
    score += row['savings_ratio'] * 100  # 0-100 points
    
    # Credit history (20% weight)
    if row['has_existing_loans']:
        # Having loans can be positive if managed well
        if not pd.isna(row['loan_repayment_consistency']):
            if row['loan_repayment_consistency'] > 0.7:
                score += 30  # Bonus for good loan management
            else:
                score -= 20  # Penalty for poor loan management
        else:
            score -= 10  # Small penalty for unknown loan performance
    
    # Demographics (10% weight)
    # Age stability bonus
    if 25 <= row['age'] <= 55:
        score += 20
    elif row['age'] > 55:
        score += 10
    
    # Education bonus
    if row['education_level'] == 'PG':
        score += 25
    elif row['education_level'] == 'UG':
        score += 15
    
    # Employment stability
    if row['employment_type'] == 'Salaried':
        score += 20
    elif row['employment_type'] == 'Self-employed':
        score += 10
    
    # Digital payment activity bonus
    score += row['digital_payment_activity'] * 20
    
    # Dependents penalty (more dependents = higher risk)
    score -= row['dependents_count'] * 5
    
    # Ensure score is within valid range
    return max(300, min(850, int(score)))

def determine_loan_approval(row):
    """
    Determine loan approval (Yes/No) based on credit score and additional factors
    """
    credit_score = row['credit_score']
    
    # Base approval thresholds
    if credit_score >= 700:
        approval_prob = 0.85
    elif credit_score >= 650:
        approval_prob = 0.70
    elif credit_score >= 600:
        approval_prob = 0.55
    elif credit_score >= 550:
        approval_prob = 0.35
    else:
        approval_prob = 0.15
    
    # Adjust based on additional factors
    
    # Income stability
    if row['monthly_cashflow'] > 25000:
        approval_prob += 0.1
    elif row['monthly_cashflow'] < 10000:
        approval_prob -= 0.1
    
    # Savings ratio
    if row['savings_ratio'] > 0.3:
        approval_prob += 0.05
    elif row['savings_ratio'] < 0.1:
        approval_prob -= 0.05
    
    # Employment type
    if row['employment_type'] == 'Salaried':
        approval_prob += 0.05
    elif row['employment_type'] == 'Unemployed':
        approval_prob -= 0.2
    
    # Existing loan management
    if row['has_existing_loans'] and not pd.isna(row['loan_repayment_consistency']):
        if row['loan_repayment_consistency'] > 0.8:
            approval_prob += 0.05
        elif row['loan_repayment_consistency'] < 0.5:
            approval_prob -= 0.15
    
    # Ensure probability is within bounds
    approval_prob = max(0.05, min(0.95, approval_prob))
    
    # Make random decision based on probability
    return 'Yes' if np.random.rand() < approval_prob else 'No'

def enhance_dataset():
    """
    Main function to enhance the dataset with target variables
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Load the dataset
    data_path = Path("../data/financial_dataset.csv")
    print(f"Loading dataset from: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"Original dataset shape: {df.shape}")
    
    # Handle missing values for calculation purposes
    df_calc = df.copy()
    
    # Fill missing loan_repayment_consistency with median for calculation
    median_consistency = df_calc['loan_repayment_consistency'].median()
    df_calc.loc[:, 'loan_repayment_consistency'] = df_calc['loan_repayment_consistency'].fillna(median_consistency)
    
    # Fill missing education_level with mode
    mode_education = df_calc['education_level'].mode()[0] if not df_calc['education_level'].mode().empty else 'Secondary'
    df_calc.loc[:, 'education_level'] = df_calc['education_level'].fillna(mode_education)
    
    # Calculate credit scores
    print("Calculating credit scores...")
    df['credit_score'] = df_calc.apply(calculate_credit_score, axis=1)
    
    # Add credit score to df_calc for loan approval calculation
    df_calc['credit_score'] = df['credit_score']
    
    # Determine loan approvals
    print("Determining loan approvals...")
    df['loan_approval'] = df_calc.apply(determine_loan_approval, axis=1)
    
    # Display statistics
    print("\n📊 Target Variable Statistics:")
    print(f"Credit Score - Mean: {df['credit_score'].mean():.1f}, Std: {df['credit_score'].std():.1f}")
    print(f"Credit Score Range: {df['credit_score'].min()} - {df['credit_score'].max()}")
    print(f"Loan Approval Distribution:")
    print(df['loan_approval'].value_counts())
    print(f"Loan Approval Rate: {(df['loan_approval'] == 'Yes').mean():.1%}")
    
    # Save enhanced dataset
    output_path = data_path
    df.to_csv(output_path, index=False)
    print(f"\n✅ Enhanced dataset saved to: {output_path}")
    print(f"New dataset shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    print("🚀 Starting dataset enhancement...")
    enhanced_df = enhance_dataset()
    print("✅ Dataset enhancement completed!")
