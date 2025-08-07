"""
Credit Invisibility Dataset Generator for American Citizens
Generates comprehensive alternative credit data for people without traditional credit history
"""

import pandas as pd
import numpy as np
from pathlib import Path
import random
from datetime import datetime, timedelta

def generate_credit_invisibility_dataset(n_samples=3000):
    """
    Generate comprehensive dataset for credit invisibility using alternative data
    Ensures balanced representation across all demographic and financial segments
    """
    np.random.seed(42)
    random.seed(42)
    
    print("🏗️ Generating Credit Invisibility Dataset for American Citizens...")
    
    # Define demographic segments for balanced sampling
    age_segments = ['young_adult', 'mid_career', 'established', 'mature']  # 18-25, 26-35, 36-50, 51-65
    income_segments = ['low', 'lower_middle', 'middle', 'upper_middle', 'high']
    housing_segments = ['low_rent', 'medium_rent', 'high_rent']
    employment_segments = ['gig', 'part_time', 'full_time', 'self_employed', 'unemployed']
    education_segments = ['high_school', 'some_college', 'bachelors', 'graduate']
    
    # Calculate samples per combination to ensure balanced representation
    total_combinations = len(age_segments) * len(income_segments) * len(housing_segments) * len(employment_segments)
    base_samples = max(1, n_samples // total_combinations)
    
    data = []
    
    for age_seg in age_segments:
        for income_seg in income_segments:
            for housing_seg in housing_segments:
                for employment_seg in employment_segments:
                    # Generate multiple samples for each combination
                    for _ in range(base_samples + random.randint(0, 2)):  # Add some variation
                        sample = generate_individual_profile(age_seg, income_seg, housing_seg, employment_seg, education_segments)
                        data.append(sample)
    
    # Add additional random samples to reach target
    while len(data) < n_samples:
        age_seg = random.choice(age_segments)
        income_seg = random.choice(income_segments)
        housing_seg = random.choice(housing_segments)
        employment_seg = random.choice(employment_segments)
        sample = generate_individual_profile(age_seg, income_seg, housing_seg, employment_seg, education_segments)
        data.append(sample)
    
    # Trim to exact target if we exceeded
    data = data[:n_samples]
    
    df = pd.DataFrame(data)
    return df

def generate_individual_profile(age_seg, income_seg, housing_seg, employment_seg, education_segments):
    """Generate individual profile based on segment characteristics"""
    
    # Age generation
    age_ranges = {
        'young_adult': (18, 25),
        'mid_career': (26, 35), 
        'established': (36, 50),
        'mature': (51, 65)
    }
    age = random.randint(*age_ranges[age_seg])
    
    # Income generation (monthly gross)
    income_ranges = {
        'low': (1800, 3500),
        'lower_middle': (3500, 5500),
        'middle': (5500, 8500),
        'upper_middle': (8500, 15000),
        'high': (15000, 30000)
    }
    monthly_income = random.randint(*income_ranges[income_seg])
    
    # Rent generation
    rent_ranges = {
        'low_rent': (400, 1200),
        'medium_rent': (1200, 2500),
        'high_rent': (2500, 5000)
    }
    monthly_rent = random.randint(*rent_ranges[housing_seg])
    
    # Ensure rent doesn't exceed reasonable income percentage
    max_rent = monthly_income * 0.5  # Cap at 50% of income
    monthly_rent = min(monthly_rent, int(max_rent))
    
    # Employment type
    employment_type = employment_seg
    
    # Education
    education_level = random.choice(education_segments)
    
    # Location (US states with different cost of living)
    us_states = ['CA', 'NY', 'TX', 'FL', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI', 'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
    state = random.choice(us_states)
    
    # Generate correlated financial behaviors
    
    # Rent payment consistency (higher income = more consistent)
    base_rent_consistency = 0.7 + (income_seg == 'high') * 0.2 + (income_seg == 'upper_middle') * 0.15
    rent_payment_consistency = min(1.0, max(0.3, base_rent_consistency + random.uniform(-0.2, 0.2)))
    
    # Utility payment consistency
    utility_payment_consistency = min(1.0, max(0.4, rent_payment_consistency + random.uniform(-0.15, 0.15)))
    
    # Monthly cashflow after fixed expenses
    fixed_expenses = monthly_rent + random.randint(200, 800)  # utilities, insurance, etc.
    monthly_cashflow = max(0, monthly_income - fixed_expenses + random.randint(-500, 500))
    
    # Subscription payment behavior (Netflix, Spotify, gym, etc.)
    num_subscriptions = random.randint(0, 8)
    subscription_payment_consistency = min(1.0, max(0.5, 0.8 + random.uniform(-0.3, 0.2)))
    
    # Bank balance patterns
    income_factor = {'low': 0.1, 'lower_middle': 0.15, 'middle': 0.2, 'upper_middle': 0.25, 'high': 0.3}[income_seg]
    minimum_bank_balance = max(50, int(monthly_income * income_factor * random.uniform(0.5, 1.5)))
    
    # Savings behavior
    savings_rate = max(0.0, min(0.4, income_factor + random.uniform(-0.1, 0.15)))
    monthly_savings = int(monthly_cashflow * savings_rate)
    
    # Savings goal completion rate
    savings_goal_completion_rate = min(1.0, max(0.0, savings_rate * 2 + random.uniform(-0.3, 0.3)))
    
    # P2P transfer patterns (Venmo, Zelle, etc.)
    p2p_monthly_volume = random.randint(0, min(2000, int(monthly_cashflow * 0.3)))
    
    # Risky P2P behavior (gambling, unverified users, etc.)
    base_risky_p2p = 0.1 if age_seg in ['mature', 'established'] else 0.2
    risky_p2p_ratio = max(0.0, min(0.6, base_risky_p2p + random.uniform(-0.1, 0.2)))
    
    # Phone bill payment consistency
    phone_payment_consistency = min(1.0, max(0.6, utility_payment_consistency + random.uniform(-0.1, 0.1)))
    
    # Employment stability (months in current job)
    employment_stability_months = generate_employment_stability(employment_seg, age_seg)
    
    # Insurance payment consistency
    insurance_payment_consistency = min(1.0, max(0.5, rent_payment_consistency + random.uniform(-0.2, 0.2)))
    
    # Overdraft frequency (lower income = higher risk)
    income_protection = {'low': 0, 'lower_middle': 0.1, 'middle': 0.2, 'upper_middle': 0.3, 'high': 0.4}[income_seg]
    monthly_overdrafts = max(0, int((0.3 - income_protection) * 10 * random.uniform(0.5, 1.5)))
    
    # Create profile dictionary
    profile = {
        'age': age,
        'state': state,
        'education_level': education_level,
        'employment_type': employment_type,
        'employment_stability_months': employment_stability_months,
        'monthly_income': monthly_income,
        'monthly_rent': monthly_rent,
        'monthly_cashflow': monthly_cashflow,
        'rent_payment_consistency': round(rent_payment_consistency, 3),
        'utility_payment_consistency': round(utility_payment_consistency, 3),
        'phone_payment_consistency': round(phone_payment_consistency, 3),
        'insurance_payment_consistency': round(insurance_payment_consistency, 3),
        'num_subscriptions': num_subscriptions,
        'subscription_payment_consistency': round(subscription_payment_consistency, 3),
        'minimum_bank_balance': minimum_bank_balance,
        'monthly_savings': monthly_savings,
        'savings_goal_completion_rate': round(savings_goal_completion_rate, 3),
        'p2p_monthly_volume': p2p_monthly_volume,
        'risky_p2p_ratio': round(risky_p2p_ratio, 3),
        'monthly_overdrafts': monthly_overdrafts
    }
    
    return profile

def generate_employment_stability(employment_seg, age_seg):
    """Generate employment stability in months"""
    base_ranges = {
        'unemployed': (0, 2),
        'gig': (1, 8),
        'part_time': (2, 18),
        'full_time': (6, 48),
        'self_employed': (3, 36)
    }
    
    age_multiplier = {
        'young_adult': 0.7,
        'mid_career': 1.0,
        'established': 1.3,
        'mature': 1.5
    }
    
    base_min, base_max = base_ranges[employment_seg]
    multiplier = age_multiplier[age_seg]
    
    min_months = int(base_min * multiplier)
    max_months = int(base_max * multiplier)
    
    return random.randint(min_months, max_months)

def calculate_alternative_credit_score(row):
    """
    Calculate realistic credit score (300-850) for credit invisible Americans
    Based on research: credit invisible typically score 500-650, with most in 540-620 range
    """
    # Base score for credit invisible Americans (lower than traditional credit users)
    score = 520  # Realistic base for credit invisible population
    
    # Payment consistency factors (most important for alternative scoring)
    payment_avg = (
        row['rent_payment_consistency'] * 0.35 +  # Rent is most important
        row['utility_payment_consistency'] * 0.25 +
        row['phone_payment_consistency'] * 0.2 +
        row['insurance_payment_consistency'] * 0.15 +
        row['subscription_payment_consistency'] * 0.05
    )
    
    # Convert payment consistency (0-1) to score impact (-40 to +80)
    score += int((payment_avg - 0.5) * 160)  # Range: -80 to +80
    
    # Financial stability (income-to-expenses ratio)
    if row['monthly_income'] > 0:
        essential_expenses = row['monthly_rent'] + 400  # rent + utilities/food estimate
        disposable_ratio = (row['monthly_income'] - essential_expenses) / row['monthly_income']
        
        if disposable_ratio > 0.3:  # >30% disposable income
            score += 25
        elif disposable_ratio > 0.15:  # >15% disposable income  
            score += 15
        elif disposable_ratio < -0.1:  # Spending more than earning
            score -= 35
        elif disposable_ratio < 0.05:  # Very tight budget
            score -= 15
    
    # Savings and banking behavior
    savings_score = row['savings_goal_completion_rate'] * 30  # 0-30 points
    score += int(savings_score)
    
    # Bank balance stability
    if row['minimum_bank_balance'] > 1500:
        score += 20
    elif row['minimum_bank_balance'] > 500:
        score += 10
    elif row['minimum_bank_balance'] < 50:
        score -= 25
    
    # Risk factors (negative impacts)
    overdraft_penalty = min(row['monthly_overdrafts'] * 8, 40)  # Cap at -40
    p2p_risk_penalty = row['risky_p2p_ratio'] * 35  # 0-35 penalty
    score -= int(overdraft_penalty + p2p_risk_penalty)
    
    # Employment stability (crucial for credit invisible)
    if row['employment_stability_months'] > 36:
        score += 20
    elif row['employment_stability_months'] > 12:
        score += 10
    elif row['employment_stability_months'] < 6:
        score -= 25
    
    # Employment type impact
    employment_adjustments = {
        'full_time': 15,
        'part_time': 0,
        'self_employed': -10,  # Higher risk perception
        'gig': -15,           # Inconsistent income
        'unemployed': -30
    }
    score += employment_adjustments.get(row['employment_type'], 0)
    
    # Age factor (limited impact for credit invisible)
    if row['age'] >= 35:
        score += 8
    elif row['age'] >= 25:
        score += 5
    elif row['age'] < 21:
        score -= 10  # Very young, limited financial history
    
    # Education (minimal impact for alternative scoring)
    education_bonus = {
        'high_school': 0,
        'some_college': 3,
        'bachelors': 8,
        'graduate': 12
    }
    score += education_bonus.get(row['education_level'], 0)
    
    # Add some realistic randomness (±5 points) to avoid perfect patterns
    random_adjustment = random.randint(-5, 5)
    score += random_adjustment
    
    # Realistic score range for credit invisible Americans
    # Most should be in 540-650 range, very few above 700
    final_score = max(480, min(750, int(score)))
    
    # Apply realistic distribution constraints
    # Only 5% should score above 680, 10% below 520
    if final_score > 680:
        if random.random() > 0.05:  # 95% chance to cap it
            final_score = random.randint(620, 680)
    elif final_score < 520:
        if random.random() > 0.10:  # 90% chance to raise it
            final_score = random.randint(520, 580)
    
    return final_score

def calculate_loan_approval(row):
    """
    Calculate realistic loan approval for credit invisible Americans
    Based on alternative data and more stringent criteria
    """
    credit_score = row['credit_score']
    
    # Base approval probability (more conservative for credit invisible)
    if credit_score >= 700:
        approval_prob = 0.85  # Even high scores face some challenges
    elif credit_score >= 660:
        approval_prob = 0.70
    elif credit_score >= 620:
        approval_prob = 0.55
    elif credit_score >= 580:
        approval_prob = 0.40
    elif credit_score >= 540:
        approval_prob = 0.25
    elif credit_score >= 500:
        approval_prob = 0.15
    else:
        approval_prob = 0.08
    
    # Adjust based on additional factors specific to credit invisible population
    
    # Employment stability is crucial
    if row['employment_stability_months'] > 24:
        approval_prob += 0.10
    elif row['employment_stability_months'] > 12:
        approval_prob += 0.05
    elif row['employment_stability_months'] < 6:
        approval_prob -= 0.15
    
    # Employment type matters more for credit invisible
    employment_adjustments = {
        'full_time': 0.08,
        'part_time': -0.05,
        'self_employed': -0.12,  # Harder to verify income
        'gig': -0.15,            # Inconsistent income
        'unemployed': -0.25
    }
    approval_prob += employment_adjustments.get(row['employment_type'], 0)
    
    # Income stability
    if row['monthly_income'] > 0:
        debt_to_income_ratio = (row['monthly_rent'] * 12) / (row['monthly_income'] * 12)
        if debt_to_income_ratio > 0.4:  # High rent burden
            approval_prob -= 0.10
        elif debt_to_income_ratio < 0.25:  # Low rent burden
            approval_prob += 0.05
    
    # Banking relationship and stability
    if row['minimum_bank_balance'] > 1000:
        approval_prob += 0.08
    elif row['minimum_bank_balance'] < 100:
        approval_prob -= 0.12
    
    # Payment history is critical for credit invisible
    payment_avg = (
        row['rent_payment_consistency'] * 0.4 +
        row['utility_payment_consistency'] * 0.3 +
        row['phone_payment_consistency'] * 0.2 +
        row['insurance_payment_consistency'] * 0.1
    )
    
    if payment_avg > 0.85:
        approval_prob += 0.12
    elif payment_avg > 0.70:
        approval_prob += 0.06
    elif payment_avg < 0.50:
        approval_prob -= 0.15
    
    # Risk factors
    if row['monthly_overdrafts'] > 2:
        approval_prob -= 0.15
    elif row['monthly_overdrafts'] > 0:
        approval_prob -= 0.08
    
    if row['risky_p2p_ratio'] > 0.3:
        approval_prob -= 0.12
    
    # Age factor (limited experience vs stability)
    if row['age'] < 22:
        approval_prob -= 0.08  # Limited financial history
    elif row['age'] > 40:
        approval_prob += 0.03  # More stable
    
    # Cap probabilities
    approval_prob = max(0.02, min(0.92, approval_prob))
    
    # Generate final decision
    return "Yes" if random.random() < approval_prob else "No"
    
    # Income stability
    if row['monthly_income'] > 8000:
        approval_prob += 0.08
    elif row['monthly_income'] > 5000:
        approval_prob += 0.05
    elif row['monthly_income'] < 2500:
        approval_prob -= 0.10
    
    # Employment type
    employment_adjustments = {
        'full_time': 0.08,
        'self_employed': 0.03,
        'part_time': -0.05,
        'gig': -0.10,
        'unemployed': -0.25
    }
    approval_prob += employment_adjustments.get(row['employment_type'], 0)
    
    # Financial behavior
    if row['monthly_overdrafts'] == 0:
        approval_prob += 0.05
    elif row['monthly_overdrafts'] > 2:
        approval_prob -= 0.10
    
    if row['savings_goal_completion_rate'] > 0.7:
        approval_prob += 0.05
    
    # Ensure probability bounds
    approval_prob = max(0.05, min(0.95, approval_prob))
    
    return 'Yes' if np.random.rand() < approval_prob else 'No'

def create_credit_invisibility_dataset():
    """Main function to create the complete dataset"""
    print("🚀 Creating Credit Invisibility Dataset for American Citizens...")
    
    # Generate base dataset
    df = generate_credit_invisibility_dataset(n_samples=3000)
    
    print(f"✅ Generated {len(df)} individual profiles")
    
    # Calculate credit scores
    print("📊 Calculating alternative credit scores...")
    df['credit_score'] = df.apply(calculate_alternative_credit_score, axis=1)
    
    # Calculate loan approvals
    print("🏦 Determining loan approvals...")
    np.random.seed(42)  # For reproducible loan decisions
    df['loan_approval'] = df.apply(calculate_loan_approval, axis=1)
    
    # Display statistics
    print("\n📈 Dataset Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Credit Score - Mean: {df['credit_score'].mean():.1f}, Std: {df['credit_score'].std():.1f}")
    print(f"Credit Score Range: {df['credit_score'].min()} - {df['credit_score'].max()}")
    print(f"Loan Approval Distribution:")
    print(df['loan_approval'].value_counts())
    print(f"Loan Approval Rate: {(df['loan_approval'] == 'Yes').mean():.1%}")
    
    # Show demographic balance
    print(f"\n👥 Demographic Balance:")
    print(f"Age distribution: {df.groupby(pd.cut(df['age'], bins=[17, 25, 35, 50, 65])).size()}")
    print(f"Income distribution: {df.groupby(pd.cut(df['monthly_income'], bins=[0, 3500, 5500, 8500, 15000, 50000])).size()}")
    print(f"Employment types: {df['employment_type'].value_counts()}")
    
    return df

if __name__ == "__main__":
    # Create dataset
    dataset = create_credit_invisibility_dataset()
    
    # Save to CSV
    output_path = Path(r"C:\FT2\CodeZilla_FT2\Model\data\credit_invisibility_dataset.csv")
    dataset.to_csv(output_path, index=False)
    
    print(f"\n💾 Dataset saved to: {output_path}")
    print(f"📊 Final dataset shape: {dataset.shape}")
    print("\n🎉 Credit Invisibility Dataset generation completed!")
