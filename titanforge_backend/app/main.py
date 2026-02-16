import importlib.util  # For dynamic module loading
import inspect  # New import for dynamic agent loading
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path  # For file system operations
from typing import Any, Dict, List, Literal

import litellm
import redis
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from swarm.agents.base_agent import \
    BaseAgent  # Import BaseAgent for type checking in dynamic loading
from swarm.departments.executive_board.ceo import CEO

from . import crud, db_models, schemas, security
from .api.v1.admin import router as admin_router  # New import
from .api.v1.agents import router as agents_router  # NEW - Agent management
from .api.v1.auth import router as auth_router  # NEW
from .api.v1.blog import router as blog_router  # NEW - Blog endpoints
from .api.v1.leads import router as leads_router  # NEW
from .api.v1.pricing import router as pricing_router  # NEW - Pricing management
from .api.v1.sales_funnel import router as sales_funnel_router  # NEW - Sales funnel & lead magnet
from .api.v1.roi_calculator import router as roi_calculator_router  # NEW - ROI PDF generation
from .api.v1.alumni_import import router as alumni_router  # NEW - Alumni import pipeline
from .api.v1.dashboard import router as dashboard_router  # NEW - Visual dashboard
from .api.v1.landing import router as landing_router  # NEW - Landing page
from .api.v1.income_reporting import router as income_reporting_router
from .api.v1.landing_page import router as landing_page_router
from .api.v1.payments import router as payments_router
from .api.v1.stripe_webhooks import router as stripe_webhook_router
from .core.config import settings
from .database import engine, get_db
from .redis_client import get_redis
from .scheduler import get_scheduler_jobs, start_scheduler  # New import

# --- Create DB Tables on Startup ---
db_models.Base.metadata.create_all(bind=engine)


from .dependencies import get_current_active_user, send_agent_message


from fastapi.middleware.cors import CORSMiddleware

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
    load_new_agents()  # Load any dynamically created agents
    # Initialize agents that might need to listen for messages or perform startup tasks
    # billing_agent = BillingAgent()
    # provisioning_agent = ProvisioningAgent()
    # notification_agent = NotificationAgent()
    # analytics_agent = AnalyticsAgent()

# --- Root Endpoint ---
@app.get("/")
async def root():
    """Root endpoint - health check for TitanForge MCP"""
    return {"message": "TitanForge MCP is online. Awaiting agent instructions."}


# Include API routers
app.include_router(landing_page_router, prefix="/api/v1")
app.include_router(stripe_webhook_router, prefix="/api/v1")
app.include_router(income_reporting_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")  # New router inclusion
app.include_router(agents_router, prefix="/api/v1")  # NEW - Agent management
app.include_router(auth_router, prefix="/api/v1/auth")  # NEW - Auth endpoints
app.include_router(leads_router, prefix="/api/v1")  # NEW - Lead capture
app.include_router(blog_router, prefix="/api/v1")  # NEW - Blog system
app.include_router(pricing_router, prefix="/api/v1")  # NEW - Pricing endpoints
app.include_router(sales_funnel_router, prefix="/api/v1")  # NEW - Sales funnel & lead magnet
app.include_router(roi_calculator_router, prefix="/api/v1")  # NEW - ROI PDF generation
app.include_router(alumni_router, prefix="/api/v1")  # NEW - Alumni import
app.include_router(dashboard_router)  # NEW - Visual dashboard
app.include_router(landing_router)  # NEW - Landing page

from .dependencies import get_current_active_user



# Directory where new agents are placed by AgentCreator
AGENT_NEW_RECRUITS_DIR = Path(
    "F:/TitanForge/swarm/departments/human_capital/new_recruits"
)


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


# --- Centralized Systems ---
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
    "billing_manager",  # New agent
    "hr_manager",
    "orchestrator",
    "analytics_agent",  # Existing agent, but ensuring it's in registry
    "provisioning_agent",  # New agent
    "notification_agent",  # New agent
}


# --- API Models ---
class Goal(BaseModel):
    description: str


class SendMessage(BaseModel):
    sender_id: str
    recipient_id: str
    message: str


class SpeakRequest(BaseModel):
    text: str


