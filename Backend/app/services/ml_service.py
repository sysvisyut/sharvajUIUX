import requests
import json
from flask import current_app
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
import threading

class MLService:
    """Service for credit score calculation and loan approval"""
    
    # Class-level cache for the loaded model
    _model = None
    _model_lock = threading.Lock()
    _model_version = None
    _model_loaded_at = None
    
    # Feature names that the XGBoost model expects (in order)
    FEATURE_NAMES = [
        'age', 'annual_income', 'monthly_cost', 'savings', 'monthly_savings',
        'dependents', 'num_credit_cards', 'student_loan_payment', 'car_loan_payment',
        'late_payments', 'credit_history_length', 'recent_credit_inquiries',
        'state_encoded', 'education_encoded', 'employment_type_encoded',
        'has_mortgage', 'has_student_loan', 'has_car_loan', 'bankruptcy_history'
    ]
    
    @classmethod
    def _get_model_path(cls):
        """Get the path to the XGBoost model"""
        # Get the project root (3 levels up from this file)
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        model_path = os.path.join(project_root, 'Model', 'models', 'xgboost_credit_score_model_final.joblib')
        return model_path
    
    @classmethod
    def _load_model(cls):
        """Load the XGBoost model with caching"""
        with cls._model_lock:
            if cls._model is None:
                try:
                    model_path = cls._get_model_path()
                    if not os.path.exists(model_path):
                        raise FileNotFoundError(f"Model file not found at {model_path}")
                    
                    current_app.logger.info(f"Loading XGBoost model from {model_path}")
                    cls._model = joblib.load(model_path)
                    cls._model_version = "xgboost_v1.0"
                    cls._model_loaded_at = datetime.utcnow()
                    current_app.logger.info("XGBoost model loaded successfully")
                    
                except Exception as e:
                    current_app.logger.error(f"Failed to load XGBoost model: {str(e)}")
                    cls._model = None
                    raise
            
            return cls._model
    
    @classmethod
    def get_model_info(cls):
        """Get information about the loaded model"""
        try:
            model_path = cls._get_model_path()
            model_exists = os.path.exists(model_path)
            
            info = {
                'model_path': model_path,
                'model_exists': model_exists,
                'model_loaded': cls._model is not None,
                'model_version': cls._model_version,
                'loaded_at': cls._model_loaded_at.isoformat() if cls._model_loaded_at else None,
                'expected_features': len(cls.FEATURE_NAMES),
                'feature_names': cls.FEATURE_NAMES
            }
            
            if model_exists:
                try:
                    stat = os.stat(model_path)
                    info['model_size_bytes'] = stat.st_size
                    info['model_modified'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                except:
                    pass
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    @classmethod
    def _encode_categorical_features(cls, financial_data):
        """Encode categorical features as expected by the model"""
        # State encoding (simplified - in real implementation, use the same encoding as training)
        states = {'CA': 0, 'NY': 1, 'TX': 2, 'FL': 3, 'IL': 4}  # Add more states as needed
        state = financial_data.get('personal_info', {}).get('state', 'CA')
        state_encoded = states.get(state, 0)
        
        # Education encoding
        education_levels = {
            'high_school': 0,
            'some_college': 1,
            'bachelors': 2,
            'masters': 3,
            'doctorate': 4
        }
        education = financial_data.get('personal_info', {}).get('education_level', 'high_school')
        education_encoded = education_levels.get(education, 0)
        
        # Employment type encoding
        employment_types = {
            'unemployed': 0,
            'part_time': 1,
            'full_time': 2,
            'self_employed': 3,
            'retired': 4
        }
        employment_type = financial_data.get('employment_income', {}).get('employment_type', 'full_time')
        employment_type_encoded = employment_types.get(employment_type, 2)
        
        return state_encoded, education_encoded, employment_type_encoded
    
    @classmethod
    def _prepare_features_for_model(cls, financial_data):
        """Prepare features in the exact format expected by the XGBoost model"""
        try:
            # Extract basic features
            age = financial_data.get('personal_info', {}).get('age', 30)
            annual_income = financial_data.get('employment_income', {}).get('annual_income', 50000)
            monthly_cost = financial_data.get('housing', {}).get('monthly_cost', 1200)
            savings = financial_data.get('housing', {}).get('savings', 10000)
            monthly_savings = financial_data.get('housing', {}).get('monthly_savings', 200)
            dependents = financial_data.get('family', {}).get('dependents', 0)
            num_credit_cards = financial_data.get('credit_loans', {}).get('num_credit_cards', 2)
            student_loan_payment = financial_data.get('credit_loans', {}).get('student_loan_payment', 0)
            car_loan_payment = financial_data.get('credit_loans', {}).get('car_loan_payment', 0)
            late_payments = financial_data.get('credit_behavior', {}).get('late_payments', 0)
            credit_history_length = financial_data.get('credit_behavior', {}).get('credit_history_length', 5)
            recent_credit_inquiries = financial_data.get('credit_behavior', {}).get('recent_credit_inquiries', 1)
            
            # Boolean features (convert to int)
            has_mortgage = int(financial_data.get('housing', {}).get('has_mortgage', False))
            has_student_loan = int(financial_data.get('credit_loans', {}).get('has_student_loan', False))
            has_car_loan = int(financial_data.get('credit_loans', {}).get('has_car_loan', False))
            bankruptcy_history = int(financial_data.get('credit_behavior', {}).get('bankruptcy_history', False))
            
            # Encode categorical features
            state_encoded, education_encoded, employment_type_encoded = cls._encode_categorical_features(financial_data)
            
            # Create feature array in the exact order expected by the model
            features = [
                age, annual_income, monthly_cost, savings, monthly_savings,
                dependents, num_credit_cards, student_loan_payment, car_loan_payment,
                late_payments, credit_history_length, recent_credit_inquiries,
                state_encoded, education_encoded, employment_type_encoded,
                has_mortgage, has_student_loan, has_car_loan, bankruptcy_history
            ]
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            current_app.logger.error(f"Feature preparation error: {str(e)}")
            return None
    
    @staticmethod
    def calculate_credit_score(financial_data):
        """Calculate credit score using ML model"""
        try:
            if current_app.config.get('ML_MODEL_LOCAL', True):
                return MLService._local_model_prediction(financial_data)
            else:
                return MLService._api_model_prediction(financial_data)
        except Exception as e:
            current_app.logger.error(f"ML prediction error: {str(e)}")
            return MLService._fallback_prediction(financial_data)
    
    @classmethod
    def _local_model_prediction(cls, financial_data):
        """Use local XGBoost model for prediction"""
        try:
            # Load the model (cached)
            model = cls._load_model()
            if model is None:
                raise Exception("Model not loaded")
            
            # Prepare features
            features = cls._prepare_features_for_model(financial_data)
            if features is None:
                raise Exception("Feature preparation failed")
            
            # Make prediction
            current_app.logger.info("Making prediction with XGBoost model")
            prediction = model.predict(features)
            credit_score = int(prediction[0])
            
            # Ensure score is in valid range
            credit_score = max(300, min(850, credit_score))
            
            # Calculate loan approval based on score and other factors
            annual_income = financial_data.get('employment_income', {}).get('annual_income', 0)
            late_payments = financial_data.get('credit_behavior', {}).get('late_payments', 0)
            loan_approved = credit_score >= 650 and annual_income > 25000 and late_payments <= 2
            
            # Calculate best achievable score (conservative estimate)
            best_score = min(850, credit_score + 100)
            
            # Generate insights
            insights = cls._generate_insights(financial_data, credit_score)
            
            # Generate score factors
            score_factors = cls._generate_score_factors(financial_data, credit_score)
            
            return {
                'credit_score': credit_score,
                'loan_approved': loan_approved,
                'best_achievable_score': int(best_score),
                'score_factors': score_factors,
                'insights': insights,
                'calculated_at': datetime.utcnow().isoformat(),
                'model_version': cls._model_version or 'xgboost_v1.0',
                'prediction_method': 'xgboost_model'
            }
            
        except Exception as e:
            current_app.logger.error(f"Local XGBoost model error: {str(e)}")
            return cls._rule_based_scoring(financial_data)
    
    @staticmethod
    def _generate_score_factors(financial_data, credit_score):
        """Generate score factors based on financial data and predicted score"""
        factors = []
        
        # Payment History Analysis
        late_payments = financial_data.get('credit_behavior', {}).get('late_payments', 0)
        if late_payments == 0:
            factors.append({
                'factor': 'Payment History',
                'weight': 35,
                'status': 'excellent',
                'impact': 'positive',
                'description': 'No late payments recorded'
            })
        elif late_payments <= 2:
            factors.append({
                'factor': 'Payment History', 
                'weight': 35,
                'status': 'good',
                'impact': 'neutral',
                'description': f'{late_payments} late payment(s)'
            })
        else:
            factors.append({
                'factor': 'Payment History',
                'weight': 35, 
                'status': 'poor',
                'impact': 'negative',
                'description': f'{late_payments} late payments hurt your score'
            })
        
        # Credit Utilization (estimated)
        num_cards = financial_data.get('credit_loans', {}).get('num_credit_cards', 2)
        if num_cards <= 3:
            factors.append({
                'factor': 'Credit Utilization',
                'weight': 30,
                'status': 'good',
                'impact': 'positive', 
                'description': f'{num_cards} credit cards managed well'
            })
        else:
            factors.append({
                'factor': 'Credit Utilization',
                'weight': 30,
                'status': 'fair',
                'impact': 'neutral',
                'description': f'{num_cards} credit cards - monitor usage'
            })
        
        # Length of Credit History
        credit_history = financial_data.get('credit_behavior', {}).get('credit_history_length', 0)
        if credit_history >= 7:
            factors.append({
                'factor': 'Length of Credit History',
                'weight': 15,
                'status': 'excellent',
                'impact': 'positive',
                'description': f'{credit_history} years of credit history'
            })
        elif credit_history >= 3:
            factors.append({
                'factor': 'Length of Credit History',
                'weight': 15,
                'status': 'good', 
                'impact': 'neutral',
                'description': f'{credit_history} years of credit history'
            })
        else:
            factors.append({
                'factor': 'Length of Credit History',
                'weight': 15,
                'status': 'fair',
                'impact': 'negative',
                'description': 'Limited credit history'
            })
        
        # Income Stability
        income = financial_data.get('employment_income', {}).get('annual_income', 0)
        if income >= 75000:
            factors.append({
                'factor': 'Income Stability',
                'weight': 10,
                'status': 'excellent',
                'impact': 'positive',
                'description': 'Strong income supports creditworthiness'
            })
        elif income >= 40000:
            factors.append({
                'factor': 'Income Stability', 
                'weight': 10,
                'status': 'good',
                'impact': 'neutral',
                'description': 'Stable income level'
            })
        else:
            factors.append({
                'factor': 'Income Stability',
                'weight': 10,
                'status': 'fair',
                'impact': 'neutral', 
                'description': 'Consider increasing income for better rates'
            })
        
        # Recent Credit Inquiries
        inquiries = financial_data.get('credit_behavior', {}).get('recent_credit_inquiries', 0)
        if inquiries == 0:
            factors.append({
                'factor': 'New Credit Inquiries',
                'weight': 10,
                'status': 'excellent',
                'impact': 'positive',
                'description': 'No recent credit inquiries'
            })
        elif inquiries <= 2:
            factors.append({
                'factor': 'New Credit Inquiries',
                'weight': 10,
                'status': 'good',
                'impact': 'neutral',
                'description': f'{inquiries} recent inquiry/inquiries'
            })
        else:
            factors.append({
                'factor': 'New Credit Inquiries',
                'weight': 10,
                'status': 'poor',
                'impact': 'negative',
                'description': f'{inquiries} recent inquiries may lower score'
            })
        
        return factors
    
    @staticmethod
    def _api_model_prediction(financial_data):
        """Use external API for ML prediction"""
        try:
            model_url = current_app.config.get('ML_MODEL_URL')
            response = requests.post(
                f"{model_url}/predict",
                json=financial_data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            current_app.logger.error(f"API model error: {str(e)}")
            return MLService._fallback_prediction(financial_data)
    
    @staticmethod
    def _rule_based_scoring(financial_data):
        """Rule-based credit scoring for demo/fallback"""
        try:
            # Extract key financial metrics
            age = financial_data.get('personal_info', {}).get('age', 25)
            income = financial_data.get('employment_income', {}).get('annual_income', 0)
            housing_cost = financial_data.get('housing', {}).get('monthly_cost', 0)
            savings = financial_data.get('housing', {}).get('savings', 0)
            dependents = financial_data.get('family', {}).get('dependents', 0)
            existing_loans = financial_data.get('credit_loans', {}).get('existing_loans', 0)
            late_payments = financial_data.get('credit_behavior', {}).get('late_payments', 0)
            credit_history_length = financial_data.get('credit_behavior', {}).get('credit_history_length', 0)
            
            # Calculate base score (300-850 range)
            base_score = 500
            
            # Age factor (18-65 optimal range)
            if 25 <= age <= 45:
                base_score += 50
            elif age >= 65 or age < 21:
                base_score -= 30
            
            # Income factor
            if income >= 100000:
                base_score += 100
            elif income >= 50000:
                base_score += 70
            elif income >= 30000:
                base_score += 40
            elif income < 15000:
                base_score -= 50
            
            # Debt-to-income ratio
            if income > 0:
                monthly_income = income / 12
                debt_ratio = (housing_cost + existing_loans) / monthly_income
                if debt_ratio < 0.3:
                    base_score += 80
                elif debt_ratio < 0.5:
                    base_score += 40
                elif debt_ratio > 0.8:
                    base_score -= 100
            
            # Savings factor
            if savings >= 50000:
                base_score += 60
            elif savings >= 20000:
                base_score += 30
            elif savings < 5000:
                base_score -= 20
            
            # Credit behavior
            base_score -= (late_payments * 25)  # Each late payment costs 25 points
            
            if credit_history_length >= 5:
                base_score += 70
            elif credit_history_length >= 2:
                base_score += 40
            elif credit_history_length == 0:
                base_score -= 60
            
            # Dependents factor
            base_score -= (dependents * 10)
            
            # Clamp score to valid range
            credit_score = max(300, min(850, base_score))
            
            # Calculate loan approval
            loan_approved = credit_score >= 650 and (income > 25000) and (late_payments <= 2)
            
            # Calculate best achievable score
            best_score = min(850, credit_score + 150)
            
            # Generate insights
            insights = MLService._generate_insights(financial_data, credit_score)
            
            return {
                'credit_score': int(credit_score),
                'loan_approved': loan_approved,
                'best_achievable_score': int(best_score),
                'score_factors': [
                    {'factor': 'Payment History', 'weight': 35, 'status': 'good' if late_payments <= 1 else 'poor'},
                    {'factor': 'Credit Utilization', 'weight': 30, 'status': 'good'},
                    {'factor': 'Length of Credit History', 'weight': 15, 'status': 'good' if credit_history_length >= 3 else 'fair'},
                    {'factor': 'Credit Mix', 'weight': 10, 'status': 'fair'},
                    {'factor': 'New Credit', 'weight': 10, 'status': 'good'}
                ],
                'insights': insights,
                'calculated_at': datetime.utcnow().isoformat(),
                'model_version': 'rule_based_v1.0'
            }
            
        except Exception as e:
            current_app.logger.error(f"Rule-based scoring error: {str(e)}")
            return MLService._fallback_prediction(financial_data)
    
    @staticmethod
    def _generate_insights(financial_data, credit_score):
        """Generate personalized financial insights based on XGBoost prediction"""
        insights = []
        
        late_payments = financial_data.get('credit_behavior', {}).get('late_payments', 0)
        income = financial_data.get('employment_income', {}).get('annual_income', 0)
        savings = financial_data.get('housing', {}).get('savings', 0)
        monthly_cost = financial_data.get('housing', {}).get('monthly_cost', 0)
        credit_history_length = financial_data.get('credit_behavior', {}).get('credit_history_length', 0)
        num_credit_cards = financial_data.get('credit_loans', {}).get('num_credit_cards', 0)
        
        # Score-based insights
        if credit_score >= 750:
            insights.append({
                'type': 'positive',
                'title': 'Excellent Credit Score',
                'message': 'Your credit score qualifies you for the best interest rates and premium credit products!',
                'impact': 'high'
            })
        elif credit_score >= 700:
            insights.append({
                'type': 'positive', 
                'title': 'Good Credit Score',
                'message': 'You qualify for most loans with competitive rates. Consider reaching 750+ for even better terms.',
                'impact': 'medium'
            })
        elif credit_score >= 650:
            insights.append({
                'type': 'tip',
                'title': 'Fair Credit Score',
                'message': 'You qualify for many loan products. Focus on improving to 700+ for better rates.',
                'impact': 'medium'
            })
        else:
            insights.append({
                'type': 'warning',
                'title': 'Credit Score Needs Improvement',
                'message': 'Focus on payment history and reducing debt utilization to improve your score significantly.',
                'impact': 'high'
            })
        
        # Payment history insights
        if late_payments > 2:
            insights.append({
                'type': 'warning',
                'title': 'Payment History Impact',
                'message': f'Your {late_payments} late payments are significantly impacting your score. Set up automatic payments to avoid future late payments.',
                'impact': 'high'
            })
        elif late_payments > 0:
            insights.append({
                'type': 'tip',
                'title': 'Payment History Opportunity',
                'message': 'Continue making on-time payments to improve your score over time.',
                'impact': 'medium'
            })
        
        # Income vs expenses insight
        if income > 0 and monthly_cost > 0:
            monthly_income = income / 12
            housing_ratio = monthly_cost / monthly_income
            if housing_ratio > 0.4:
                insights.append({
                    'type': 'warning',
                    'title': 'Housing Cost Ratio',
                    'message': f'Your housing costs are {housing_ratio:.1%} of income. Consider reducing to below 30% for better financial health.',
                    'impact': 'medium'
                })
            elif housing_ratio < 0.25:
                insights.append({
                    'type': 'positive',
                    'title': 'Excellent Housing Ratio',
                    'message': f'Your housing costs are only {housing_ratio:.1%} of income - excellent financial management!',
                    'impact': 'low'
                })
        
        # Savings insights
        if income > 0:
            months_of_savings = (savings / (income / 12)) if (income / 12) > 0 else 0
            if months_of_savings < 3:
                insights.append({
                    'type': 'tip',
                    'title': 'Emergency Fund',
                    'message': 'Build an emergency fund of 3-6 months of expenses for better financial security.',
                    'impact': 'medium'
                })
            elif months_of_savings >= 6:
                insights.append({
                    'type': 'positive',
                    'title': 'Strong Emergency Fund',
                    'message': f'Excellent! You have {months_of_savings:.1f} months of expenses saved.',
                    'impact': 'low'
                })
        
        # Credit history insights
        if credit_history_length < 2:
            insights.append({
                'type': 'tip',
                'title': 'Credit History Length',
                'message': 'Keep your oldest accounts open to build a longer credit history over time.',
                'impact': 'medium'
            })
        
        # Credit cards insight
        if num_credit_cards == 0:
            insights.append({
                'type': 'tip',
                'title': 'Credit Building',
                'message': 'Consider getting a credit card to build your credit history, but use it responsibly.',
                'impact': 'medium'
            })
        elif num_credit_cards > 5:
            insights.append({
                'type': 'warning',
                'title': 'Credit Card Management',
                'message': f'Having {num_credit_cards} credit cards requires careful management. Consider consolidating if needed.',
                'impact': 'low'
            })
        
        return insights
    
    @staticmethod
    def _fallback_prediction(financial_data):
        """Fallback prediction when XGBoost model fails"""
        current_app.logger.warning("Using fallback prediction method")
        return {
            'credit_score': 650,
            'loan_approved': False,
            'best_achievable_score': 750,
            'score_factors': [
                {
                    'factor': 'Payment History',
                    'weight': 35,
                    'status': 'unknown',
                    'impact': 'neutral',
                    'description': 'Unable to analyze - please try again'
                },
                {
                    'factor': 'Credit Utilization', 
                    'weight': 30,
                    'status': 'unknown',
                    'impact': 'neutral',
                    'description': 'Unable to analyze - please try again'
                }
            ],
            'insights': [{
                'type': 'info',
                'title': 'Score Calculation',
                'message': 'Using fallback scoring method due to model unavailability. Please try again later for accurate XGBoost-based results.',
                'impact': 'low'
            }],
            'calculated_at': datetime.utcnow().isoformat(),
            'model_version': 'fallback_v1.0',
            'prediction_method': 'fallback'
        }
    
    @classmethod
    def clear_model_cache(cls):
        """Clear the cached model (useful for testing or updates)"""
        with cls._model_lock:
            cls._model = None
            cls._model_version = None
            cls._model_loaded_at = None
            current_app.logger.info("Model cache cleared")
    
    @classmethod
    def preload_model(cls):
        """Preload the model (useful for application startup)"""
        try:
            cls._load_model()
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to preload model: {str(e)}")
            return False
