#!/usr/bin/env python
"""
Comprehensive test suite for Day-7 Authentication API
Tests all endpoints and role-based access control
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
test_results = []

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test(name, method, endpoint, data=None, headers=None, expected_status=None):
    """Helper function to test endpoints"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            return None
        
        status = "✅" if (expected_status is None or response.status_code == expected_status) else "❌"
        success = (expected_status is None or response.status_code == expected_status)
        
        print(f"{status} {name}")
        print(f"   Method: {method} | Endpoint: {endpoint}")
        print(f"   Status: {response.status_code} (Expected: {expected_status})")
        
        try:
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
        except:
            print(f"   Response: {response.text[:200]}")
        
        test_results.append({
            "test": name,
            "endpoint": endpoint,
            "method": method,
            "status": response.status_code,
            "expected": expected_status,
            "passed": success
        })
        
        return response
        
    except Exception as e:
        print(f"❌ {name}")
        print(f"   Error: {str(e)}")
        test_results.append({
            "test": name,
            "endpoint": endpoint,
            "method": method,
            "status": "ERROR",
            "expected": expected_status,
            "passed": False
        })
        return None

# Test 1: Root endpoint
print_section("TEST 1: ROOT ENDPOINT")
test("Root Endpoint", "GET", "/", expected_status=200)

# Test 2: User Registration
print_section("TEST 2: USER REGISTRATION")
user_data = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "mysecretpassword",
    "role": "user"
}
resp = test("Register Normal User", "POST", "/auth/register", data=user_data, expected_status=201)

admin_data = {
    "username": "adminuser",
    "email": "admin@example.com",
    "password": "adminsecret",
    "role": "admin"
}
test("Register Admin User", "POST", "/auth/register", data=admin_data, expected_status=200)

moderator_data = {
    "username": "moderatoruser",
    "email": "moderator@example.com",
    "password": "modsecret",
    "role": "moderator"
}
test("Register Moderator User", "POST", "/auth/register", data=moderator_data, expected_status=200)

# Test 3: Duplicate Registration
print_section("TEST 3: ERROR HANDLING - DUPLICATE USER")
test("Duplicate Registration (Should Fail)", "POST", "/auth/register", data=user_data, expected_status=400)

# Test 4: Login (using form-data)
print_section("TEST 4: USER LOGIN")
# OAuth2PasswordRequestForm requires form-data, not JSON
login_resp = None
try:
    login_resp = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "johndoe", "password": "mysecretpassword"}
    )
    status_code = login_resp.status_code
    success = (status_code == 200)
    status = "✅" if success else "❌"
    print(f"{status} User Login")
    print(f"   Method: POST | Endpoint: /auth/login")
    print(f"   Status: {status_code} (Expected: 200)")
    try:
        result = login_resp.json()
        print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
    except:
        print(f"   Response: {login_resp.text[:200]}")
    test_results.append({"test": "User Login", "endpoint": "/auth/login", "method": "POST", "status": status_code, "expected": 200, "passed": success})
except Exception as e:
    print(f"❌ User Login\n   Error: {str(e)}")
    test_results.append({"test": "User Login", "endpoint": "/auth/login", "method": "POST", "status": "ERROR", "expected": 200, "passed": False})
user_token = None
if login_resp and login_resp.status_code == 200:
    user_token = login_resp.json().get("access_token")
    print(f"   📌 Access Token obtained: {user_token[:20]}..." if user_token else "   ⚠️  No token in response")

# Admin Login (form-data)
print("Testing Admin Login...")
try:
    admin_resp = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "adminuser", "password": "adminsecret"}
    )
    status_code = admin_resp.status_code
    success = (status_code == 200)
    status = "✅" if success else "❌"
    print(f"{status} Admin Login")
    print(f"   Status: {status_code} (Expected: 200)")
    test_results.append({"test": "Admin Login", "endpoint": "/auth/login", "method": "POST", "status": status_code, "expected": 200, "passed": success})
except Exception as e:
    print(f"❌ Admin Login\n   Error: {str(e)}")
    test_results.append({"test": "Admin Login", "endpoint": "/auth/login", "method": "POST", "status": "ERROR", "expected": 200, "passed": False})
    admin_resp = None

admin_token = None
if admin_resp and admin_resp.status_code == 200:
    admin_token = admin_resp.json().get("access_token")
    print(f"   📌 Admin Token obtained: {admin_token[:20]}..." if admin_token else "   ⚠️  No token in response")

# Moderator Login (form-data)
print("Testing Moderator Login...")
try:
    mod_resp = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "moderatoruser", "password": "modsecret"}
    )
    status_code = mod_resp.status_code
    success = (status_code == 200)
    status = "✅" if success else "❌"
    print(f"{status} Moderator Login")
    print(f"   Status: {status_code} (Expected: 200)")
    test_results.append({"test": "Moderator Login", "endpoint": "/auth/login", "method": "POST", "status": status_code, "expected": 200, "passed": success})
