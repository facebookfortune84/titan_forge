from fastapi import APIRouter, Depends
from typing import Any, Dict, List

from ... import db_models
from ...dependencies import get_current_active_user

router = APIRouter()

agent_registry: set = {
    "ceo",
    "architect",
    "engineering_manager",
    "backend_developer",
    "frontend_developer",
    "marketing_manager",
    "content_creator",
    "social_media_manager",
    "lead_generation_agent",
    "community_manager",
    "design_manager",
    "graphic_designer",
    "qa_manager",
    "test_engineer",
    "code_reviewer",
    "billing_manager",
    "hr_manager",
    "orchestrator",
    "analytics_agent",
    "provisioning_agent",
    "notification_agent",
}

@router.get("/graph")
async def get_agent_graph(
    current_user: db_models.User = Depends(get_current_active_user),
) -> Dict[str, List[Dict[str, Any]]]:
    nodes = []
    links = []

    for agent_id in agent_registry:
        nodes.append({"id": agent_id, "category": "AGENT", "sector": "general_engineering"})

    mock_tasks = {
        "task_1": {"description": "Develop new feature", "assigned_to": "backend_developer"},
        "task_2": {"description": "Design UI", "assigned_to": "frontend_developer"},
        "task_3": {"description": "Analyze market data", "assigned_to": "analytics_agent"},
    }

    for task_id, task_data in mock_tasks.items():
        nodes.append({"id": task_id, "category": "TASK", "description": task_data["description"]})
        if task_data["assigned_to"] in agent_registry:
            links.append({"source": task_id, "target": task_data["assigned_to"]})

    mock_artifacts = {
        "artifact_a": {"name": "codebase.zip", "created_by": "backend_developer"},
        "artifact_b": {"name": "design_mockup.fig", "created_by": "frontend_developer"},
    }

    for artifact_id, artifact_data in mock_artifacts.items():
        nodes.append({"id": artifact_id, "category": "ARTIFACT", "name": artifact_data["name"]})
        if artifact_data["created_by"] in agent_registry:
            links.append({"source": artifact_id, "target": artifact_data["created_by"]})
    
    return {"nodes": nodes, "links": links}