class TaskUpdate(BaseModel):
    status: Literal["in_progress", "completed", "failed"]
    agent_id: str


class ShortTermMemoryAdd(BaseModel):


    agent_id: str


    key: str


    value: str





# --- New API Models for File I/O and Graph ---


class FilePath(BaseModel):


    path: str





class FileContent(BaseModel):


    path: str


    content: str





# --- File I/O Endpoints ---





# Define a safe workspace directory relative to the project root


# For Docker, this path might need to be adjusted based on the volume mapping.


# For local development, ensure this directory exists and is managed.


# IMPORTANT: In a production environment, this should be configured more securely


# and potentially isolated per user or agent.


AGENT_FILES_DIR = Path("./agent_files_workspace").resolve()


AGENT_FILES_DIR.mkdir(parents=True, exist_ok=True) # Ensure it exists





def get_safe_path(base_dir: Path, relative_path: str) -> Path:


    """


    Constructs a safe absolute path ensuring it remains within the base_dir.


    Raises HTTPException if the path attempts to escape the base_dir.


    """


    full_path = (base_dir / relative_path).resolve()


    if not full_path.is_relative_to(base_dir):


        raise HTTPException(


            status_code=status.HTTP_400_BAD_REQUEST,


            detail="Operation not allowed outside designated workspace."


        )


    return full_path





@app.post("/api/v1/io/read")


async def read_agent_file(


    file_path_data: FilePath,


    current_user: db_models.User = Depends(get_current_active_user),


) -> Dict[str, str]:


    """


    Reads the content of a file from the agent's workspace.


    """


    try:


        path = get_safe_path(AGENT_FILES_DIR, file_path_data.path)


        if not path.is_file():


            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")


        content = path.read_text()


        return {"content": content}


    except HTTPException as e:


        raise e


    except Exception as e:


        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to read file: {e}")





@app.post("/api/v1/io/write")


async def write_agent_file(


    file_content_data: FileContent,


    current_user: db_models.User = Depends(get_current_active_user),


) -> Dict[str, str]:


    """


    Writes content to a file in the agent's workspace.


    """


    try:


        path = get_safe_path(AGENT_FILES_DIR, file_content_data.path)


        path.parent.mkdir(parents=True, exist_ok=True) # Ensure parent directories exist


        path.write_text(file_content_data.content)


        return {"message": "File written successfully."}


    except HTTPException as e:


        raise e


    except Exception as e:


        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to write file: {e}")





# --- Graph Endpoint ---


@app.get("/api/v1/graph")


async def get_agent_graph(


    current_user: db_models.User = Depends(get_current_active_user),


) -> Dict[str, List[Dict[str, Any]]]:


    """


    Generates and returns a graph of agents, tasks, and artifacts.


    """


    # For initial implementation, return mock data.


    # In a real system, this would dynamically generate graph data


    # based on active agents, tasks, and their relationships.


    nodes = []


    links = []





    # Add agents as nodes


    for agent_id in agent_registry:


        nodes.append({"id": agent_id, "category": "AGENT", "sector": "general_engineering"})





    # Add some mock tasks and link them to agents


    mock_tasks = {


        "task_1": {"description": "Develop new feature", "assigned_to": "backend_developer"},


        "task_2": {"description": "Design UI", "assigned_to": "frontend_developer"},


        "task_3": {"description": "Analyze market data", "assigned_to": "analytics_agent"},


    }





    for task_id, task_data in mock_tasks.items():


        nodes.append({"id": task_id, "category": "TASK", "description": task_data["description"]})


        if task_data["assigned_to"] in agent_registry:


            links.append({"source": task_id, "target": task_data["assigned_to"]})





    # Add some mock artifacts


    mock_artifacts = {


        "artifact_a": {"name": "codebase.zip", "created_by": "backend_developer"},


        "artifact_b": {"name": "design_mockup.fig", "created_by": "frontend_developer"},


    }





    for artifact_id, artifact_data in mock_artifacts.items():


        nodes.append({"id": artifact_id, "category": "ARTIFACT", "name": artifact_data["name"]})


        if artifact_data["created_by"] in agent_registry:


            links.append({"source": artifact_id, "target": artifact_data["created_by"]})


    


    return {"nodes": nodes, "links": links}





