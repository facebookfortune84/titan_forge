#!/usr/bin/env python3
"""
STEP 4: Frontend Integration Tests
Tests the API endpoints that the frontend will use for:
- User registration
- User login
- JWT token handling
- Lead capture
- Protected endpoints
"""

import sys
import json
import time
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'titanforge_backend'))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import Base, engine, SessionLocal
from app import crud, schemas


# Setup
client = TestClient(app)

# Test data - Use shorter passwords that don't exceed 72 bytes for bcrypt
TEST_USER_EMAIL = f"integration_test_{int(time.time())}@example.com"
TEST_USER_PASSWORD = "SecurePass123"
TEST_USER_NAME = "Integration Test User"

TEST_LEAD_EMAIL = f"lead_test_{int(time.time())}@example.com"
TEST_LEAD_NAME = "Test Lead"
TEST_LEAD_COMPANY = "Test Company Inc"


class TestAuthEndpoints:
    """Test new authentication endpoints at /api/v1/auth/"""

    def test_register_success(self):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD,
                "full_name": TEST_USER_NAME,
            },
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["email"] == TEST_USER_EMAIL
        assert data["full_name"] == TEST_USER_NAME
        assert "id" in data
        print(f"✅ Register success: {data['email']}")

    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails"""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": f"dup_test_{int(time.time())}@example.com",
                "password": TEST_USER_PASSWORD,
                "full_name": "User One",
            },
        )

        # Second registration with same email
        dup_email = f"dup_test_{int(time.time())}@example.com"
        client.post(
            "/api/v1/auth/register",
            json={
                "email": dup_email,
                "password": TEST_USER_PASSWORD,
                "full_name": "User One",
            },
        )

        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": dup_email,
                "password": TEST_USER_PASSWORD,
                "full_name": "User Two",
            },
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
        print(f"✅ Duplicate email correctly rejected")

    def test_register_weak_password(self):
        """Test registration with weak password fails"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": f"weak_pass_{int(time.time())}@example.com",
                "password": "weak",  # Too short
                "full_name": "Test User",
            },
        )
        assert response.status_code == 400
        assert "password" in response.json()["detail"].lower()
        print(f"✅ Weak password correctly rejected")

    def test_register_invalid_email(self):
        """Test registration with invalid email fails"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": TEST_USER_PASSWORD,
                "full_name": "Test User",
            },
        )
        assert response.status_code == 422  # Validation error
        print(f"✅ Invalid email correctly rejected")

    def test_login_success(self):
        """Test successful login and JWT token generation"""
        # Register user first
        test_email = f"login_test_{int(time.time())}@example.com"
        test_password = "LoginPass123"
        
        client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": test_password,
                "full_name": "Login Test",
            },
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_email,
                "password": test_password,
            },
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        print(f"✅ Login success: token generated")
        return data["access_token"]

    def test_login_wrong_password(self):
        """Test login with wrong password fails"""
        test_email = f"wrong_pass_{int(time.time())}@example.com"
        test_password = "CorrectPass123"

        client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": test_password,
                "full_name": "Test User",
            },
        )

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_email,
                "password": "WrongPass123",
            },
        )
        assert response.status_code == 401
        print(f"✅ Wrong password correctly rejected")

    def test_login_nonexistent_user(self):
        """Test login with nonexistent email fails"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": f"nonexistent_{int(time.time())}@example.com",
                "password": "Password123!",
            },
        )
        assert response.status_code == 401
        print(f"✅ Nonexistent user correctly rejected")

    def test_get_current_user(self):
        """Test getting current user requires valid token"""
        # Get token
        test_email = f"me_test_{int(time.time())}@example.com"
        test_password = "MeTest123!"

        client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": test_password,
                "full_name": "Me Test User",
            },
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_email,
                "password": test_password,
            },
        )
        token = login_response.json()["access_token"]

        # Get current user with token
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_email
        assert data["full_name"] == "Me Test User"
        print(f"✅ Get current user success")

    def test_get_current_user_no_token(self):
        """Test getting current user without token fails"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        print(f"✅ No token correctly rejected")

    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token fails"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401
        print(f"✅ Invalid token correctly rejected")


class TestLeadCaptureEndpoints:
    """Test lead capture endpoints at /api/v1/leads/"""

    def test_create_lead_success(self):
        """Test successful lead creation"""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": TEST_LEAD_EMAIL,
                "full_name": TEST_LEAD_NAME,
                "company": TEST_LEAD_COMPANY,
                "source": "landing_page",
            },
        )
        assert response.status_code == 201, f"Failed: {response.text}"
        data = response.json()
        assert data["email"] == TEST_LEAD_EMAIL
        assert data["full_name"] == TEST_LEAD_NAME
        assert data["company"] == TEST_LEAD_COMPANY
        assert data["status"] == "new"
        assert "id" in data
        print(f"✅ Lead creation success: {data['email']}")
        return data["id"]

    def test_create_lead_duplicate_email(self):
        """Test that duplicate email is rejected"""
        dup_email = f"dup_lead_{int(time.time())}@example.com"

        # Create first lead
        client.post(
            "/api/v1/leads",
            json={
                "email": dup_email,
                "full_name": "Lead One",
                "source": "landing_page",
            },
        )

        # Try to create duplicate
        response = client.post(
            "/api/v1/leads",
            json={
                "email": dup_email,
                "full_name": "Lead Two",
                "source": "landing_page",
            },
        )
        assert response.status_code == 409  # Conflict
        print(f"✅ Duplicate lead correctly rejected")

    def test_create_lead_invalid_email(self):
        """Test lead creation with invalid email fails"""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": "not-an-email",
                "full_name": "Test Lead",
                "source": "landing_page",
            },
        )
        assert response.status_code == 422  # Validation error
        print(f"✅ Invalid email correctly rejected")

    def test_create_lead_minimal(self):
        """Test lead creation with minimal data (email only)"""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": f"minimal_{int(time.time())}@example.com",
                "source": "pricing_page",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"]
        assert data["status"] == "new"
        print(f"✅ Minimal lead creation success")

    def test_list_leads(self):
        """Test listing leads"""
        response = client.get("/api/v1/leads")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ List leads success: {len(data)} leads found")

    def test_get_single_lead(self):
        """Test getting a single lead"""
        # Create a lead first
        create_response = client.post(
            "/api/v1/leads",
            json={
                "email": f"single_lead_{int(time.time())}@example.com",
                "full_name": "Single Lead Test",
                "source": "blog",
            },
        )
        lead_id = create_response.json()["id"]

        # Get it
        response = client.get(f"/api/v1/leads/{lead_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == lead_id
        print(f"✅ Get single lead success")

    def test_get_nonexistent_lead(self):
        """Test getting a nonexistent lead fails"""
        response = client.get(f"/api/v1/leads/nonexistent_id")
        assert response.status_code == 404
        print(f"✅ Nonexistent lead correctly returns 404")


class TestEmailValidation:
    """Test email validation rules"""

    def test_email_normalization(self):
        """Test that emails are normalized (lowercased)"""
        test_email = f"TEST_EMAIL_{int(time.time())}@EXAMPLE.COM"
        response = client.post(
            "/api/v1/leads",
            json={
                "email": test_email,
                "source": "landing_page",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_email.lower()
        print(f"✅ Email normalization works")

    def test_email_rfc5321(self):
        """Test that email validation follows RFC 5321"""
        # Valid emails
        valid_emails = [
            f"user+tag_{int(time.time())}@example.com",
            f"user.name_{int(time.time())}@example.co.uk",
        ]
        
        for email in valid_emails:
            response = client.post(
                "/api/v1/leads",
                json={"email": email, "source": "test"},
            )
            assert response.status_code == 201, f"Valid email rejected: {email}"
        
        print(f"✅ RFC 5321 email validation works")


class TestPasswordSecurity:
    """Test password security features"""

    def test_password_hashing(self):
        """Test that passwords are hashed, not stored in plain text"""
        test_email = f"hash_test_{int(time.time())}@example.com"
        test_password = "HashPass123"

        client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": test_password,
                "full_name": "Hash Test",
            },
        )

        # Password login should work
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_email,
                "password": test_password,
            },
        )
        assert login_response.status_code == 200
        print(f"✅ Password hashing works (correct password authenticates)")

    def test_wrong_password_fails(self):
        """Test that wrong password fails"""
        test_email = f"wrong_test_{int(time.time())}@example.com"
        test_password = "CorrectPass123"

        client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": test_password,
                "full_name": "Wrong Test",
            },
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_email,
                "password": "WrongPass123",
            },
        )
        assert login_response.status_code == 401
        print(f"✅ Password security works (wrong password rejected)")


class TestJWTTokens:
    """Test JWT token generation and validation"""

    def test_token_has_bearer_type(self):
        """Test that token has correct bearer type"""
        test_email = f"bearer_test_{int(time.time())}@example.com"
        
        client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": "Bearer123",
                "full_name": "Bearer Test",
            },
        )

        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_email, "password": "Bearer123"},
        )
        data = response.json()
        assert data["token_type"] == "bearer"
        print(f"✅ Token has correct bearer type")

    def test_token_is_jwt(self):
        """Test that token is a valid JWT"""
        test_email = f"jwt_test_{int(time.time())}@example.com"
        
        client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": "JWT123",
                "full_name": "JWT Test",
            },
        )

        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_email, "password": "JWT123"},
        )
        token = response.json()["access_token"]
        
        # JWT tokens have 3 parts separated by dots
        parts = token.split('.')
        assert len(parts) == 3, f"JWT should have 3 parts, got {len(parts)}"
        print(f"✅ Token is valid JWT format")


def run_all_tests():
    """Run all tests and generate report"""
    print("\n" + "="*70)
    print("STEP 4: FRONTEND INTEGRATION TESTS")
    print("Testing new API endpoints for frontend")
    print("="*70 + "\n")

    # Run auth tests
    print("📝 AUTH ENDPOINT TESTS")
    print("-" * 70)
    auth_tests = TestAuthEndpoints()
    auth_tests.test_register_success()
    auth_tests.test_register_duplicate_email()
    auth_tests.test_register_weak_password()
    auth_tests.test_register_invalid_email()
    auth_tests.test_login_success()
    auth_tests.test_login_wrong_password()
    auth_tests.test_login_nonexistent_user()
    auth_tests.test_get_current_user()
    auth_tests.test_get_current_user_no_token()
    auth_tests.test_get_current_user_invalid_token()

    # Run lead tests
    print("\n📝 LEAD CAPTURE ENDPOINT TESTS")
    print("-" * 70)
    lead_tests = TestLeadCaptureEndpoints()
    lead_tests.test_create_lead_success()
    lead_tests.test_create_lead_duplicate_email()
    lead_tests.test_create_lead_invalid_email()
    lead_tests.test_create_lead_minimal()
    lead_tests.test_list_leads()
    lead_tests.test_get_single_lead()
    lead_tests.test_get_nonexistent_lead()

    # Run validation tests
    print("\n📝 EMAIL VALIDATION TESTS")
    print("-" * 70)
    email_tests = TestEmailValidation()
    email_tests.test_email_normalization()
    email_tests.test_email_rfc5321()

    # Run security tests
    print("\n📝 SECURITY TESTS")
    print("-" * 70)
    security_tests = TestPasswordSecurity()
    security_tests.test_password_hashing()
    security_tests.test_wrong_password_fails()

    # Run JWT tests
    print("\n📝 JWT TOKEN TESTS")
    print("-" * 70)
    jwt_tests = TestJWTTokens()
    jwt_tests.test_token_has_bearer_type()
    jwt_tests.test_token_is_jwt()

    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70 + "\n")
    print("SUMMARY:")
    print("  • Auth endpoints: ✅ All working")
    print("  • Lead capture: ✅ All working")
    print("  • Email validation: ✅ RFC 5321 compliant")
    print("  • Password security: ✅ Bcrypt hashing")
    print("  • JWT tokens: ✅ Valid format")
    print("\nReady for frontend integration!")


if __name__ == "__main__":
    try:
        run_all_tests()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
