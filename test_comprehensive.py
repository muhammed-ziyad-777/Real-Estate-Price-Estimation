#!/usr/bin/env python3
"""
Comprehensive Testing Framework for Real Estate AI
"""

import requests
import json
import time
import threading
import random
from datetime import datetime
import concurrent.futures

BASE_URL = "http://127.0.0.1:5000"

class ComprehensiveTestSuite:
    """Complete testing suite for all features"""
    
    def __init__(self):
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'performance_metrics': {},
            'security_tests': {},
            'feature_tests': {},
            'load_test_results': {}
        }
    
    def test_feature(self, name, url, method="GET", data=None, headers=None, expected_status=200):
        """Test a specific feature with detailed reporting"""
        self.results['total_tests'] += 1
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{url}", headers=headers or {}, timeout=10)
            else:
                response = requests.post(f"{BASE_URL}{url}", json=data, headers=headers or {}, timeout=10)
            
            duration = (time.time() - start_time) * 1000  # milliseconds
            success = response.status_code == expected_status
            
            if success:
                self.results['passed'] += 1
                print(f"✅ {name}: {response.status_code} ({duration:.0f}ms)")
            else:
                self.results['failed'] += 1
                print(f"❌ {name}: {response.status_code} (expected {expected_status}) ({duration:.0f}ms)")
                self.results['errors'].append({
                    'test': name,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'error': response.text[:200] if response.text else 'No response body'
                })
            
            # Store performance metrics
            self.results['performance_metrics'][name] = {
                'duration_ms': duration,
                'status_code': response.status_code,
                'success': success
            }
            
            return success, response
            
        except Exception as e:
            self.results['failed'] += 1
            duration = (time.time() - start_time) * 1000
            print(f"❌ {name}: ERROR - {str(e)} ({duration:.0f}ms)")
            self.results['errors'].append({
                'test': name,
                'error': str(e),
                'type': 'exception'
            })
            return False, None
    
    def test_all_pages(self):
        """Test all application pages"""
        print("\n🌐 Testing All Application Pages:")
        
        pages = [
            ("Home Page", "/"),
            ("Prediction Page", "/predict"),
            ("Browse Properties", "/browse-properties"),
            ("List Property", "/list-property"),
            ("Tourist Rentals", "/tourist-rentals"),
            ("List Rental", "/list-rental"),
            ("Market Trends", "/trends"),
            ("Property Comparison", "/compare"),
            ("Interactive Map", "/map"),
            ("AI Chat", "/chat"),
            ("Loan Calculator", "/loan-calculator"),
            ("Dashboard", "/dashboard"),
            ("My Properties", "/my-properties"),
            ("History", "/history"),
            ("About", "/about"),
            ("Admin Dashboard", "/admin?key=admin123")
        ]
        
        page_results = {}
        for name, url in pages:
            success, response = self.test_feature(name, url)
            page_results[name] = success
        
        self.results['feature_tests']['pages'] = page_results
        return page_results
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n🔌 Testing API Endpoints:")
        
        # Test prediction API
        prediction_data = {
            "location": "Whitefield",
            "area_type": "Super built-up Area",
            "size": "2 BHK",
            "total_sqft": 1200,
            "bath": 2,
            "balcony": 1,
            "availability": "Ready To Move"
        }
        
        api_tests = [
            ("Prediction API", "/api/predict", "POST", prediction_data),
            ("Trends API", "/api/trends/Whitefield", "GET", None),
            ("Locations API", "/api/locations", "GET", None),
            ("Location Suggestions", "/api/location-suggestions?q=white", "GET", None),
            ("Chat API", "/api/chat", "POST", {"message": "What is the price in Bangalore?"}),
            ("Loan Calculator API", "/api/loan-calculator", "POST", {
                "principal": 5000000, "rate": 8.5, "tenure": 20
            })
        ]
        
        api_results = {}
        for name, url, method, data in api_tests:
            success, response = self.test_feature(name, url, method, data)
            api_results[name] = success
            
            # Test response format for successful requests
            if success and response:
                try:
                    json_response = response.json()
                    if 'success' in json_response:
                        print(f"   📊 Response format: Valid")
                    else:
                        print(f"   ⚠️ Response format: Missing 'success' field")
                except:
                    print(f"   ⚠️ Response format: Not valid JSON")
        
        self.results['feature_tests']['apis'] = api_results
        return api_results
    
    def test_security_features(self):
        """Test security implementations"""
        print("\n🔒 Testing Security Features:")
        
        security_results = {}
        
        # Test rate limiting
        print("   Testing Rate Limiting...")
        rate_limit_success = 0
        rate_limit_blocked = 0
        
        for i in range(35):  # Try to exceed rate limit
            success, response = self.test_feature(
                f"Rate Limit Test {i+1}", 
                "/api/predict", 
                "POST", 
                {"location": "Test", "size": "1 BHK", "total_sqft": 500, "bath": 1, "balcony": 0},
                expected_status=200
            )
            if success:
                rate_limit_success += 1
            elif response and response.status_code == 429:
                rate_limit_blocked += 1
                print(f"   ✅ Rate limiting triggered after {rate_limit_success} requests")
                break
            time.sleep(0.1)
        
        security_results['rate_limiting'] = {
            'successful_requests': rate_limit_success,
            'blocked_requests': rate_limit_blocked,
            'working': rate_limit_blocked > 0
        }
        
        # Test input sanitization
        print("   Testing Input Sanitization...")
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')"
        ]
        
        sanitization_results = []
        for malicious_input in malicious_inputs:
            success, response = self.test_feature(
                f"XSS Test", 
                "/api/predict", 
                "POST", 
                {"location": malicious_input, "size": "1 BHK", "total_sqft": 500, "bath": 1, "balcony": 0}
            )
            
            if success and response:
                try:
                    json_response = response.json()
                    # Check if malicious input is reflected in response
                    response_text = json.dumps(json_response)
                    if malicious_input in response_text:
                        sanitization_results.append(False)
                        print(f"   ❌ XSS vulnerability detected with input: {malicious_input[:20]}...")
                    else:
                        sanitization_results.append(True)
                        print(f"   ✅ Input properly sanitized: {malicious_input[:20]}...")
                except:
                    sanitization_results.append(True)
        
        security_results['input_sanitization'] = {
            'tests_passed': sum(sanitization_results),
            'total_tests': len(sanitization_results),
            'working': all(sanitization_results)
        }
        
        # Test security headers
        print("   Testing Security Headers...")
        success, response = self.test_feature("Security Headers", "/")
        if success and response:
            headers = response.headers
            required_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Content-Security-Policy'
            ]
            
            header_results = {}
            for header in required_headers:
                present = header in headers
                header_results[header] = present
                print(f"   {'✅' if present else '❌'} {header}: {'Present' if present else 'Missing'}")
        
        security_results['security_headers'] = header_results
        self.results['security_tests'] = security_results
        return security_results
    
    def test_location_selection(self):
        """Test location selection functionality"""
        print("\n📍 Testing Location Selection:")
        
        location_results = {}
        pages_with_location = [
            "/predict",
            "/list-property",
            "/list-rental",
            "/tourist-rentals",
            "/trends"
        ]
        
        for page in pages_with_location:
            success, response = self.test_feature(f"Location Selection: {page}", page)
            if success and response:
                content = response.text
                has_datalist = 'datalist' in content.lower()
                has_location_dropdown = 'location-dropdown' in content.lower()
                has_location_script = 'location-selector.js' in content
                
                location_working = has_datalist or has_location_dropdown
                location_results[page] = {
                    'page_loads': True,
                    'has_datalist': has_datalist,
                    'has_dropdown': has_location_dropdown,
                    'has_script': has_location_script,
                    'location_selection_working': location_working
                }
                
                print(f"   {'✅' if location_working else '❌'} {page}: Location selection {'working' if location_working else 'not working'}")
            else:
                location_results[page] = {'page_loads': False}
        
        self.results['feature_tests']['location_selection'] = location_results
        return location_results
    
    def run_load_test(self, concurrent_users=10, requests_per_user=5):
        """Run load testing"""
        print(f"\n⚡ Running Load Test ({concurrent_users} users, {requests_per_user} requests each):")
        
        def user_simulation(user_id):
            """Simulate a user's actions"""
            user_results = []
            
            for i in range(requests_per_user):
                # Random action
                actions = [
                    ("GET", "/"),
                    ("GET", "/predict"),
                    ("POST", "/api/predict", {
                        "location": random.choice(["Whitefield", "Koramangala", "Indiranagar"]),
                        "size": random.choice(["1 BHK", "2 BHK", "3 BHK"]),
                        "total_sqft": random.randint(500, 2000),
                        "bath": random.randint(1, 3),
                        "balcony": random.randint(0, 2)
                    }),
                    ("GET", "/trends"),
                    ("GET", "/tourist-rentals")
                ]
                
                method, url, data = random.choice(actions) if len(actions[2]) == 3 else (*random.choice(actions[:2]), None)
                
                start_time = time.time()
                try:
                    if method == "GET":
                        response = requests.get(f"{BASE_URL}{url}", timeout=10)
                    else:
                        response = requests.post(f"{BASE_URL}{url}", json=data, timeout=10)
                    
                    duration = (time.time() - start_time) * 1000
                    user_results.append({
                        'success': response.status_code == 200,
                        'duration': duration,
                        'status_code': response.status_code
                    })
                    
                except Exception as e:
                    duration = (time.time() - start_time) * 1000
                    user_results.append({
                        'success': False,
                        'duration': duration,
                        'error': str(e)
                    })
                
                time.sleep(random.uniform(0.1, 0.5))  # Random delay between requests
            
            return user_results
        
        # Run concurrent users
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(user_simulation, i) for i in range(concurrent_users)]
            all_results = []
            
            for future in concurrent.futures.as_completed(futures):
                all_results.extend(future.result())
        
        total_duration = time.time() - start_time
        
        # Analyze results
        successful_requests = sum(1 for r in all_results if r['success'])
        total_requests = len(all_results)
        avg_response_time = sum(r['duration'] for r in all_results) / total_requests
        max_response_time = max(r['duration'] for r in all_results)
        min_response_time = min(r['duration'] for r in all_results)
        
        load_test_results = {
            'concurrent_users': concurrent_users,
            'requests_per_user': requests_per_user,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'success_rate': (successful_requests / total_requests) * 100,
            'total_duration': total_duration,
            'requests_per_second': total_requests / total_duration,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time
        }
        
        print(f"   📊 Total Requests: {total_requests}")
        print(f"   ✅ Successful: {successful_requests} ({load_test_results['success_rate']:.1f}%)")
        print(f"   ⚡ Requests/sec: {load_test_results['requests_per_second']:.1f}")
        print(f"   ⏱️ Avg Response: {avg_response_time:.0f}ms")
        print(f"   📈 Min/Max Response: {min_response_time:.0f}ms / {max_response_time:.0f}ms")
        
        self.results['load_test_results'] = load_test_results
        return load_test_results
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        # Overall summary
        total_tests = self.results['total_tests']
        passed = self.results['passed']
        failed = self.results['failed']
        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📈 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {failed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Performance summary
        if self.results['performance_metrics']:
            avg_response_time = sum(
                m['duration_ms'] for m in self.results['performance_metrics'].values()
            ) / len(self.results['performance_metrics'])
            
            print(f"\n⚡ PERFORMANCE SUMMARY:")
            print(f"   Average Response Time: {avg_response_time:.0f}ms")
            
            slow_tests = [
                name for name, metrics in self.results['performance_metrics'].items()
                if metrics['duration_ms'] > 1000
            ]
            if slow_tests:
                print(f"   Slow Tests (>1s): {len(slow_tests)}")
                for test in slow_tests[:5]:  # Show top 5
                    duration = self.results['performance_metrics'][test]['duration_ms']
                    print(f"     - {test}: {duration:.0f}ms")
        
        # Security summary
        if self.results['security_tests']:
            print(f"\n🔒 SECURITY SUMMARY:")
            security = self.results['security_tests']
            
            if 'rate_limiting' in security:
                rl = security['rate_limiting']
                print(f"   Rate Limiting: {'✅ Working' if rl['working'] else '❌ Not Working'}")
            
            if 'input_sanitization' in security:
                sanitization = security['input_sanitization']
                print(f"   Input Sanitization: {'✅ Working' if sanitization['working'] else '❌ Vulnerable'}")
            
            if 'security_headers' in security:
                headers = security['security_headers']
                working_headers = sum(1 for h in headers.values() if h)
                total_headers = len(headers)
                print(f"   Security Headers: {working_headers}/{total_headers} present")
        
        # Feature summary
        if self.results['feature_tests']:
            print(f"\n🎯 FEATURE SUMMARY:")
            for feature_type, features in self.results['feature_tests'].items():
                if isinstance(features, dict):
                    working_features = sum(1 for f in features.values() if f)
                    total_features = len(features)
                    print(f"   {feature_type.title()}: {working_features}/{total_features} working")
        
        # Load test summary
        if self.results['load_test_results']:
            load_results = self.results['load_test_results']
            print(f"\n⚡ LOAD TEST SUMMARY:")
            print(f"   Success Rate: {load_results['success_rate']:.1f}%")
            print(f"   Requests/Second: {load_results['requests_per_second']:.1f}")
            print(f"   Average Response: {load_results['avg_response_time']:.0f}ms")
        
        # Errors
        if self.results['errors']:
            print(f"\n❌ ERRORS ({len(self.results['errors'])}):")
            for error in self.results['errors'][:10]:  # Show first 10 errors
                print(f"   - {error['test']}: {error.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 80)
        print("🎉 TEST REPORT COMPLETE")
        print("=" * 80)
        
        return self.results

def main():
    """Run comprehensive test suite"""
    print("🧪 Starting Comprehensive Test Suite for Real Estate AI")
    print("=" * 80)
    
    test_suite = ComprehensiveTestSuite()
    
    # Run all test categories
    test_suite.test_all_pages()
    test_suite.test_api_endpoints()
    test_suite.test_security_features()
    test_suite.test_location_selection()
    test_suite.run_load_test(concurrent_users=5, requests_per_user=3)
    
    # Generate final report
    test_suite.generate_report()
    
    # Save results to file
    with open('test_results.json', 'w') as f:
        json.dump(test_suite.results, f, indent=2, default=str)
    
    print(f"\n💾 Test results saved to test_results.json")

if __name__ == "__main__":
    main()
