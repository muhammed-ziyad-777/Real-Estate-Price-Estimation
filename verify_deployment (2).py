#!/usr/bin/env python3
"""
Real Estate AI - Deployment Verification Script
Tests all application endpoints and features
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

class DeploymentVerifier:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def test_endpoint(self, endpoint, method="GET", data=None, expected_status=200):
        """Test a single endpoint"""
        url = urljoin(self.base_url, endpoint)
        
        try:
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=10)
            
            success = response.status_code == expected_status
            
            result = {
                'endpoint': endpoint,
                'method': method,
                'status_code': response.status_code,
                'expected': expected_status,
                'success': success,
                'response_time': response.elapsed.total_seconds()
            }
            
            self.results.append(result)
            
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {method} {endpoint} - {response.status_code} ({response.elapsed.total_seconds():.2f}s)")
            
            return success, response
            
        except Exception as e:
            result = {
                'endpoint': endpoint,
                'method': method,
                'status_code': 'ERROR',
                'expected': expected_status,
                'success': False,
                'error': str(e)
            }
            
            self.results.append(result)
            print(f"❌ {method} {endpoint} - ERROR: {e}")
            return False, None
    
    def test_main_pages(self):
        """Test all main application pages"""
        print("\n🏠 Testing Main Pages...")
        
        pages = [
            "/",
            "/predict",
            "/trends", 
            "/compare",
            "/map",
            "/chat",
            "/loan-calculator",
            "/history",
            "/about"
        ]
        
        for page in pages:
            self.test_endpoint(page)
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        print("\n🔌 Testing API Endpoints...")
        
        # Test locations API
        self.test_endpoint("/api/locations")
        
        # Test location suggestions
        self.test_endpoint("/api/location-suggestions?q=white")
        
        # Test prediction API
        prediction_data = {
            "location": "Whitefield",
            "area_type": "Super built-up Area",
            "size": "3 BHK",
            "total_sqft": 1450,
            "bath": 3,
            "balcony": 2,
            "availability": "Ready To Move"
        }
        
        self.test_endpoint("/api/predict", "POST", prediction_data)
        
        # Test trends API
        self.test_endpoint("/api/trends/Whitefield")
        
        # Test chat API
        chat_data = {"message": "What is the average price in Bangalore?"}
        self.test_endpoint("/api/chat", "POST", chat_data)
        
        # Test loan calculator API
        loan_data = {
            "principal": 5000000,
            "rate": 8.5,
            "tenure": 20
        }
        self.test_endpoint("/api/loan-calculator", "POST", loan_data)
    
    def test_static_assets(self):
        """Test static asset loading"""
        print("\n📁 Testing Static Assets...")
        
        assets = [
            "/static/css/main.css",
            "/static/js/main.js",
            "/static/js/theme.js"
        ]
        
        for asset in assets:
            self.test_endpoint(asset)
    
    def test_error_pages(self):
        """Test error handling"""
        print("\n🚫 Testing Error Handling...")
        
        # Test 404 page
        self.test_endpoint("/nonexistent-page", expected_status=404)
    
    def test_performance(self):
        """Test application performance"""
        print("\n⚡ Testing Performance...")
        
        # Test multiple concurrent requests to home page
        start_time = time.time()
        
        for i in range(5):
            self.test_endpoint("/")
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 5
        
        print(f"📊 Average response time for 5 requests: {avg_time:.2f}s")
        
        if avg_time < 1.0:
            print("✅ Performance: Excellent")
        elif avg_time < 2.0:
            print("⚠️ Performance: Good")
        else:
            print("❌ Performance: Needs improvement")
    
    def test_prediction_accuracy(self):
        """Test prediction functionality with various inputs"""
        print("\n🎯 Testing Prediction Accuracy...")
        
        test_cases = [
            {
                "name": "Premium Location",
                "data": {
                    "location": "Koramangala",
                    "area_type": "Super built-up Area",
                    "size": "3 BHK",
                    "total_sqft": 1500,
                    "bath": 3,
                    "balcony": 2,
                    "availability": "Ready To Move"
                }
            },
            {
                "name": "Budget Property",
                "data": {
                    "location": "Electronic City",
                    "area_type": "Built-up Area",
                    "size": "2 BHK",
                    "total_sqft": 1000,
                    "bath": 2,
                    "balcony": 1,
                    "availability": "Ready To Move"
                }
            },
            {
                "name": "Luxury Property",
                "data": {
                    "location": "Indiranagar",
                    "area_type": "Super built-up Area",
                    "size": "4 BHK",
                    "total_sqft": 2500,
                    "bath": 4,
                    "balcony": 3,
                    "availability": "Ready To Move"
                }
            }
        ]
        
        for test_case in test_cases:
            print(f"  Testing {test_case['name']}...")
            success, response = self.test_endpoint("/api/predict", "POST", test_case['data'])
            
            if success and response:
                try:
                    result = response.json()
                    if result.get('success'):
                        price = result.get('prediction', 0)
                        print(f"    Predicted price: ₹{price:.2f} Lakhs")
                    else:
                        print(f"    Error: {result.get('error', 'Unknown error')}")
                except:
                    print("    Error parsing response")
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        print("\n" + "="*60)
        print("📋 DEPLOYMENT VERIFICATION REPORT")
        print("="*60)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.results:
                if not result['success']:
                    error_msg = result.get('error', f"Status {result['status_code']}")
                    print(f"  - {result['method']} {result['endpoint']}: {error_msg}")
        
        # Performance summary
        response_times = [r.get('response_time', 0) for r in self.results if 'response_time' in r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"\n⚡ Average Response Time: {avg_response_time:.3f}s")
        
        print("\n" + "="*60)
        
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! Deployment is ready for production.")
        elif failed_tests <= 2:
            print("⚠️ Minor issues detected. Review failed tests before production.")
        else:
            print("🚨 Multiple issues detected. Fix errors before deploying to production.")
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """Run complete verification suite"""
        print("🚀 Starting Real Estate AI Deployment Verification...")
        print(f"🌐 Testing URL: {self.base_url}")
        
        # Wait for server to be ready
        print("\n⏳ Waiting for server to be ready...")
        max_retries = 10
        for i in range(max_retries):
            try:
                response = requests.get(self.base_url, timeout=5)
                if response.status_code == 200:
                    print("✅ Server is ready!")
                    break
            except:
                if i == max_retries - 1:
                    print("❌ Server is not responding. Please check if the application is running.")
                    return False
                time.sleep(2)
        
        # Run all test suites
        self.test_main_pages()
        self.test_api_endpoints()
        self.test_static_assets()
        self.test_error_pages()
        self.test_performance()
        self.test_prediction_accuracy()
        
        # Generate final report
        return self.generate_report()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify Real Estate AI deployment')
    parser.add_argument('--url', default='http://127.0.0.1:5000', 
                       help='Base URL to test (default: http://127.0.0.1:5000)')
    
    args = parser.parse_args()
    
    verifier = DeploymentVerifier(args.url)
    success = verifier.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
