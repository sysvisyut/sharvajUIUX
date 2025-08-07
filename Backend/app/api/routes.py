from flask import Blueprint, request, jsonify, send_file
from app.auth.auth import auth_required, get_current_user
from app.models.database import Database, User, CreditScore, FinancialData, ChatHistory
from app.services.ml_service import MLService
from app.services.chat_service import ChatService
from app.services.pdf_service import PDFService
from datetime import datetime
import tempfile
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/dashboard', methods=['GET'])
@auth_required
def get_dashboard():
    """Get dashboard data for authenticated user"""
    try:
        user = get_current_user()
        firebase_uid = user['uid']
        
        # Get latest credit score data
        score_data = CreditScore.find_latest_by_user(firebase_uid)
        
        if score_data:
            dashboard_data = {
                'creditScore': score_data.get('credit_score', 0),
                'lastUpdatedDate': score_data.get('created_at', '').isoformat() if score_data.get('created_at') else None,
                'bestAchievableScore': score_data.get('best_achievable_score', 850),
                'loanApproved': score_data.get('loan_approved', False),
                'scoreRange': _get_score_range(score_data.get('credit_score', 0)),
                'hasData': True
            }
        else:
            dashboard_data = {
                'creditScore': None,
                'lastUpdatedDate': None,
                'bestAchievableScore': None,
                'loanApproved': None,
                'scoreRange': None,
                'hasData': False
            }
        
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/submit-score', methods=['POST'])
@auth_required
def submit_score():
    """Submit financial data and calculate credit score"""
    try:
        user = get_current_user()
        firebase_uid = user['uid']
        
        financial_data = request.get_json()
        
        if not financial_data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Check if user already has financial data
        existing_data = FinancialData.find_by_user(firebase_uid)
        
        if existing_data:
            # Return existing score if available
            existing_score = CreditScore.find_latest_by_user(firebase_uid)
            if existing_score:
                return jsonify({
                    'success': True,
                    'existing': True,
                    'data': {
                        'creditScore': existing_score.get('credit_score'),
                        'loanApproved': existing_score.get('loan_approved'),
                        'bestAchievableScore': existing_score.get('best_achievable_score'),
                        'scoreFactors': existing_score.get('score_factors', []),
                        'insights': existing_score.get('insights', []),
                        'calculatedAt': existing_score.get('created_at', '').isoformat() if existing_score.get('created_at') else None
                    }
                })
        
        # Save/update financial data
        FinancialData.update_or_create(firebase_uid, financial_data)
        
        # Calculate credit score using ML service
        score_result = MLService.calculate_credit_score(financial_data)
        
        # Save credit score data
        score_data = {
            'firebase_uid': firebase_uid,
            'credit_score': score_result['credit_score'],
            'loan_approved': score_result['loan_approved'],
            'best_achievable_score': score_result['best_achievable_score'],
            'score_factors': score_result.get('score_factors', []),
            'insights': score_result.get('insights', []),
            'model_version': score_result.get('model_version', 'unknown')
        }
        
        CreditScore.create(score_data)
        
        return jsonify({
            'success': True,
            'existing': False,
            'data': {
                'creditScore': score_result['credit_score'],
                'loanApproved': score_result['loan_approved'],
                'bestAchievableScore': score_result['best_achievable_score'],
                'scoreFactors': score_result.get('score_factors', []),
                'insights': score_result.get('insights', []),
                'calculatedAt': datetime.utcnow().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/insights', methods=['GET'])
@auth_required
def get_insights():
    """Get detailed insights for user"""
    try:
        user = get_current_user()
        firebase_uid = user['uid']
        
        # Get latest score data with insights
        score_data = CreditScore.find_latest_by_user(firebase_uid)
        
        if not score_data:
            return jsonify({
                'success': False,
                'error': 'No credit score data found. Please submit your information first.'
            }), 404
        
        insights_data = {
            'creditScore': score_data.get('credit_score'),
            'scoreRange': _get_score_range(score_data.get('credit_score', 0)),
            'loanApproved': score_data.get('loan_approved'),
            'bestAchievableScore': score_data.get('best_achievable_score'),
            'scoreFactors': score_data.get('score_factors', []),
            'insights': score_data.get('insights', []),
            'lastUpdated': score_data.get('created_at', '').isoformat() if score_data.get('created_at') else None
        }
        
        return jsonify({
            'success': True,
            'data': insights_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/chat', methods=['POST'])
@auth_required
def chat():
    """Handle chat requests"""
    try:
        user = get_current_user()
        firebase_uid = user['uid']
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Get user context for better responses
        user_context = None
        score_data = CreditScore.find_latest_by_user(firebase_uid)
        if score_data:
            user_context = {
                'credit_score': score_data.get('credit_score'),
                'last_updated': score_data.get('created_at', '').strftime('%Y-%m-%d') if score_data.get('created_at') else None,
                'loan_approved': score_data.get('loan_approved')
            }
        
        # Get response from chat service
        response = ChatService.send_message(message, user_context)
        
        # Save chat history
        ChatHistory.add_message(firebase_uid, message, response)
        
        return jsonify({
            'success': True,
            'data': {
                'response': response,
                'timestamp': datetime.utcnow().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/chat/suggestions', methods=['GET'])
def get_chat_suggestions():
    """Get suggested chat questions"""
    try:
        suggestions = ChatService.get_suggested_questions()
        
        return jsonify({
            'success': True,
            'data': {
                'suggestions': suggestions
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/generate-pdf', methods=['POST'])
@auth_required
def generate_pdf():
    """Generate PDF report"""
    try:
        user = get_current_user()
        firebase_uid = user['uid']
        
        # Get user's financial data and score data
        financial_data = FinancialData.find_by_user(firebase_uid)
        score_data = CreditScore.find_latest_by_user(firebase_uid)
        
        if not financial_data or not score_data:
            return jsonify({
                'success': False,
                'error': 'Insufficient data to generate report. Please submit your information first.'
            }), 400
        
        # Generate PDF
        pdf_buffer = PDFService.generate_credit_report(
            user_data=user,
            financial_data=financial_data,
            score_data=score_data
        )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_buffer.getvalue())
            tmp_file_path = tmp_file.name
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'credit_report_{timestamp}.pdf'
        
        def remove_file(response):
            try:
                os.unlink(tmp_file_path)
            except Exception:
                pass
            return response
        
        return send_file(
            tmp_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/chat/history', methods=['GET'])
@auth_required
def get_chat_history():
    """Get user's chat history"""
    try:
        user = get_current_user()
        firebase_uid = user['uid']
        
        limit = request.args.get('limit', 20, type=int)
        history = ChatHistory.get_user_history(firebase_uid, limit)
        
        # Format history for response
        formatted_history = []
        for chat in history:
            formatted_history.append({
                'message': chat['message'],
                'response': chat['response'],
                'timestamp': chat['timestamp'].isoformat() if chat.get('timestamp') else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'history': formatted_history
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _get_score_range(score):
    """Get score range description"""
    if score >= 800:
        return 'Exceptional'
    elif score >= 750:
        return 'Excellent'
    elif score >= 700:
        return 'Good'
    elif score >= 650:
        return 'Fair'
    elif score >= 600:
        return 'Poor'
    else:
        return 'Very Poor'

@api_bp.route('/ml/model-info', methods=['GET'])
@auth_required
def get_model_info():
    """Get information about the ML model"""
    try:
        model_info = MLService.get_model_info()
        return jsonify({
            'success': True,
            'data': model_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/ml/clear-cache', methods=['POST'])
@auth_required  
def clear_model_cache():
    """Clear the ML model cache"""
    try:
        MLService.clear_model_cache()
        return jsonify({
            'success': True,
            'message': 'Model cache cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