except Exception as e:
    print(f"❌ Moderator Login\n   Error: {str(e)}")
    test_results.append({"test": "Moderator Login", "endpoint": "/auth/login", "method": "POST", "status": "ERROR", "expected": 200, "passed": False})
    mod_resp = None

mod_token = None
if mod_resp and mod_resp.status_code == 200:
    mod_token = mod_resp.json().get("access_token")
    print(f"   📌 Moderator Token obtained: {mod_token[:20]}..." if mod_token else "   ⚠️  No token in response")

# Test 5: Invalid Login (form-data)
print_section("TEST 5: ERROR HANDLING - INVALID LOGIN")
try:
    invalid_resp = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "johndoe", "password": "wrongpassword"}
    )
    status_code = invalid_resp.status_code
    success = (status_code == 401)
    status = "✅" if success else "❌"
    print(f"{status} Invalid Password (Should Fail)")
    print(f"   Status: {status_code} (Expected: 401)")
    test_results.append({"test": "Invalid Password (Should Fail)", "endpoint": "/auth/login", "method": "POST", "status": status_code, "expected": 401, "passed": success})
except Exception as e:
    print(f"❌ Invalid Password\n   Error: {str(e)}")
    test_results.append({"test": "Invalid Password (Should Fail)", "endpoint": "/auth/login", "method": "POST", "status": "ERROR", "expected": 401, "passed": False})

# Test 6: Get Current User
print_section("TEST 6: PROTECTED ENDPOINTS - GET CURRENT USER")
if user_token:
    headers = {"Authorization": f"Bearer {user_token}"}
    test("Get Current User (User)", "GET", "/users/me", headers=headers, expected_status=200)

if admin_token:
    headers = {"Authorization": f"Bearer {admin_token}"}
    test("Get Current User (Admin)", "GET", "/users/me", headers=headers, expected_status=200)

# Test 7: Missing Token
print_section("TEST 7: ERROR HANDLING - MISSING TOKEN")
test("Access Protected Route Without Token (Should Fail)", "GET", "/users/me", expected_status=403)

# Test 8: Admin Dashboard
print_section("TEST 8: ADMIN-ONLY ENDPOINT")
if admin_token:
    headers = {"Authorization": f"Bearer {admin_token}"}
    test("Admin Dashboard (Admin Access)", "GET", "/users/admin-dashboard", headers=headers, expected_status=200)

if user_token:
    headers = {"Authorization": f"Bearer {user_token}"}
    test("Admin Dashboard (User Access - Should Fail)", "GET", "/users/admin-dashboard", headers=headers, expected_status=403)

# Test 9: Moderator Panel
print_section("TEST 9: MODERATOR/ADMIN ENDPOINT")
if mod_token:
    headers = {"Authorization": f"Bearer {mod_token}"}
    test("Moderator Panel (Moderator Access)", "GET", "/users/moderator-panel", headers=headers, expected_status=200)

if admin_token:
    headers = {"Authorization": f"Bearer {admin_token}"}
    test("Moderator Panel (Admin Access)", "GET", "/users/moderator-panel", headers=headers, expected_status=200)

if user_token:
    headers = {"Authorization": f"Bearer {user_token}"}
    test("Moderator Panel (User Access - Should Fail)", "GET", "/users/moderator-panel", headers=headers, expected_status=403)

# Test 10: Token Refresh
print_section("TEST 10: TOKEN REFRESH")
if login_resp and login_resp.status_code == 200:
    refresh_token = login_resp.json().get("refresh_token")
    if refresh_token:
        refresh_data = {"refresh_token": refresh_token}
        refresh_resp = test("Refresh Token", "POST", "/auth/refresh", data=refresh_data, expected_status=200)
        if refresh_resp and refresh_resp.status_code == 200:
            new_token = refresh_resp.json().get("access_token")
            print(f"   📌 New Token obtained: {new_token[:20]}..." if new_token else "   ⚠️  No token in response")
            
            # Test with new token
            headers = {"Authorization": f"Bearer {new_token}"}
            test("Access with Refreshed Token", "GET", "/users/me", headers=headers, expected_status=200)

# Summary
print_section("TEST SUMMARY")
total_tests = len(test_results)
passed_tests = sum(1 for t in test_results if t["passed"])
failed_tests = total_tests - passed_tests

print(f"Total Tests: {total_tests}")
print(f"✅ Passed: {passed_tests}")
print(f"❌ Failed: {failed_tests}")
print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

print("\n" + "="*70)
print("DETAILED RESULTS:")
print("="*70)
for result in test_results:
    status = "✅" if result["passed"] else "❌"
    print(f"{status} {result['test']:<40} | {result['method']:<6} {result['endpoint']:<25}")

print("\n" + "="*70)
print("Test execution completed at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("="*70)
