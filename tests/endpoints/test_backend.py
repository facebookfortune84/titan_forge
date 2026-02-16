#!/usr/bin/env python
"""Quick backend test to verify it starts properly."""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'titanforge_backend'))

try:
    print("Testing imports...")
    from app.main import app
    print("✅ FastAPI app imported successfully")
    
    from app.core.config import settings
    print("✅ Settings imported successfully")
    print(f"   DATABASE_URL: {settings.DATABASE_URL[:50]}...")
    print(f"   REDIS_URL: {settings.REDIS_URL}")
    
    from app import db_models
    print("✅ Database models imported successfully")
    
    print("\n✅ All imports successful!")
    print("\nBackend is ready. You can now run:")
    print("  python -m uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
