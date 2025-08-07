#!/usr/bin/env python3
"""
Test script for ML Service model loading and prediction
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from flask import Flask
from config.config import DevelopmentConfig
from app.services.ml_service import MLService

def test_model_loading():
    """Test the model loading functionality"""
    print("🧪 Testing ML Service Model Loading...")
    
    # Create a minimal Flask app for testing
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    with app.app_context():
        print("\n1. Testing model path calculation...")
        model_path = MLService._get_model_path()
        print(f"   Model path: {model_path}")
        print(f"   File exists: {os.path.exists(model_path)}")
        
        print("\n2. Testing model info...")
        model_info = MLService.get_model_info()
        print(f"   Model info: {model_info}")
        
        print("\n3. Testing model loading...")
        model = MLService._load_model()
        if model is not None:
            print(f"   ✅ Model loaded successfully: {type(model)}")
        else:
            print("   ❌ Model loading failed")
        
        print("\n4. Testing feature preparation...")
        # Sample financial data for testing
        sample_data = {
            'personal_info': {
                'age': 30,
                'state': 'CA',
                'education_level': 'bachelors'
            },
            'employment_income': {
                'annual_income': 60000,
                'employment_type': 'full_time',
                'years_current_job': 3
            },
            'housing': {
                'monthly_cost': 1500,
                'savings': 10000,
                'monthly_savings': 300,
                'has_mortgage': False
            },
            'family': {
                'dependents': 1
            },
            'credit_loans': {
                'num_credit_cards': 2,
                'student_loan_payment': 200,
                'car_loan_payment': 0,
                'has_student_loan': True,
                'has_car_loan': False
            },
            'credit_behavior': {
                'late_payments': 0,
                'credit_history_length': 5,
                'recent_credit_inquiries': 1,
                'bankruptcy_history': False
            }
        }
        
        features = MLService._prepare_features_for_model(sample_data)
        if features is not None:
            print(f"   ✅ Features prepared successfully: {len(features)} features")
            print(f"   Features: {features}")
        else:
            print("   ❌ Feature preparation failed")
        
        print("\n5. Testing full prediction...")
        try:
            result = MLService.calculate_credit_score(sample_data)
            print(f"   ✅ Prediction successful!")
            print(f"   Credit Score: {result.get('credit_score')}")
            print(f"   Loan Approved: {result.get('loan_approved')}")
            print(f"   Model Version: {result.get('model_version')}")
        except Exception as e:
            print(f"   ❌ Prediction failed: {e}")

if __name__ == "__main__":
    test_model_loading()
