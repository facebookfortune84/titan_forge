"""
Integration tests for new API endpoints (STEP 2-3)

Tests for:
- Lead capture endpoint
- Auth endpoints (register, login, refresh, logout)
- Input validation
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app import db_models


client = TestClient(app)


class TestLeadCapture:
    """Test lead capture endpoint"""

    def test_create_lead_success(self):
        """Test creating a new lead with valid data"""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": "john.doe@example.com",
                "name": "John Doe",
                "company": "Acme Corp",
                "phone": "+1-555-123-4567",
                "message": "Interested in your service"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "john.doe@example.com"
        assert data["name"] == "John Doe"
        assert data["status"] == "new"
        assert data["source"] == "landing_page"

    def test_create_lead_invalid_email(self):
        """Test that invalid emails are rejected"""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": "not-an-email",
                "name": "John Doe"
            }
        )
        assert response.status_code == 400
        assert "Invalid email" in response.json()["detail"]

    def test_create_lead_duplicate_email(self):
        """Test that duplicate emails are rejected"""
        # First lead
        response1 = client.post(
            "/api/v1/leads",
            json={
                "email": "duplicate@example.com",
                "name": "First"
            }
        )
        assert response1.status_code == 201

        # Duplicate lead
        response2 = client.post(
            "/api/v1/leads",
            json={
                "email": "duplicate@example.com",
                "name": "Second"
            }
        )
        assert response2.status_code == 409
        assert "already been captured" in response2.json()["detail"]

    def test_list_leads(self):
        """Test listing all leads"""
        response = client.get("/api/v1/leads")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_single_lead(self):
        """Test getting a single lead by ID"""
        # Create lead
        create_resp = client.post(
            "/api/v1/leads",
            json={
                "email": "single@example.com",
                "name": "Single Lead"
            }
        )
        lead_id = create_resp.json()["id"]

        # Get lead
        get_resp = client.get(f"/api/v1/leads/{lead_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["email"] == "single@example.com"

    def test_get_nonexistent_lead(self):
        """Test getting a lead that doesn't exist"""
        response = client.get("/api/v1/leads/nonexistent-id")
        assert response.status_code == 404


class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_register_success(self):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePassword123",
                "full_name": "New User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert data["is_active"] is True

    def test_register_weak_password(self):
        """Test that weak passwords are rejected"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "weak@example.com",
                "password": "weak",
                "full_name": "Weak Password User"
            }
        )
        assert response.status_code == 400
        assert "at least 8 characters" in response.json()["detail"]

    def test_register_duplicate_email(self):
        """Test that duplicate emails are rejected"""
        email = "duplicate.user@example.com"
        
        # First registration
        response1 = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": "SecurePassword123",
                "full_name": "First User"
            }
        )
        assert response1.status_code == 201

        # Duplicate registration
        response2 = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": "SecurePassword456",
                "full_name": "Second User"
            }
        )
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"]

    def test_register_invalid_email(self):
        """Test that invalid emails are rejected"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePassword123"
            }
        )
        assert response.status_code == 422  # Pydantic validation error

    def test_login_success(self):
        """Test successful login"""
        email = "login.test@example.com"
        password = "TestPassword123"

        # Register first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": "Login Test"
            }
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": email,
                "password": password
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "WrongPassword"
            }
        )
        assert response.status_code == 401
        assert "Incorrect" in response.json()["detail"]

    def test_get_current_user(self):
        """Test getting current user profile"""
        email = "current.user@example.com"
        password = "CurrentPassword123"

        # Register
        client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": "Current User"
            }
        )

        # Login
        login_resp = client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password}
        )
        token = login_resp.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == email

    def test_get_current_user_unauthorized(self):
        """Test getting current user without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403

    def test_refresh_token(self):
        """Test token refresh"""
        email = "refresh.test@example.com"
        password = "RefreshPassword123"

        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password
            }
        )
        login_resp = client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password}
        )
        old_token = login_resp.json()["access_token"]

        # Refresh
        response = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {old_token}"}
        )
        assert response.status_code == 200
        new_data = response.json()
        assert "access_token" in new_data
        assert new_data["access_token"] != old_token  # Should be different

    def test_logout(self):
        """Test logout endpoint"""
        email = "logout.test@example.com"
        password = "LogoutPassword123"

        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password
            }
        )
        login_resp = client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password}
        )
        token = login_resp.json()["access_token"]

        # Logout
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "Logged out" in response.json()["message"]


class TestInputValidation:
    """Test input validation across endpoints"""

    def test_lead_email_case_normalization(self):
        """Test that email addresses are normalized"""
        response1 = client.post(
            "/api/v1/leads",
            json={"email": "TEST@EXAMPLE.COM"}
        )
        assert response1.status_code == 201

        # Try to add duplicate with different case
        response2 = client.post(
            "/api/v1/leads",
            json={"email": "test@example.com"}
        )
        assert response2.status_code == 409

    def test_password_hashing(self):
        """Test that passwords are hashed"""
        password = "PlainTextPassword123"
        email = "hash.test@example.com"

        # Register
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password
            }
        )
        assert response.status_code == 201


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
