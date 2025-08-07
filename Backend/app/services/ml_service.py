import requests
import json
from flask import current_app
import joblib
import numpy as np
from datetime import datetime

class MLService:
    """Service for credit score calculation and loan approval"""
    
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
    
    @staticmethod
    def _local_model_prediction(financial_data):
        """Use local ML model for prediction"""
        try:
            # Load model (implement your model loading logic)
            # model = joblib.load('models/baseline_linear_regression.joblib')
            
            # For demo, use rule-based scoring
            score_data = MLService._rule_based_scoring(financial_data)
            return score_data
            
        except Exception as e:
            current_app.logger.error(f"Local model error: {str(e)}")
            return MLService._fallback_prediction(financial_data)
    
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
        """Generate personalized financial insights"""
        insights = []
        
        late_payments = financial_data.get('credit_behavior', {}).get('late_payments', 0)
        income = financial_data.get('employment_income', {}).get('annual_income', 0)
        savings = financial_data.get('housing', {}).get('savings', 0)
        
        if late_payments > 2:
            insights.append({
                'type': 'warning',
                'title': 'Payment History',
                'message': 'Reduce late payments to improve your score by 50-100 points.',
                'impact': 'high'
            })
        
        if income < 30000:
            insights.append({
                'type': 'tip',
                'title': 'Income Growth',
                'message': 'Increasing your income can significantly improve loan approval chances.',
                'impact': 'medium'
            })
        
        if savings < 10000:
            insights.append({
                'type': 'tip',
                'title': 'Emergency Fund',
                'message': 'Build an emergency fund of 3-6 months of expenses.',
                'impact': 'medium'
            })
        
        if credit_score >= 750:
            insights.append({
                'type': 'positive',
                'title': 'Excellent Credit',
                'message': 'Your credit score qualifies you for the best interest rates!',
                'impact': 'high'
            })
        elif credit_score >= 650:
            insights.append({
                'type': 'positive',
                'title': 'Good Credit',
                'message': 'You qualify for most loans. Focus on reaching 750+ for better rates.',
                'impact': 'medium'
            })
        else:
            insights.append({
                'type': 'warning',
                'title': 'Credit Improvement Needed',
                'message': 'Focus on payment history and reducing debt to improve your score.',
                'impact': 'high'
            })
        
        return insights
    
    @staticmethod
    def _fallback_prediction(financial_data):
        """Fallback prediction when all models fail"""
        return {
            'credit_score': 650,
            'loan_approved': False,
            'best_achievable_score': 750,
            'score_factors': [],
            'insights': [{
                'type': 'info',
                'title': 'Score Calculation',
                'message': 'Using fallback scoring method. Please try again later for accurate results.',
                'impact': 'low'
            }],
            'calculated_at': datetime.utcnow().isoformat(),
            'model_version': 'fallback_v1.0'
        }
