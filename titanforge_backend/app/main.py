import importlib.util  # For dynamic module loading
import inspect  # New import for dynamic agent loading
import sys
from pathlib import Path  # For file system operations
from typing import Any, Dict, List

import redis
import uvicorn
from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from swarm.agents.base_agent import \
    BaseAgent  # Import BaseAgent for type checking in dynamic loading

from . import db_models, schemas
from .api.v1.admin import router as admin_router
from .api.v1.agents import router as agents_router
from .api.v1.auth import router as auth_router
from .api.v1.blog import router as blog_router
from .api.v1.leads import router as leads_router
from .api.v1.pricing import router as pricing_router
from .api.v1.sales_funnel import router as sales_funnel_router
from .api.v1.roi_calculator import router as roi_calculator_router
from .api.v1.alumni_import import router as alumni_router
from .api.v1.dashboard import router as dashboard_router
from .api.v1.landing import router as landing_router
from .api.v1.income_reporting import router as income_reporting_router
from .api.v1.payments import router as payments_router
from .api.v1.stripe_webhooks import router as stripe_webhook_router
from .api.v1.tasks import router as tasks_router
from .api.v1.io import router as io_router
from .api.v1.graph import router as graph_router
from .api.v1.messages import router as messages_router
from .api.v1.memory import router as memory_router
from .api.v1.analytics import router as analytics_router
from .api.v1.scheduler import router as scheduler_router

from .core.config import settings
from .database import engine, get_db
from .redis_client import get_redis
from .scheduler import start_scheduler

from fastapi.middleware.cors import CORSMiddleware

# --- Create DB Tables on Startup ---


# --- Start Scheduler on Startup ---
app = FastAPI(
    title="TitanForge Master Control Program (MCP)",
    description="The central API for coordinating the TitanForge autonomous agent swarm.",
    version="0.1.0",
)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    load_new_agents()

# --- Root Endpoint ---
@app.get("/")
async def root():
    """Root endpoint - health check for TitanForge MCP"""
    return {"message": "TitanForge MCP is online. Awaiting agent instructions."}


# Include API routers
app.include_router(stripe_webhook_router, prefix="/api/v1")
app.include_router(income_reporting_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(agents_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(leads_router, prefix="/api/v1")
app.include_router(blog_router, prefix="/api/v1")
app.include_router(pricing_router, prefix="/api/v1")
app.include_router(sales_funnel_router, prefix="/api/v1")
app.include_router(roi_calculator_router, prefix="/api/v1")
app.include_router(alumni_router, prefix="/api/v1")
app.include_router(dashboard_router)
app.include_router(landing_router)
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(io_router, prefix="/api/v1/io")
app.include_router(graph_router, prefix="/api/v1")
app.include_router(messages_router, prefix="/api/v1/messages")
app.include_router(memory_router, prefix="/api/v1/memory")
app.include_router(analytics_router, prefix="/api/v1/analytics")
app.include_router(scheduler_router, prefix="/api/v1/scheduler")


# Directory where new agents are placed by AgentCreator
AGENT_NEW_RECRUITS_DIR = Path(
    "F:/TitanForge/swarm/departments/human_capital/new_recruits"
)

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

def load_new_agents():
    print(f"Scanning for new agents in: {AGENT_NEW_RECRUITS_DIR}")
    if not AGENT_NEW_RECRUITS_DIR.exists():
        AGENT_NEW_RECRUITS_DIR.mkdir(parents=True, exist_ok=True)
        return

    for agent_file in AGENT_NEW_RECRUITS_DIR.glob("*.py"):
        if agent_file.name == "__init__.py":
            continue

        module_name = f"swarm.departments.human_capital.new_recruits.{agent_file.stem}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, agent_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseAgent)
                        and obj is not BaseAgent
                    ):
                        try:
                            temp_agent_instance = obj(
                                model_name=settings.LLM_MODEL_NAME
                            )
                            if (
                                temp_agent_instance.agent_id not in agent_registry
                            ):  # Use agent_id instead of role
                                agent_registry.add(temp_agent_instance.agent_id)
                                print(
                                    f"Dynamically loaded and registered new agent: {temp_agent_instance.agent_id}"
                                )
                        except Exception as e:
                            print(
                                f"Error instantiating dynamically loaded agent {name}: {e}"
                            )
            else:
                print(f"Could not get spec or loader for {agent_file}")
        except Exception as e:
            print(f"Error loading agent module {module_name} from {agent_file}: {e}")

if __name__ == "__main__":
    if settings.LLM_MODEL_NAME == "mock-response":
        print("Using mock LLM response.")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
