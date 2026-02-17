from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import redis

from ... import db_models
from ...dependencies import get_current_active_user
from ...redis_client import get_redis

router = APIRouter()

class ShortTermMemoryAdd(BaseModel):
    agent_id: str
    key: str
    value: str

@router.post("/short_term/add")
async def add_to_short_term_memory(
    item: ShortTermMemoryAdd,
    r: redis.Redis = Depends(get_redis),
    current_user: db_models.User = Depends(get_current_active_user),
):
    r.hset(f"short_term_memory:{item.agent_id}", item.key, item.value)
    return {"message": "Data added to short-term memory."}

@router.get("/short_term/{agent_id}")
async def get_from_short_term_memory(
    agent_id: str,
    r: redis.Redis = Depends(get_redis),
    current_user: db_models.User = Depends(get_current_active_user),
):
    memory = r.hgetall(f"short_term_memory:{agent_id}")
    if not memory:
        raise HTTPException(
            status_code=404, detail="Agent not found in short-term memory."
        )
    return {"memory": memory}
