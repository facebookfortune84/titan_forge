import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from titanforge_backend.app import main
from titanforge_backend.app.schemas import UserResponse

client = TestClient(main.app)

def test_get_current_user(db: Session):
    # Create a user
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["email"] == "testuser@example.com"

    # Log in to get a token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    token = token_data["access_token"]

    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    
    # Validate the response using the Pydantic schema
    UserResponse.model_validate(me_data)
    
    assert me_data["email"] == "testuser@example.com"
