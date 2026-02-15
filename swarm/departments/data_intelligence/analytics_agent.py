from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import re

from backend.app import db_models
from backend.app.core.config import settings
from backend.app.database import get_db_session_from_agent
from swarm.agents.base_agent import BaseAgent
from swarm.tools.data_analyzer import DataAnalyzer  # Keep existing tool


class AnalyticsAgent(BaseAgent):
    """
    Analyzes data, provides insights, and aggregates metrics for optimizing strategies and reporting.
    """

    def __init__(self, model_name: str = settings.LLM_MODEL_NAME):
        # Initialize with existing DataAnalyzer tool
        tools = [DataAnalyzer()]
        super().__init__(
            agent_id="analytics_agent",  # Ensure a consistent agent_id
            role="Analytics Agent",
            goal="Collect, process, and report on key business metrics to provide insights for strategic decisions.",
            backstory="A keen observer of data trends, this agent meticulously gathers information, identifies patterns, and distills complex datasets into actionable insights, driving data-informed growth.",
            model_name=model_name,
            tools=tools,
        )

    def record_event(
        self, event_type: str, user_id: str = None, payload: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Records a specific event into the events table.
        :param event_type: Type of the event (e.g., "user_signup", "subscription_created").
        :param user_id: Optional UUID of the user associated with the event.
        :param payload: Optional dictionary with additional event-specific data.
        """
        db = next(get_db_session_from_agent())
        try:
            event = db_models.Event(
                event_type=event_type,
                user_id=user_id,
                payload=payload,
                timestamp=datetime.utcnow(),
            )
            db.add(event)
            db.commit()
            return {"status": "success", "message": f"Event '{event_type}' recorded."}
        except Exception as e:
            db.rollback()
            return {
                "status": "error",
                "message": f"Failed to record event '{event_type}': {e}",
            }
        finally:
            db.close()

    def aggregate_daily_metrics(
        self, date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Aggregates key metrics for a given day (defaults to yesterday) from the events table.
        This is a simplified example and would be much more complex in a real scenario.
        """
        if date is None:
            date = datetime.utcnow() - timedelta(days=1)  # Aggregate for yesterday

        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)

        db = next(get_db_session_from_agent())
        try:
            # Example: Count new signups
            new_signups = (
                db.query(db_models.Event)
                .filter(
                    db_models.Event.event_type == "user_signup",
                    db_models.Event.timestamp >= start_of_day,
                    db_models.Event.timestamp < end_of_day,
                )
                .count()
            )

            # Example: Count new active subscriptions
            new_active_subscriptions = (
                db.query(db_models.Subscription)
                .filter(
                    db_models.Subscription.status == "active",
                    db_models.Subscription.created_at >= start_of_day,
                    db_models.Subscription.created_at < end_of_day,
                )
                .count()
            )

            # This is where more complex metrics like MRR estimation would be calculated
            # For simplicity, we'll just return basic counts
            metrics = {
                "date": start_of_day.isoformat(),
                "new_signups": new_signups,
                "new_active_subscriptions": new_active_subscriptions,
                # ... more metrics
            }

            # Optionally, store these aggregated metrics in a dedicated table for dashboards
            # For now, just print/return
            print(f"Daily Metrics for {start_of_day.date()}: {metrics}")
            return {"status": "success", "metrics": metrics}
        except Exception as e:
            db.rollback()
            return {
                "status": "error",
                "message": f"Failed to aggregate daily metrics: {e}",
            }
        finally:
            db.close()

    def execute_task(self, task_description: str) -> str:
        # Original execute_task logic can be adapted or replaced
        # For now, we'll extend it to handle new types of tasks for event processing/aggregation

        # Check for specific commands related to event recording or metric aggregation
        if "record event" in task_description.lower():
            # Expecting task_description like: "record event user_signup, user_id=xxx, payload={...}"
            # This would require more sophisticated parsing in a real agent, or direct function calls
            return self.record_event(
                event_type="generic_agent_event",
                payload={"description": task_description},
            )

        elif "aggregate daily metrics" in task_description.lower():
            # Example: "aggregate daily metrics for 2024-01-15"
            match = re.search(r"for (\d{4}-\d{2}-\d{2})", task_description)
            date_str = match.group(1) if match else None
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    return str(self.aggregate_daily_metrics(date_obj))
                except ValueError:
                    return "Invalid date format. Use YYYY-MM-DD."
            else:
                return str(self.aggregate_daily_metrics())

        # Fallback to original DataAnalyzer if no specific analytics task is matched
        print(
            f"[{self.agent_id}] Received task for general analysis: {task_description}"
        )
        action = self.think(task_description)  # LLM decides best action for analysis

        try:
            if action["tool"] == "data_analyzer":
                result = self.use_tool(action["tool"], **action["params"])
            else:
                result = f"Analytics Agent handled: {task_description}"

            # Simplified status update if needed for generic tasks
            return result
        except Exception as e:
            return f"An error occurred during analytics task: {e}"
