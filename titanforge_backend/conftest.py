"""
Pytest configuration and fixtures for TitanForge backend tests.
Handles database setup, cleanup, and test client initialization.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db

# Use PostgreSQL for tests instead of SQLite to support all types
# Falls back to in-memory if PostgreSQL unavailable
SQLALCHEMY_TEST_DATABASE_URL = "postgresql://titanforge_user:Flossie1984!@localhost:5432/titanforge_test_db"

try:
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        echo=False,
    )
    # Test connection
    with engine.connect() as conn:
        pass
    print("Using PostgreSQL for tests")
except Exception as e:
    print(f"PostgreSQL not available: {e}, using SQLite")
    # Fallback to SQLite without JSONB tables
    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Session:
    """Create and provide a test database session.
    
    Attempts to create tables but skips if JSONB types aren't supported.
    """
    from app.database import Base
    
    # Try to create tables, but handle errors gracefully
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create all tables: {e}")
        # Still proceed with testing
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        try:
            Base.metadata.drop_all(bind=engine)
        except:
            pass


@pytest.fixture(scope="function")
def client(db: Session):
    """Create and provide a test client with overridden database dependency.
    
    This ensures all API calls use the test database instead of production.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass  # Don't close here, fixture handles it

    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()

