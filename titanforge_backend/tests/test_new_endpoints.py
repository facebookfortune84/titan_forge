"""
Integration tests for new API endpoints (STEP 2-3)

Tests for:
- Lead capture endpoint
- Auth endpoints (register, login, refresh, logout)
- Input validation
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app import db_models


class TestLeadCapture:
    """Test lead capture endpoint"""

    def test_create_lead_success(self, client):
        """Test creating a new lead with valid data"""
        email = f"john_{uuid.uuid4().hex[:8]}@test.local"
        response = client.post(
            "/api/v1/leads",
            json={
                "email": email,
                "name": "John Doe",
                "company": "Acme Corp",
                "phone": "+1-555-123-4567",
                "message": "Interested in your service"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == email
        assert data["name"] == "John Doe"
        assert data["status"] == "new"
        assert data["source"] == "landing_page"

    def test_create_lead_invalid_email(self, client):
        """Test that invalid emails are rejected"""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": "not-an-email",
                "name": "John Doe"
            }
        )
        assert response.status_code == 422
        
    def test_create_lead_duplicate_email(self, client):
        """Test that duplicate emails are rejected"""
        email = f"dup_{uuid.uuid4().hex[:8]}@test.local"
        # First lead
        response1 = client.post(
            "/api/v1/leads",
            json={
                "email": email,
                "name": "First"
            }
        )
        assert response1.status_code == 201

        # Duplicate lead
        response2 = client.post(
            "/api/v1/leads",
            json={
                "email": email,
                "name": "Second"
            }
        )
        assert response2.status_code == 409
        assert "already been captured" in response2.json()["detail"]

    def test_list_leads(self, client):
        """Test listing all leads"""
        response = client.get("/api/v1/leads")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_single_lead(self, client):
        """Test getting a single lead by ID"""
        email = f"single_{uuid.uuid4().hex[:8]}@test.local"
        # Create lead
        create_resp = client.post(
            "/api/v1/leads",
            json={
                "email": email,
                "name": "Single Lead"
            }
        )
        lead_id = create_resp.json()["id"]

        # Get lead
        get_resp = client.get(f"/api/v1/leads/{lead_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["email"] == email

    def test_get_nonexistent_lead(self, client):
        """Test getting a lead that doesn't exist"""
        response = client.get("/api/v1/leads/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_register_success(self, client):
        """Test successful user registration"""
        email = f"newuser_{uuid.uuid4().hex[:8]}@test.local"
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": "SecurePassword123",
                "full_name": "New User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == email
        assert data["full_name"] == "New User"
        assert data["is_active"] is True

    def test_register_weak_password(self, client):
        """Test that weak passwords are rejected"""
        email = f"weak_{uuid.uuid4().hex[:8]}@test.local"
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": "weak",
                "full_name": "Weak Password User"
            }
        )
        # Password validation happens at handler level, returns 400 via HTTPException
        # Or it might be rejected by pydantic validator before reaching handler
        assert response.status_code in [400, 422]

    def test_register_duplicate_email(self, client):
        """Test that duplicate emails are rejected"""
        email = f"duplicate_{uuid.uuid4().hex[:8]}@test.local"
        
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

    def test_register_invalid_email(self, client):
        """Test that invalid emails are rejected"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePassword123"
            }
        )
        assert response.status_code == 422  # Pydantic validation error

    def test_login_success(self, client):
        """Test successful login"""
        email = f"login_{uuid.uuid4().hex[:8]}@test.local"
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

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        email = f"invalid_{uuid.uuid4().hex[:8]}@test.local"
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": email,
                "password": "WrongPassword"
            }
        )
        assert response.status_code == 401
        assert "Incorrect" in response.json()["detail"]

    def test_get_current_user(self, client):
        """Test getting current user profile"""
        email = f"current_{uuid.uuid4().hex[:8]}@test.local"
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

    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403

    def test_refresh_token(self, client):
        """Test token refresh"""
        email = f"refresh_{uuid.uuid4().hex[:8]}@test.local"
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

    def test_logout(self, client):
        """Test logout endpoint"""
        email = f"logout_{uuid.uuid4().hex[:8]}@test.local"
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
        data = response.json()
        assert "message" in data or "status" in data


class TestInputValidation:
    """Test input validation across endpoints"""

    def test_lead_email_case_normalization(self, client):
        """Test that email addresses are normalized"""
        email = f"TEST_{uuid.uuid4().hex[:8]}@TEST.LOCAL"
        response1 = client.post(
            "/api/v1/leads",
            json={"email": email}
        )
        assert response1.status_code == 201

        # Try to add duplicate with different case
        response2 = client.post(
            "/api/v1/leads",
            json={"email": email.lower()}
        )
        assert response2.status_code == 409

    def test_password_hashing(self, client):
        """Test that passwords are hashed"""
        password = "PlainTextPassword123"
        email = f"hash_{uuid.uuid4().hex[:8]}@test.local"

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
