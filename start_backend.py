#!/usr/bin/env python3
"""
Simple script to start the RecipeSnap backend server
"""

import sys
import os
import subprocess

def main():
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    print("🚀 Starting RecipeSnap Backend Server...")
    print("📍 Backend directory:", os.getcwd())
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Copying from env.example...")
        if os.path.exists('../env.example'):
            import shutil
            shutil.copy('../env.example', '.env')
            print("✅ Created .env file from template")
        else:
            print("❌ env.example not found. Please create .env manually.")
    
    # Start the server
    try:
        subprocess.run([sys.executable, 'main.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main() 