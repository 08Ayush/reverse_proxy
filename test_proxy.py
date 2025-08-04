#!/usr/bin/env python3
"""
Test script for PAANY RAG Reverse Proxy
"""

import requests
import json
import time

# Configuration - Update these values
PROXY_URL = "http://localhost:8080"  # Change to your Render URL when deployed
API_TOKEN = "6e8b43cca9d29b261843a3b1c53382bdaa5b2c9e96db92da679278c6dc0042ca"

def test_root():
    """Test root endpoint"""
    print("🏠 Testing root endpoint...")
    try:
        response = requests.get(f"{PROXY_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Root test failed: {e}")
        return False

def test_proxy_health():
    """Test proxy health endpoint"""
    print("\n🔍 Testing proxy health...")
    try:
        response = requests.get(f"{PROXY_URL}/proxy/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Proxy health test failed: {e}")
        return False

def test_health():
    """Test basic health endpoint (forwards to AWS)"""
    print("\n🏥 Testing health endpoint (AWS forwarding)...")
    try:
        response = requests.get(f"{PROXY_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return False

def test_api_health():
    """Test comprehensive API health (forwards to AWS)"""
    print("\n🔍 Testing API health (AWS forwarding)...")
    try:
        response = requests.get(f"{PROXY_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API health test failed: {e}")
        return False

def test_main_rag_api():
    """Test main RAG API endpoint"""
    print("\n🚀 Testing main RAG API (forwards to AWS)...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    payload = {
        "documents": "Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed.",
        "questions": [
            "What is artificial intelligence?",
            "How does machine learning relate to AI?"
        ]
    }
    
    try:
        print("📤 Sending request...")
        start_time = time.time()
        
        response = requests.post(
            f"{PROXY_URL}/api/v1/hackrx/run",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        response_time = time.time() - start_time
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {response_time:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ RAG API Response:")
            if isinstance(result.get('answers'), list):
                for i, answer in enumerate(result['answers']):
                    print(f"  Q{i+1}: {answer[:200]}...")
            else:
                print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ API Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Main API test failed: {e}")
        return False

def test_redis_status():
    """Test Redis status endpoint"""
    print("\n📊 Testing Redis status (forwards to AWS)...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    try:
        response = requests.get(f"{PROXY_URL}/redis-status", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Redis status test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 PAANY RAG REVERSE PROXY TEST SUITE")
    print("=" * 60)
    print(f"🎯 Target URL: {PROXY_URL}")
    print("=" * 60)
    
    tests = [
        ("Root Endpoint", test_root),
        ("Proxy Health", test_proxy_health),
        ("Basic Health (AWS)", test_health),
        ("API Health (AWS)", test_api_health),
        ("Redis Status (AWS)", test_redis_status),
        ("Main RAG API (AWS)", test_main_rag_api),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your reverse proxy is working correctly.")
    elif passed > total // 2:
        print("⚠️  Most tests passed. Check failed tests for issues.")
    else:
        print("❌ Many tests failed. Check your AWS instance and configuration.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
