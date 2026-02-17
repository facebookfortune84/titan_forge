from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Literal
from pydantic import BaseModel
from datetime import datetime
import redis

from ... import crud, db_models, schemas, security
from ...database import get_db
from ...dependencies import get_current_active_user, send_agent_message
from ...redis_client import get_redis
from swarm.departments.executive_board.ceo import CEO
from ...core.config import settings

router = APIRouter()

class Goal(BaseModel):
    description: str

class TaskUpdate(BaseModel):
    status: Literal["in_progress", "completed", "failed"]
    agent_id: str

@router.post("/goals")
async def submit_goal(
    goal: Goal,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
    r: redis.Redis = Depends(get_redis),
):
    print(f"MCP Received new goal from user {current_user.email}: {goal.description}")
    try:
        new_task = db_models.Task(
            description=goal.description,
            status="pending",
            created_at=datetime.utcnow(),
            history=[{"status": "pending", "timestamp": datetime.utcnow().isoformat()}],
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        task_id = str(new_task.id)

        send_agent_message(
            recipient_id="analytics_agent",
            sender_id="mcp",
            message_content={
                "action": "record_event",
                "event_type": "goal_submitted",
                "user_id": str(current_user.id),
                "payload": {"task_id": task_id, "goal_description": goal.description},
            },
            r=r,
        )

        ceo_agent = CEO(model_name=settings.LLM_MODEL_NAME)
        task_description_with_id = f"Task ID: {task_id}. Goal: {goal.description}"
        result = ceo_agent.execute_task(task_description_with_id)

        return {
            "message": "Goal received and task created.",
            "task_id": task_id,
            "ceo_response": result,
        }
    except Exception as e:
        db.rollback()
        send_agent_message(
            recipient_id="notification_agent",
            sender_id="mcp",
            message_content={
                "action": "process_notification_request",
                "notification_type": "internal_error",
                "data": {
                    "error_message": f"Failed to process goal for user {current_user.email}: {e}"
                },
            },
            r=r,
        )
        raise HTTPException(status_code=500, detail=f"Failed to process goal: {e}")

@router.get("/tasks", response_model=List[Dict[str, Any]])
async def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    tasks = db.query(db_models.Task).all()
    return [
        {
            "id": str(task.id),
            "description": task.description,
            "status": task.status,
            "created_at": task.created_at,
            "history": task.history,
        }
        for task in tasks
    ]

@router.put("/tasks/{task_id}")
async def update_task_status(
    task_id: str,
    update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    task = db.query(db_models.Task).filter(db_models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    task.status = update.status
    new_history = task.history + [
        {
            "status": update.status,
            "agent_id": update.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
    ]
    task.history = new_history

    db.commit()
    return {"message": f"Task {task_id} status updated to {update.status}"}
