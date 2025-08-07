"""
Simple Credit Score Predictor
Interactive script that loads the trained XGBoost model and predicts credit scores
based on user input
"""

import joblib
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class CreditScorePredictor:
    """
    Simple credit score predictor using the trained XGBoost model
    """
    
    def __init__(self):
        """Initialize the predictor by loading the saved model"""
        self.model_path = "../models/xgboost_credit_score_model_final.joblib"
        self.model = None
        self.feature_names = None
        self.load_model()
    
    def load_model(self):
        """Load the trained XGBoost model"""
        try:
            print("🔄 Loading trained XGBoost model...")
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            print(f"✅ Model loaded successfully!")
        except FileNotFoundError:
            print(f"❌ Error: Model file not found at {self.model_path}")
            print("Please train the XGBoost model first by running xgboost_final.py")
            exit(1)
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            exit(1)
    
    def get_user_input(self):
        """
        Collect user input for all required features
        """
        print("\n" + "="*60)
        print("🎯 CREDIT SCORE PREDICTOR - INPUT YOUR INFORMATION")
        print("="*60)
        
        user_data = {}
        
        # Get basic information
        print("\n📝 Please enter your information:")
        
        user_data['age'] = int(input("Age (18-80): "))
        user_data['state'] = input("State (e.g., CA, NY, TX): ").upper()
        
        # Education level
        print("\nEducation options: high_school, some_college, bachelors, masters, doctorate")
        user_data['education_level'] = input("Education level: ").lower()
        
        # Employment type
        print("\nEmployment options: full_time, part_time, self_employed, unemployed, student, retired")
        user_data['employment_type'] = input("Employment type: ").lower()
        
        user_data['monthly_income'] = int(input("Monthly income ($): "))
        user_data['monthly_housing_cost'] = int(input("Monthly housing cost ($): "))
        user_data['num_dependents'] = int(input("Number of dependents: "))
        user_data['years_current_job'] = int(input("Years at current job: "))
        user_data['num_credit_cards'] = int(input("Number of credit cards: "))
        
        # Boolean inputs
        user_data['has_student_loan'] = input("Have student loan? (yes/no): ").lower() == 'yes'
        user_data['student_loan_payment'] = int(input("Monthly student loan payment ($): "))
        user_data['has_car_loan'] = input("Have car loan? (yes/no): ").lower() == 'yes'
        user_data['car_loan_payment'] = int(input("Monthly car loan payment ($): "))
        user_data['has_mortgage'] = input("Have mortgage? (yes/no): ").lower() == 'yes'
        
        user_data['bank_balance'] = int(input("Current bank balance ($): "))
        user_data['monthly_savings'] = int(input("Monthly savings ($): "))
        user_data['recent_credit_inquiries'] = int(input("Credit inquiries in last 12 months: "))
        user_data['late_payments_12m'] = int(input("Late payments in last 12 months: "))
        user_data['bankruptcy_history'] = input("Ever filed bankruptcy? (yes/no): ").lower() == 'yes'
        user_data['years_credit_history'] = int(input("Years of credit history: "))
        
        return user_data
    
    def create_features(self, user_data):
        """
        Create all the features that the model expects
        """
        # Start with a dataframe
        df = pd.DataFrame([user_data])
        
        # Add loan approval dummy (model expects this)
        df['loan_approval'] = '1'
        
        # Create derived features (same as in preprocessing)
        df['debt_to_income_ratio'] = (df['monthly_housing_cost'] + df['student_loan_payment'] + df['car_loan_payment']) / (df['monthly_income'] + 1)
        df['available_income'] = df['monthly_income'] - df['monthly_housing_cost'] - df['student_loan_payment'] - df['car_loan_payment']
        df['savings_rate'] = df['monthly_savings'] / (df['available_income'] + 1)
        df['financial_stability'] = (np.sqrt(df['years_current_job'] + 1) * 100 + np.log(df['bank_balance'] + 1)) / 10
        df['credit_capacity'] = df['monthly_income'] / (df['num_credit_cards'] + 1)
        df['credit_risk_score'] = (df['late_payments_12m'] * 2 + df['recent_credit_inquiries'] + df['bankruptcy_history'].astype(int) * 10)
        df['credit_history_ratio'] = df['years_credit_history'] / (df['age'] + 1)
        df['debt_burden'] = df['debt_to_income_ratio'] * df['monthly_income'] / 1000
        
        # One-hot encode categorical variables
        # Education level
        for edu in ['bachelors', 'doctorate', 'high_school', 'masters', 'some_college']:
            df[f'education_level_{edu}'] = (df['education_level'] == edu).astype(int)
        
        # Employment type
        for emp in ['full_time', 'part_time', 'retired', 'self_employed', 'student', 'unemployed']:
            df[f'employment_type_{emp}'] = (df['employment_type'] == emp).astype(int)
        
        # State (simplified - just a few major states)
        for state in ['AZ', 'CA', 'FL', 'GA', 'IL', 'IN', 'MA', 'MD', 'MI', 'MO', 'NC', 'NJ', 'NY', 'OH', 'PA', 'TN', 'TX', 'VA', 'WA', 'WI']:
            df[f'state_{state}'] = (df['state'] == state).astype(int)
        
        # Loan approval
        df['loan_approval_0'] = 0
        df['loan_approval_1'] = 1
        
        # Boolean features
        df['has_student_loan'] = df['has_student_loan'].astype(int)
        df['has_car_loan'] = df['has_car_loan'].astype(int)
        df['has_mortgage'] = df['has_mortgage'].astype(int)
        df['bankruptcy_history'] = df['bankruptcy_history'].astype(int)
        
        # Remove original categorical columns
        df = df.drop(['education_level', 'employment_type', 'state', 'loan_approval'], axis=1)
        
        # Ensure all expected features are present
        expected_features = self.feature_names
        for feature in expected_features:
            if feature not in df.columns:
                df[feature] = 0
        
        # Select only the features the model expects, in the right order
        df = df.reindex(columns=expected_features, fill_value=0)
        
        return df
    
    def predict_credit_score(self, user_data):
        """
        Predict credit score from user input
        """
        print("\n🔄 Processing your information...")
        
        # Create features
        X = self.create_features(user_data)
        
        # Handle any NaN values
        X = X.fillna(0)
        
        try:
            # Make prediction
            print("🎯 Predicting your credit score...")
            predicted_score = self.model.predict(X)[0]
            
            # Ensure score is within reasonable bounds
            predicted_score = max(300, min(850, int(predicted_score)))
            
            return predicted_score
            
        except Exception as e:
            print(f"❌ Prediction error: {str(e)}")
            return None
    
    def interpret_score(self, score):
        """
        Provide interpretation of the credit score
        """
        if score >= 800:
            return "Excellent", "🟢"
        elif score >= 740:
            return "Very Good", "🟢"
        elif score >= 670:
            return "Good", "�"
        elif score >= 580:
            return "Fair", "🟠"
        else:
            return "Poor", "�"
    
    def run(self):
        """
        Run the interactive credit score predictor
        """
        print("🎯 Welcome to the Credit Score Predictor!")
        print("This tool uses your trained XGBoost model to predict credit scores.")
        
        try:
            # Get user input
            user_data = self.get_user_input()
            
            # Predict credit score
            predicted_score = self.predict_credit_score(user_data)
            
            if predicted_score:
                # Display results
                rating, color = self.interpret_score(predicted_score)
                
                print("\n" + "="*60)
                print("🎉 CREDIT SCORE PREDICTION RESULTS")
                print("="*60)
                print(f"{color} Predicted Credit Score: {predicted_score}")
                print(f"🏷️  Credit Rating: {rating}")
                print("="*60)
                
                # Show key insights
                if user_data.get('bankruptcy_history', False):
                    print("❌ Bankruptcy history significantly impacts your score")
                if user_data.get('late_payments_12m', 0) > 2:
                    print("⚠️ Recent late payments are affecting your score")
                if user_data.get('years_current_job', 0) > 3:
                    print("✅ Stable employment history helps your score")
                if user_data.get('monthly_savings', 0) > 500:
                    print("✅ Good savings habits boost your score")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using the Credit Score Predictor!")
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")


def main():
    """
    Main function to run the credit score predictor
    """
    
    p = CreditScorePredictor()
    data = {
        'age': 35,
        'state': 'CA',
        'education_level': 'bachelors',
        'employment_type': 'full_time',
        'monthly_income': 10000,
        'monthly_housing_cost': 0,
        'num_dependents': 0,
        'years_current_job': 15,
        'num_credit_cards': 3,
        'has_student_loan': False,
        'student_loan_payment': 0,
        'has_car_loan': False,
        'car_loan_payment': 0,
        'has_mortgage': True,
        'bank_balance': 1500000,
        'monthly_savings': 8000,
        'recent_credit_inquiries': 0,
        'late_payments_12m': 0,
        'bankruptcy_history': False,
        'years_credit_history': 1
    }


    score = p.predict_credit_score(data)
    print(f'Predicted Score : {score}')

if __name__ == "__main__":
    main()
