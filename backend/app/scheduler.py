import json
from datetime import datetime
from typing import Any, Dict

import redis
from apscheduler.schedulers.background import BackgroundScheduler

from .core.config import settings
from .swarm.departments.executive_board.ceo import CEO

# from swarm.departments.marketing.lead_generation import LeadGeneration # Removed top-level import


def get_redis_client():
    """Helper to get a Redis client for scheduler tasks."""
    r = redis.Redis(
        host=settings.REDIS_URL.split("://")[1].split(":")[0],
        port=int(settings.REDIS_URL.split(":")[-1].split("/")[0]),
        db=int(settings.REDIS_URL.split("/")[-1]),
    )
    return r


def send_agent_message(
    recipient_id: str, sender_id: str, message_content: Dict[str, Any], r: redis.Redis
) -> None:
    message_json = json.dumps({"sender_id": sender_id, "message": message_content})
    r.rpush(recipient_id, message_json)


def process_backlog_task():
    """Function to be executed by the scheduler to process the CEO's backlog."""
    print("--- SCHEDULER: Triggering CEO to process backlog. ---")
    try:
        ceo = CEO(model_name=settings.LLM_MODEL_NAME)
        # Calling with no description makes the CEO process one item from the backlog
        ceo.execute_task(task_description="")
    except Exception as e:
        print(f"--- SCHEDULER ERROR (CEO Backlog): {e} ---")


def customer_acquisition_task():
    """Function to be executed by the scheduler to find new customers."""
    print("--- SCHEDULER: Triggering Lead Generation agent. ---")
    try:
        from swarm.departments.marketing.lead_generation import \
            LeadGeneration  # Moved import here

        lead_agent = LeadGeneration(model_name=settings.LLM_MODEL_NAME)
        lead_agent.execute_task(
            "Search for potential customers and send outreach emails."
        )
    except Exception as e:
        print(f"--- SCHEDULER ERROR (Customer Acquisition): {e} ---")


def aggregate_analytics_task():
    """Function to be executed by the scheduler to aggregate daily analytics."""
    print(
        f"--- SCHEDULER: Triggering Analytics Agent to aggregate daily metrics for {datetime.utcnow().date()}. ---"
    )
    r = get_redis_client()
    send_agent_message(
        recipient_id="analytics_agent",
        sender_id="scheduler",
        message_content={
            "action": "aggregate_daily_metrics",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
        },
        r=r,
    )
    print("--- SCHEDULER: Analytics Agent notified for daily aggregation. ---")


scheduler = BackgroundScheduler()
scheduler.add_job(process_backlog_task, "interval", hours=1, id="ceo_backlog_processor")
scheduler.add_job(
    customer_acquisition_task, "interval", hours=4, id="customer_acquisition"
)
scheduler.add_job(
    aggregate_analytics_task, "cron", hour=2, minute=0, id="daily_analytics_aggregation"
)  # Run daily at 2 AM UTC


def start_scheduler():
    print("Starting task scheduler...")
    scheduler.start()


def get_scheduler_jobs():
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append(
            {
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run_time": str(job.next_run_time),
            }
        )
    return jobs
