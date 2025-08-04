#!/usr/bin/env python3
"""
Simple test script to check if the app can start
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

try:
    print("Testing imports...")
    
    # Test basic imports
    import flask
    print("✅ Flask imported")
    
    import pandas as pd
    print("✅ Pandas imported")
    
    import numpy as np
    print("✅ NumPy imported")
    
    # Test our modules
    try:
        from utils.ml_utils import load_model_and_data
        print("✅ ML utils imported")
    except Exception as e:
        print(f"❌ ML utils error: {e}")
    
    try:
        from routes.main_routes import main_bp
        print("✅ Main routes imported")
    except Exception as e:
        print(f"❌ Main routes error: {e}")
    
    try:
        from routes.api_routes import api_bp
        print("✅ API routes imported")
    except Exception as e:
        print(f"❌ API routes error: {e}")
    
    # Test app creation
    try:
        from app import create_app
        app = create_app()
        print("✅ App created successfully")
        
        # Test basic route
        with app.test_client() as client:
            response = client.get('/')
            print(f"✅ Home route status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ App creation error: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")
