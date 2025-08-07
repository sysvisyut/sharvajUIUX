from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import uuid

class Database:
    client = None
    db = None
    
    @staticmethod
    def initialize(uri):
        Database.client = MongoClient(uri)
        Database.db = Database.client.get_default_database()
    
    @staticmethod
    def get_collection(name):
        return Database.db[name]

class User:
    COLLECTION = 'users'
    
    @staticmethod
    def create(user_data):
        """Create a new user record"""
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        result = Database.get_collection(User.COLLECTION).insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_firebase_uid(firebase_uid):
        """Find user by Firebase UID"""
        return Database.get_collection(User.COLLECTION).find_one({'firebase_uid': firebase_uid})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by MongoDB ObjectId"""
        return Database.get_collection(User.COLLECTION).find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def update(firebase_uid, update_data):
        """Update user data"""
        update_data['updated_at'] = datetime.utcnow()
        return Database.get_collection(User.COLLECTION).update_one(
            {'firebase_uid': firebase_uid},
            {'$set': update_data}
        )

class CreditScore:
    COLLECTION = 'credit_scores'
    
    @staticmethod
    def create(score_data):
        """Create a new credit score record"""
        score_data['created_at'] = datetime.utcnow()
        score_data['score_id'] = str(uuid.uuid4())
        result = Database.get_collection(CreditScore.COLLECTION).insert_one(score_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_latest_by_user(firebase_uid):
        """Find latest credit score for user"""
        return Database.get_collection(CreditScore.COLLECTION).find_one(
            {'firebase_uid': firebase_uid},
            sort=[('created_at', -1)]
        )
    
    @staticmethod
    def find_by_user(firebase_uid):
        """Find all credit scores for user"""
        return list(Database.get_collection(CreditScore.COLLECTION).find(
            {'firebase_uid': firebase_uid}
        ).sort('created_at', -1))
    
    @staticmethod
    def update_score(firebase_uid, score_data):
        """Update or create credit score"""
        existing = CreditScore.find_latest_by_user(firebase_uid)
        
        if existing:
            score_data['updated_at'] = datetime.utcnow()
            return Database.get_collection(CreditScore.COLLECTION).update_one(
                {'_id': existing['_id']},
                {'$set': score_data}
            )
        else:
            return CreditScore.create(score_data)

class FinancialData:
    COLLECTION = 'financial_data'
    
    @staticmethod
    def create(financial_data):
        """Create financial data record"""
        financial_data['created_at'] = datetime.utcnow()
        financial_data['data_id'] = str(uuid.uuid4())
        result = Database.get_collection(FinancialData.COLLECTION).insert_one(financial_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_user(firebase_uid):
        """Find latest financial data for user"""
        return Database.get_collection(FinancialData.COLLECTION).find_one(
            {'firebase_uid': firebase_uid},
            sort=[('created_at', -1)]
        )
    
    @staticmethod
    def update_or_create(firebase_uid, financial_data):
        """Update or create financial data"""
        existing = FinancialData.find_by_user(firebase_uid)
        
        if existing:
            financial_data['updated_at'] = datetime.utcnow()
            return Database.get_collection(FinancialData.COLLECTION).update_one(
                {'firebase_uid': firebase_uid},
                {'$set': financial_data}
            )
        else:
            financial_data['firebase_uid'] = firebase_uid
            return FinancialData.create(financial_data)

class ChatHistory:
    COLLECTION = 'chat_history'
    
    @staticmethod
    def add_message(firebase_uid, message, response):
        """Add chat message and response"""
        chat_data = {
            'firebase_uid': firebase_uid,
            'message': message,
            'response': response,
            'timestamp': datetime.utcnow()
        }
        result = Database.get_collection(ChatHistory.COLLECTION).insert_one(chat_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_user_history(firebase_uid, limit=50):
        """Get chat history for user"""
        return list(Database.get_collection(ChatHistory.COLLECTION).find(
            {'firebase_uid': firebase_uid}
        ).sort('timestamp', -1).limit(limit))
