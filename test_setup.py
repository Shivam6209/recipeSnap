#!/usr/bin/env python3
"""
Simple test script to verify RecipeSnap setup
"""

import requests
import time
import sys

def test_backend():
    """Test if backend is running"""
    try:
        print("🔍 Testing backend connection...")
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running successfully!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on port 8001?")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    try:
        print("🔍 Testing frontend connection...")
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible!")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend. Is it running on port 8000?")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def main():
    print("🚀 RecipeSnap Setup Test")
    print("=" * 40)
    
    # Wait a moment for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(3)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"   Backend (API): {'✅ OK' if backend_ok else '❌ FAILED'}")
    print(f"   Frontend (UI): {'✅ OK' if frontend_ok else '❌ FAILED'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 SUCCESS! RecipeSnap is ready to use!")
        print("   🌐 Open http://localhost:8000 in your browser")
        print("   📚 API docs: http://localhost:8001/docs")
    else:
        print("\n⚠️  Some services are not running. Check the setup:")
        if not backend_ok:
            print("   - Start backend: python start_backend.py")
        if not frontend_ok:
            print("   - Start frontend: npm start")
    
    return 0 if (backend_ok and frontend_ok) else 1

if __name__ == "__main__":
    sys.exit(main()) 