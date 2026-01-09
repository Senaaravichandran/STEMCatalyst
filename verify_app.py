#!/usr/bin/env python3
"""
STEM Problem Solver - Application Verification Script
Verifies all components are working correctly
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_backend_health():
    """Test backend health endpoint"""
    try:
        print("🔍 Testing backend health...")
        response = requests.get("http://localhost:5000/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is healthy")
            print(f"   Version: {data.get('version', 'Unknown')}")
            print(f"   Response time: {data.get('response_time_ms', 'Unknown')}ms")
            
            services = data.get('services', {})
            for service, status in services.items():
                status_emoji = "✅" if status.get('status') == 'healthy' else "⚠️"
                print(f"   {status_emoji} {service}: {status.get('status', 'unknown')}")
            
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running")
        return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_ai_service():
    """Test AI service functionality"""
    try:
        print("\n🤖 Testing AI service...")
        
        test_payload = {
            "problem": "What is 2 + 2?",
            "subject": "Mathematics",
            "difficulty": "Beginner",
            "showSteps": True,
            "includeTheory": False,
            "includeDiagrams": False,
            "temperature": 0.1
        }
        
        response = requests.post(
            "http://localhost:5000/api/solve",
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('solution'):
                print("✅ AI service is working")
                print(f"   Solution preview: {data['solution'][:100]}...")
                return True
            else:
                print("❌ AI service returned empty solution")
                return False
        else:
            print(f"❌ AI service failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI service test error: {e}")
        return False

def test_image_generation():
    """Test image generation service"""
    try:
        print("\n🎨 Testing image generation...")
        
        test_payload = {
            "prompt": "A simple mathematical diagram",
            "context": "Educational Mathematics content",
            "size": "512x512",
            "quality": "standard",
            "style": "educational"
        }
        
        response = requests.post(
            "http://localhost:5000/api/generate-image",
            json=test_payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('image_url'):
                print("✅ Image generation is working")
                print(f"   Model: {data.get('model', 'Unknown')}")
                return True
            else:
                print("❌ Image generation failed")
                print(f"   Error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Image generation service failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Image generation test error: {e}")
        return False

def test_frontend():
    """Test frontend accessibility"""
    try:
        print("\n🌐 Testing frontend...")
        response = requests.get("http://localhost:3000", timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running")
        return False
    except Exception as e:
        print(f"❌ Frontend test error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 STEM Problem Solver - Application Verification")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend", test_frontend),
        ("AI Service", test_ai_service),
        ("Image Generation", test_image_generation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
        
        # Wait between tests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"📊 Verification Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is fully functional.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