# --- Authentication Endpoints ---
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=schemas.UserResponse)
async def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = crud.create_user(db=db, user=user)

    # Send user_signup event to Analytics Agent
    send_agent_message(
        recipient_id="analytics_agent",
        sender_id="mcp",
        message_content={
            "action": "record_event",
            "event_type": "user_signup",
            "user_id": str(new_user.id),
            "payload": {"email": new_user.email},
        },
        r=r,
    )
    # Send welcome email to Notification Agent
    send_agent_message(
        recipient_id="notification_agent",
        sender_id="mcp",
        message_content={
            "action": "process_notification_request",
            "notification_type": "welcome",
            "data": {
                "user_email": new_user.email,
                "user_name": new_user.full_name or new_user.email.split("@")[0],
            },
        },
        r=r,
    )
    return new_user


@app.get("/users/me/", response_model=schemas.UserResponse)
async def read_users_me(
    current_user: schemas.UserResponse = Depends(get_current_active_user),
):
    return current_user


# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "TitanForge MCP is online. Awaiting agent instructions."}


@app.post("/goals")
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

        # Send goal_submitted event to Analytics Agent
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
        # Optionally send internal error notification
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


@app.post("/speak")
# ... (speak endpoint is unchanged)


# -- Scheduler Endpoints --
@app.get("/scheduler/jobs")
async def get_scheduled_jobs():
    """
    Returns a list of currently scheduled jobs.
    """
    return get_scheduler_jobs()


# -- Task Management Endpoints --
@app.get("/tasks", response_model=List[Dict[str, Any]])
async def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    # For now, return all tasks. Later, filter by user.
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


@app.put("/tasks/{task_id}")
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
    task.history = new_history  # SQLAlchemy detects this change on mutable types

    db.commit()
    return {"message": f"Task {task_id} status updated to {update.status}"}


# -- Inter-Agent Communication Endpoints --
@app.post("/messages/send")
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


@app.get("/messages/receive/{agent_id}")
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


# -- Short-Term Memory Endpoints --
@app.post("/memory/short_term/add")
async def add_to_short_term_memory(
    item: ShortTermMemoryAdd,
    r: redis.Redis = Depends(get_redis),
    current_user: db_models.User = Depends(get_current_active_user),
):
    r.hset(f"short_term_memory:{item.agent_id}", item.key, item.value)
    return {"message": "Data added to short-term memory."}


@app.get("/memory/short_term/{agent_id}")
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


@app.get("/analytics/summary")
async def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    # This endpoint should ideally only be accessible by superusers or admin roles
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view analytics.",
        )

    total_users = db.query(db_models.User).count()
    total_signups = (
        db.query(db_models.Event)
        .filter(db_models.Event.event_type == "user_signup")
        .count()
    )
    active_subscriptions = (
        db.query(db_models.Subscription)
        .filter(db_models.Subscription.status == "active")
        .count()
    )

    # Placeholder for MRR - would need more sophisticated calculation
    # For now, sum of unit_amount for active subscriptions
    mrr_estimate = 0
    active_subs = (
        db.query(db_models.Subscription)
        .filter(db_models.Subscription.status == "active")
        .all()
    )
    for sub in active_subs:
        product = (
            db.query(db_models.Product)
            .filter(db_models.Product.id == sub.product_id)
            .first()
        )
        if product and product.type == "subscription":
            # Assuming monthly for simplicity, adjust for annual plans
            if product.interval == "month":
                mrr_estimate += product.unit_amount
            elif product.interval == "year":
                mrr_estimate += product.unit_amount / 12  # Convert yearly to monthly

    # Convert cents to dollars for display
    mrr_estimate_dollars = mrr_estimate / 100

    return {
        "total_users": total_users,
        "total_signups": total_signups,
        "active_subscriptions": active_subscriptions,
        "mrr_estimate_usd": round(mrr_estimate_dollars, 2),
    }


# ... (other endpoints like long-term memory are unchanged for now)

if __name__ == "__main__":
    if settings.LLM_MODEL_NAME == "mock-response":
        print("Using mock LLM response.")
        # Mock response needs to be imported or defined here
        # For simplicity, we assume it's available
                # litellm.mock_response = mock_llm_response

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
