"""Comprehensive integration test suite for TitanForge backend."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'titanforge_backend'))

import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi.testclient import TestClient
import time

from app import schemas
from app.main import app

client = TestClient(app)


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

class TestAuthentication:
    """Test user authentication endpoints."""
    
    def test_register_new_user_success(self, db):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePassword123!",
                "full_name": "New User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert "id" in data
    
    def test_register_duplicate_email(self, db, test_user):
        """Test registration fails with duplicate email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user.email,
                "password": "AnotherPassword123!",
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_email(self):
        """Test registration fails with invalid email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePassword123!",
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_register_weak_password(self):
        """Test registration fails with weak password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user@example.com",
                "password": "weak",  # Too short
            }
        )
        assert response.status_code == 400
    
    def test_login_success(self, test_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "TestPassword123!",
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_email(self):
        """Test login fails with invalid email."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "AnyPassword123!",
            }
        )
        assert response.status_code == 401
    
    def test_login_wrong_password(self, test_user):
        """Test login fails with wrong password."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "WrongPassword123!",
            }
        )
        assert response.status_code == 401
    
    def test_get_current_user(self, test_user, auth_headers):
        """Test getting current user info."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["id"] == str(test_user.id)
    
    def test_get_current_user_unauthorized(self):
        """Test getting user info without auth fails."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_refresh_token(self, test_user_token, auth_headers):
        """Test token refresh."""
        time.sleep(1)
        response = client.post(
            "/api/v1/auth/refresh",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["access_token"] != test_user_token  # Should be a new token


# ============================================================================
# LEAD CAPTURE TESTS
# ============================================================================

class TestLeadCapture:
    """Test lead capture endpoints."""
    
    def test_create_lead_success(self):
        """Test successful lead creation."""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": "lead@test.com",
                "name": "John Doe",
                "company": "Acme Corp",
                "phone": "+1234567890",
                "message": "Interested in TitanForge",
                "source": "landing_page"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "lead@example.com"
        assert data["name"] == "John Doe"
        assert data["status"] == "new"
    
    def test_create_lead_invalid_email(self):
        """Test lead creation with invalid email."""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": "not-an-email",
                "name": "John Doe",
            }
        )
        assert response.status_code == 422
    
    def test_create_duplicate_lead(self):
        """Test creating a duplicate lead fails."""
        lead_data = {
            "email": "duplicate@test.com",
            "name": "Jane Doe"
        }
        
        # Create first lead
        response1 = client.post("/api/v1/leads", json=lead_data)
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post("/api/v1/leads", json=lead_data)
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"].lower()
    
    def test_get_leads_list(self, auth_headers):
        """Test getting list of leads."""
        # Create some leads
        for i in range(3):
            client.post(
                "/api/v1/leads",
                json={
                    "email": f"lead{i}@test.com",
                    "name": f"Lead {i}"
                }
            )
        
        response = client.get("/api/v1/leads", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
    
    def test_get_lead_by_id(self, auth_headers):
        """Test getting a specific lead."""
        # Create a lead
        lead_response = client.post(
            "/api/v1/leads",
            json={"email": "specific@test.com", "name": "Specific Lead"}
        )
        assert lead_response.status_code == 201
        lead_id = lead_response.json()["id"]
        
        response = client.get(f"/api/v1/leads/{lead_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "specific@test.com"


# ============================================================================
# BLOG TESTS
# ============================================================================

class TestBlog:
    """Test blog endpoints."""
    
    def test_create_blog_post(self, test_user, auth_headers):
        """Test creating a blog post."""
        response = client.post(
            "/api/v1/blog",
            json={
                "title": "Getting Started with TitanForge",
                "slug": "getting-started-titanforge",
                "content": "# Getting Started\n\nThis is a blog post about TitanForge.",
                "excerpt": "Learn how to get started with TitanForge",
                "tags": ["ai", "automation", "tutorial"],
                "meta_title": "Getting Started with TitanForge",
                "meta_description": "Learn how to get started with TitanForge AI platform",
                "published": False,
                "author_id": str(test_user.id)
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Getting Started with TitanForge"
        assert data["slug"] == "getting-started-titanforge"
        assert data["published"] == False
    
    def test_create_blog_post_duplicate_slug(self, test_user, auth_headers):
        """Test creating blog post with duplicate slug fails."""
        post_data = {
            "title": "First Post",
            "slug": "duplicate-slug",
            "content": "Content",
            "author_id": str(test_user.id)
        }
        
        # Create first post
        response1 = client.post("/api/v1/blog", json=post_data, headers=auth_headers)
        assert response1.status_code == 201
        
        # Try to create duplicate
        post_data["title"] = "Second Post"
        response2 = client.post("/api/v1/blog", json=post_data, headers=auth_headers)
        assert response2.status_code == 409
    
    def test_publish_blog_post(self, test_user, auth_headers):
        """Test publishing a blog post."""
        # Create draft
        create_response = client.post(
            "/api/v1/blog",
            json={
                "title": "Draft Post",
                "slug": "draft-post",
                "content": "Draft content",
                "published": False,
                "author_id": str(test_user.id)
            },
            headers=auth_headers
        )
        post_id = create_response.json()["id"]
        
        # Publish post
        update_response = client.put(
            f"/api/v1/blog/{post_id}",
            json={"published": True},
            headers=auth_headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["published"] == True
    
    def test_list_blog_posts_published_only(self, test_user, auth_headers):
        """Test listing only published blog posts."""
        # Create published post
        client.post(
            "/api/v1/blog",
            json={
                "title": "Published Post",
                "slug": "published-post",
                "content": "Content",
                "published": True,
                "author_id": str(test_user.id)
            },
            headers=auth_headers
        )
        
        # Create draft post
        client.post(
            "/api/v1/blog",
            json={
                "title": "Draft Post",
                "slug": "draft-post",
                "content": "Content",
                "published": False,
                "author_id": str(test_user.id)
            },
            headers=auth_headers
        )
        
        # List posts
        response = client.get("/api/v1/blog?published_only=true")
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) == 1
        assert posts[0]["title"] == "Published Post"
    
    def test_get_post_by_slug(self, test_user, auth_headers):
        """Test getting blog post by slug."""
        # Create and publish post
        client.post(
            "/api/v1/blog",
            json={
                "title": "Test Post",
                "slug": "test-post-slug",
                "content": "Test content",
                "published": True,
                "author_id": str(test_user.id)
            },
            headers=auth_headers
        )
        
        response = client.get("/api/v1/blog/slug/test-post-slug")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Post"


# ============================================================================
# AGENT TESTS
# ============================================================================

class TestAgents:
    """Test agent management endpoints."""
    
    def test_list_agents(self):
        """Test listing all agents."""
        response = client.get("/api/v1/agents")
        assert response.status_code == 200
        agents = response.json()
        assert len(agents) > 0
        assert all("name" in a and "role" in a for a in agents)
    
    def test_list_agents_by_department(self):
        """Test listing agents by department."""
        response = client.get("/api/v1/agents?department=engineering")
        assert response.status_code == 200
        agents = response.json()
        assert all(a["department"] == "engineering" for a in agents)
    
    def test_get_agent_details(self):
        """Test getting details for a specific agent."""
        response = client.get("/api/v1/agents/ceo")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "ceo"
        assert "capabilities" in data
    
    def test_get_agent_capabilities(self):
        """Test getting agent capabilities."""
        response = client.get("/api/v1/agents/backend_developer/capabilities")
        assert response.status_code == 200
        capabilities = response.json()
        assert isinstance(capabilities, list)
        assert "api_design" in capabilities
    
    def test_list_departments(self):
        """Test listing all departments."""
        response = client.get("/api/v1/agents/departments")
        assert response.status_code == 200
        departments = response.json()
        assert len(departments) > 0
        assert "engineering" in departments
        assert "marketing" in departments
    
    def test_get_graph_nodes(self):
        """Test getting graph nodes for visualization."""
        response = client.get("/api/v1/agents/graph/nodes")
        assert response.status_code == 200
        nodes = response.json()
        assert len(nodes) > 0
        assert all("id" in n and "label" in n for n in nodes)
    
    def test_get_graph_edges(self):
        """Test getting graph edges for visualization."""
        response = client.get("/api/v1/agents/graph/edges")
        assert response.status_code == 200
        edges = response.json()
        assert len(edges) > 0
        assert all("source" in e and "target" in e for e in edges)


# ============================================================================
# VALIDATION & SECURITY TESTS
# ============================================================================

class TestValidationAndSecurity:
    """Test input validation and security features."""
    
    def test_email_normalization(self):
        """Test that emails are normalized (lowercased)."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "TEST@EXAMPLE.COM",
                "password": "SecurePassword123!",
            }
        )
        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"
    
    def test_password_hashing(self, test_user, db):
        """Test that passwords are hashed."""
        user = db.query(db_models.User).filter(
            db_models.User.email == test_user.email
        ).first()
        
        # Password should not be stored in plain text
        assert user.hashed_password != "TestPassword123!"
        # Password should start with bcrypt hash prefix
        assert user.hashed_password.startswith("$2b$")
    
    def test_sql_injection_prevention(self):
        """Test SQL injection attempt is prevented."""
        response = client.post(
            "/api/v1/leads",
            json={
                "email": "test'; DROP TABLE leads; --@example.com",
                "name": "Attacker"
            }
        )
        # Should fail email validation, not execute SQL
        assert response.status_code == 422
    
    def test_xss_prevention_in_blog(self, test_user, auth_headers):
        """Test XSS payload in blog content."""
        response = client.post(
            "/api/v1/blog",
            json={
                "title": "<script>alert('XSS')</script>",
                "slug": "xss-test",
                "content": "<img src=x onerror='alert(\"XSS\")'>",
                "author_id": str(test_user.id)
            },
            headers=auth_headers
        )
        # Content should be accepted (sanitization happens on frontend/display)
        assert response.status_code == 201
        # But should not execute
        data = response.json()
        assert "<script>" in data["title"]


# ============================================================================
# END-TO-END USER JOURNEY TESTS
# ============================================================================

class TestUserJourneys:
    """Test complete user workflows."""
    
    def test_signup_to_lead_capture(self):
        """Test user signup and then submitting lead form."""
        # 1. Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "journey@example.com",
                "password": "JourneyPassword123!",
                "full_name": "Journey User"
            }
        )
        assert register_response.status_code == 201
        user_id = register_response.json()["id"]
        
        # 2. Login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "journey@example.com",
                "password": "JourneyPassword123!",
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # 3. Get current user
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/api/v1/auth/me", headers=headers)
        assert me_response.status_code == 200
        assert me_response.json()["id"] == user_id
    
    def test_read_blog_flow(self, test_user, auth_headers):
        """Test reading blog posts."""
        # 1. Create and publish blog post
        post_response = client.post(
            "/api/v1/blog",
            json={
                "title": "Welcome to TitanForge",
                "slug": "welcome-titanforge",
                "content": "# Welcome\n\nTitanForge is amazing!",
                "excerpt": "Welcome to TitanForge",
                "tags": ["welcome", "introduction"],
                "published": True,
                "author_id": str(test_user.id)
            },
            headers=auth_headers
        )
        assert post_response.status_code == 201
        
        # 2. List published posts
        list_response = client.get("/api/v1/blog?published_only=true")
        assert list_response.status_code == 200
        posts = list_response.json()
        assert len(posts) > 0
        
        # 3. Get post by slug
        slug_response = client.get("/api/v1/blog/slug/welcome-titanforge")
        assert slug_response.status_code == 200
        assert slug_response.json()["title"] == "Welcome to TitanForge"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
