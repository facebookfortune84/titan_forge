"""Agent registry and management endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import db_models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/agents", tags=["agents"])


# Agent registry - in a production system, this would be loaded from a database
AGENT_ROSTER = {
    "ceo": {
        "name": "Chief Executive Officer",
        "role": "executive",
        "department": "executive_board",
        "description": "Overall strategic planning and goal orchestration",
        "capabilities": ["planning", "delegation", "strategy", "decision_making"],
        "status": "active",
    },
    "backend_developer": {
        "name": "Backend Developer",
        "role": "engineer",
        "department": "engineering",
        "description": "Backend API development and optimization",
        "capabilities": ["code_development", "api_design", "database_design", "testing"],
        "status": "active",
    },
    "frontend_developer": {
        "name": "Frontend Developer",
        "role": "engineer",
        "department": "engineering",
        "description": "Frontend UI/UX development",
        "capabilities": ["ui_development", "react_expertise", "responsive_design", "testing"],
        "status": "active",
    },
    "marketing_manager": {
        "name": "Marketing Manager",
        "role": "marketing",
        "department": "marketing",
        "description": "Marketing strategy and campaign management",
        "capabilities": ["strategy", "content_creation", "analytics", "lead_generation"],
        "status": "active",
    },
    "content_creator": {
        "name": "Content Creator",
        "role": "marketing",
        "department": "marketing",
        "description": "Blog posts, landing page copy, and SEO content",
        "capabilities": ["writing", "seo", "blog_creation", "copywriting"],
        "status": "active",
    },
    "data_analyst": {
        "name": "Data Analyst",
        "role": "analytics",
        "department": "analytics",
        "description": "Analytics, reporting, and business intelligence",
        "capabilities": ["analytics", "reporting", "data_visualization", "sql"],
        "status": "active",
    },
    "devops_engineer": {
        "name": "DevOps Engineer",
        "role": "infrastructure",
        "department": "infrastructure",
        "description": "Infrastructure, deployment, and system reliability",
        "capabilities": ["docker", "kubernetes", "ci_cd", "monitoring"],
        "status": "active",
    },
}


@router.get("", response_model=List[dict])
async def list_agents(
    department: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List all registered agents. Can filter by department or status."""
    agents = list(AGENT_ROSTER.values())
    
    if department:
        agents = [a for a in agents if a["department"] == department]
    
    if status:
        agents = [a for a in agents if a["status"] == status]
    
    return agents


@router.get("/departments", response_model=List[str])
async def list_departments():
    """List all available departments."""
    departments = set()
    for agent in AGENT_ROSTER.values():
        departments.add(agent["department"])
    return sorted(list(departments))


@router.get("/{agent_id}", response_model=dict)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Get details for a specific agent."""
    if agent_id not in AGENT_ROSTER:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    agent = AGENT_ROSTER[agent_id]
    return {**agent, "id": agent_id}


@router.get("/{agent_id}/capabilities", response_model=List[str])
async def get_agent_capabilities(agent_id: str, db: Session = Depends(get_db)):
    """Get the capabilities of a specific agent."""
    if agent_id not in AGENT_ROSTER:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    return AGENT_ROSTER[agent_id]["capabilities"]


@router.post("/{agent_id}/status", response_model=dict)
async def update_agent_status(
    agent_id: str,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """Update an agent's status. Requires authentication."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers can update agent status")
    
    if agent_id not in AGENT_ROSTER:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    if new_status not in ["active", "inactive", "maintenance"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    AGENT_ROSTER[agent_id]["status"] = new_status
    return {**AGENT_ROSTER[agent_id], "id": agent_id}


@router.get("/graph/nodes", response_model=List[dict])
async def get_graph_nodes(db: Session = Depends(get_db)):
    """Get all agents as graph nodes for NeuralLattice visualization."""
    nodes = []
    for agent_id, agent_data in AGENT_ROSTER.items():
        nodes.append({
            "id": agent_id,
            "label": agent_data["name"],
            "category": "AGENT",
            "department": agent_data["department"],
            "status": agent_data["status"],
            "description": agent_data["description"],
        })
    return nodes


@router.get("/graph/edges", response_model=List[dict])
async def get_graph_edges(db: Session = Depends(get_db)):
    """Get relationship edges for NeuralLattice visualization."""
    edges = [
        # CEO connects to all departments
        {"source": "ceo", "target": "backend_developer", "type": "manages"},
        {"source": "ceo", "target": "frontend_developer", "type": "manages"},
        {"source": "ceo", "target": "marketing_manager", "type": "manages"},
        {"source": "ceo", "target": "devops_engineer", "type": "manages"},
        # Cross-functional relationships
        {"source": "backend_developer", "target": "frontend_developer", "type": "collaborates"},
        {"source": "backend_developer", "target": "devops_engineer", "type": "collaborates"},
        {"source": "marketing_manager", "target": "content_creator", "type": "manages"},
        {"source": "marketing_manager", "target": "data_analyst", "type": "collaborates"},
    ]
    return edges
