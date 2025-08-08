#!/usr/bin/env python3
"""
Test script to verify OpenRouter API integration
Run this script to test the chat service with OpenRouter
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openrouter_direct():
    """Test OpenRouter API directly"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    model = os.getenv('OPEN_ROUTER_MODEL', 'meta-llama/llama-3.3-70b-instruct:free')
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    print(f"✅ Model: {model}")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://your-app-domain.com',
        'X-Title': 'Credit Score Assistant Test'
    }
    
    data = {
        'model': model,
        'messages': [
            {
                'role': 'system', 
                'content': 'You are a helpful AI financial advisor. Respond briefly and professionally.'
            },
            {
                'role': 'user', 
                'content': 'Hello! Can you help me understand credit scores?'
            }
        ],
        'max_tokens': 200,
        'temperature': 0.7
    }
    
    try:
        print("🔄 Testing OpenRouter API...")
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            print(f"✅ OpenRouter API Success!")
            print(f"🤖 AI Response: {ai_response}")
            return True
        else:
            print(f"❌ OpenRouter API Error: {response.status_code}")
            print(f"📝 Error Details: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False

def test_flask_app():
    """Test the Flask app chat endpoint"""
    try:
        print("\n🔄 Testing Flask app chat endpoint...")

        # First, check if Flask app is running
        print("🏥 Checking Flask app health...")
        health_response = requests.get('http://localhost:5001/health', timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Flask app is running - Status: {health_data.get('status')}")
            print(f"🔧 Config: {health_data.get('config')}")
            print(f"🔐 Auth bypass: {health_data.get('auth_bypass')}")
        else:
            print(f"⚠️  Health check returned: {health_response.status_code}")

        # First, get an auth token using test login
        print("🔐 Getting authentication token...")
        auth_response = requests.post(
            'http://localhost:5001/auth/test-login',
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if auth_response.status_code != 200:
            print(f"❌ Failed to get auth token: {auth_response.status_code}")
            print(f"📝 Auth Error: {auth_response.text}")
            return False

        auth_data = auth_response.json()
        token = auth_data.get('data', {}).get('token')

        if not token:
            print("❌ No token received from auth endpoint")
            return False

        print(f"✅ Auth token received: {token[:20]}...")

        # Test with a simple message using auth token
        response = requests.post(
            'http://localhost:5001/api/chat/send',
            json={'message': 'Hello, can you help me with my credit score?'},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            timeout=30
        )
        
        print(f"📊 Flask Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Flask API Success!")
            print(f"🤖 Response: {result.get('data', {}).get('response', 'No response')}")
            return True
        else:
            print(f"❌ Flask API Error: {response.status_code}")
            print(f"📝 Error Details: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on http://localhost:5001")
        return False
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🧪 OpenRouter Integration Test")
    print("=" * 50)
    
    # Test 1: Direct OpenRouter API
    print("\n1️⃣ Testing OpenRouter API directly...")
    direct_success = test_openrouter_direct()
    
    # Test 2: Flask app endpoint
    print("\n2️⃣ Testing Flask app chat endpoint...")
    flask_success = test_flask_app()
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 50)
    print(f"OpenRouter Direct API: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"Flask App Endpoint: {'✅ PASS' if flask_success else '❌ FAIL'}")
    
    if direct_success and flask_success:
        print("\n🎉 All tests passed! OpenRouter integration is working correctly.")
        return 0
    elif direct_success:
        print("\n⚠️  OpenRouter API works, but Flask app has issues. Check Flask app logs.")
        return 1
    else:
        print("\n❌ OpenRouter API test failed. Check your API key and model configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
