#!/usr/bin/env python3
"""
Simple test runner for Credit Score API
Run this script to test all API endpoints
"""

import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.api_tester import APITester

if __name__ == "__main__":
    print("🚀 Credit Score API Test Runner")
    print("Ensure the API server is running before running tests")
    print()
    
    # Check if server is specified
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5001'
    
    print(f"Testing API at: {base_url}")
    print()
    
    # Run tests
    tester = APITester(base_url)
    tester.run_full_test_suite()
