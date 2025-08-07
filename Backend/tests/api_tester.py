import requests
import json
from datetime import datetime

class APITester:
    """Utility class for testing the Credit Score API"""
    
    def __init__(self, base_url='http://localhost:5001'):
        self.base_url = base_url
        self.auth_token = None
        
    def test_health_check(self):
        """Test API health endpoint"""
        try:
            response = requests.get(f'{self.base_url}/health')
            print(f"✅ Health Check: {response.status_code}")
            print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health Check Failed: {str(e)}")
            return False
    
    def test_auth_bypass(self):
        """Test authentication bypass for development"""
        try:
            response = requests.post(f'{self.base_url}/auth/test-login')
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                print(f"✅ Auth Bypass: {response.status_code}")
                print(f"   Token: {self.auth_token}")
                return True
            else:
                print(f"❌ Auth Bypass Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Auth Bypass Error: {str(e)}")
            return False
    
    def test_dashboard(self):
        """Test dashboard endpoint"""
        if not self.auth_token:
            print("❌ No auth token available")
            return False
            
        try:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            response = requests.get(f'{self.base_url}/api/dashboard', headers=headers)
            print(f"✅ Dashboard: {response.status_code}")
            print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Dashboard Error: {str(e)}")
            return False
    
    def test_submit_score(self, financial_data=None):
        """Test score submission endpoint"""
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        if not financial_data:
            financial_data = self.get_sample_financial_data()
            
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(
                f'{self.base_url}/api/submit-score', 
                headers=headers,
                json=financial_data
            )
            print(f"✅ Score Submission: {response.status_code}")
            print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Score Submission Error: {str(e)}")
            return False
    
    def test_chat(self, message="How can I improve my credit score?"):
        """Test chat endpoint"""
        if not self.auth_token:
            print("❌ No auth token available")
            return False
            
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(
                f'{self.base_url}/api/chat',
                headers=headers,
                json={'message': message}
            )
            print(f"✅ Chat: {response.status_code}")
            print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Chat Error: {str(e)}")
            return False
    
    def test_chat_suggestions(self):
        """Test chat suggestions endpoint"""
        try:
            response = requests.get(f'{self.base_url}/api/chat/suggestions')
            print(f"✅ Chat Suggestions: {response.status_code}")
            print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Chat Suggestions Error: {str(e)}")
            return False
    
    def run_full_test_suite(self):
        """Run complete test suite"""
        print("🧪 Starting Credit Score API Test Suite")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Authentication Bypass", self.test_auth_bypass),
            ("Dashboard", self.test_dashboard),
            ("Submit Score", self.test_submit_score),
            ("Chat", self.test_chat),
            ("Chat Suggestions", self.test_chat_suggestions)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            if test_func():
                passed += 1
            print("-" * 30)
        
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! API is working correctly.")
        else:
            print("⚠️ Some tests failed. Check the output above.")
    
    @staticmethod
    def get_sample_financial_data():
        """Get sample financial data for testing"""
        return {
            "personal_info": {
                "age": 28,
                "state": "California",
                "education_level": "Bachelor's Degree"
            },
            "employment_income": {
                "employment_type": "Full-time Employee",
                "annual_income": 65000,
                "job_duration": "2 years"
            },
            "housing": {
                "monthly_cost": 2000,
                "mortgage": 0,
                "savings": 15000,
                "balance": 5000
            },
            "family": {
                "dependents": 0
            },
            "credit_loans": {
                "existing_loans": 1,
                "loan_payments": 300,
                "credit_cards": 2
            },
            "credit_behavior": {
                "inquiries": 1,
                "late_payments": 0,
                "bankruptcy": False,
                "credit_history_length": 3
            }
        }

def main():
    """Main testing function"""
    print("Credit Score API Testing Utility")
    print("Make sure the API is running on http://localhost:5000")
    print()
    
    tester = APITester()
    tester.run_full_test_suite()

if __name__ == "__main__":
    main()
