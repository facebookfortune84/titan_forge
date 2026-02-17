from fastapi import APIRouter
from ...scheduler import get_scheduler_jobs

router = APIRouter()

@router.get("/jobs")
async def get_scheduled_jobs():
    """
    Returns a list of currently scheduled jobs.
    """
    return get_scheduler_jobs()
