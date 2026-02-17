from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import json
import redis

from ... import db_models
from ...dependencies import get_current_active_user
from ...redis_client import get_redis

router = APIRouter()

class SendMessage(BaseModel):
    sender_id: str
    recipient_id: str
    message: str

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

@router.post("/send")
async def send_message(
    item: SendMessage,
    r: redis.Redis = Depends(get_redis),
    current_user: db_models.User = Depends(get_current_active_user),
):
    if item.recipient_id not in agent_registry:
        raise HTTPException(
            status_code=404, detail=f"Recipient agent '{item.recipient_id}' not found."
        )

    message_content = json.dumps(
        {
            "sender_id": item.sender_id,
            "message": item.message,
            "user_id": str(current_user.id),
        }
    )
    r.rpush(item.recipient_id, message_content)

    return {"message": f"Message queued for agent '{item.recipient_id}'."}

@router.get("/receive/{agent_id}")
async def receive_message(
    agent_id: str,
    r: redis.Redis = Depends(get_redis),
    current_user: db_models.User = Depends(get_current_active_user),
):
    if agent_id not in agent_registry:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found.")

    message = r.lpop(agent_id)
    if message:
        return {"message": json.loads(message)}

    return {"message": None}

class SpeakRequest(BaseModel):
    text: str

@router.post("/speak")
async def speak(request: SpeakRequest):
    # This endpoint is not fully implemented in the original code
    # I will leave it as a placeholder
    return {"message": "Speak endpoint not implemented"}
