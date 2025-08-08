#!/usr/bin/env python3
"""
Simple test to debug the chat endpoint
"""

import requests
import json

def test_simple_chat():
    """Test the chat endpoint with minimal payload"""
    try:
        print("🔄 Testing simple chat...")
        
        # Get auth token
        auth_response = requests.post(
            'http://localhost:5001/auth/test-login',
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if auth_response.status_code != 200:
            print(f"❌ Auth failed: {auth_response.status_code}")
            return False
        
        token = auth_response.json()['data']['token']
        print(f"✅ Got token: {token}")
        
        # Test chat endpoint
        chat_response = requests.post(
            'http://localhost:5001/api/chat/send',
            json={'message': 'Hello'},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            timeout=60  # Longer timeout
        )
        
        print(f"📊 Chat response status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            print(f"✅ Chat success!")
            print(f"🤖 Response: {result.get('data', {}).get('response', 'No response')[:200]}...")
            return True
        else:
            print(f"❌ Chat failed: {chat_response.status_code}")
            print(f"📝 Error: {chat_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    test_simple_chat()
