import json

from swarm.agents.base_agent import BaseAgent

# No longer need to import the manager classes directly for sending messages
# from swarm.departments.engineering.manager import EngineeringManager
# from swarm.departments.marketing.manager import MarketingManager


class CEO(BaseAgent):
    """
    The CEO of the TitanForge swarm.
    Responsible for setting high-level goals and delegating them.
    Also manages the task backlog.
    """

    def __init__(self, model_name: str = "mock-response"):
        super().__init__(
            role="CEO", department="Executive Board", model_name=model_name
        )
        self.backlog = self.load_backlog()

    def load_backlog(self):
        """Loads tasks from the backlog file."""
        try:
            with open("F:/TitanForge/data/backlog.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("backlog.json not found. Starting with an empty backlog.")
            return []
        except json.JSONDecodeError:
            print("Error decoding backlog.json. Starting with an empty backlog.")
            return []

    def delegate_task(self, task: dict):
        """Delegates a task to the appropriate department manager."""
        department = task.get("department")
        description = task.get("description")

        if not department or not description:
            return "Task is missing department or description."

        print(
            f"[{self.role}] Delegating task '{description}' to {department} department."
        )

        if department == "Executive Board":  # For architect
            self.send_message("architect", description)
            return "Task delegated to Architect."
        elif department == "HumanCapital":  # For HR Manager
            self.send_message("hr_manager", description)
            return "Task delegated to HR Manager."
        elif department == "Operations":  # For Orchestrator
            self.send_message("orchestrator", description)
            return "Task delegated to Orchestrator."
        elif department == "DataIntelligence":  # For Analytics Agent
            self.send_message("analytics_agent", description)
            return "Task delegated to Analytics Agent."
        elif department == "Engineering":
            self.send_message("engineering_manager", description)
            return "Task delegated to Engineering Manager."
        elif department == "Marketing":
            self.send_message("marketing_manager", description)
            return "Task delegated to Marketing Manager."
        elif department == "Design":
            self.send_message("design_manager", description)
            return "Task delegated to Design Manager."
        elif department == "QA":
            self.send_message("qa_manager", description)
            return "Task delegated to QA Manager."
        else:
            return f"No manager found for department: {department}"

    def execute_task(self, task_description: str) -> str:
        """
        Processes a single, high-level goal or works through the backlog.
        """
        if task_description:
            # Handle a single goal submission from the UI
            print(f"[{self.role}] Received high-level goal: {task_description}")
            # A simple heuristic to decide which department to delegate to
            if (
                "market" in task_description.lower()
                or "post" in task_description.lower()
                or "leads" in task_description.lower()
                or "customers" in task_description.lower()
            ):
                return self.delegate_task(
                    {"department": "Marketing", "description": task_description}
                )
            elif (
                "design" in task_description.lower()
                or "logo" in task_description.lower()
                or "image" in task_description.lower()
            ):
                return self.delegate_task(
                    {"department": "Design", "description": task_description}
                )
            elif (
                "test" in task_description.lower()
                or "quality" in task_description.lower()
                or "review code" in task_description.lower()
            ):
                return self.delegate_task(
                    {"department": "QA", "description": task_description}
                )
            elif (
                "hire" in task_description.lower()
                or "new agent" in task_description.lower()
                or "workforce" in task_description.lower()
            ):
                return self.delegate_task(
                    {"department": "HumanCapital", "description": task_description}
                )
            elif (
                "scale" in task_description.lower()
                or "infrastructure" in task_description.lower()
                or "deploy" in task_description.lower()
            ):
                return self.delegate_task(
                    {"department": "Operations", "description": task_description}
                )
            elif (
                "analyze data" in task_description.lower()
                or "insights" in task_description.lower()
                or "optimize" in task_description.lower()
            ):
                return self.delegate_task(
                    {"department": "DataIntelligence", "description": task_description}
                )
            elif (
                "architect" in task_description.lower()
                or "system" in task_description.lower()
                or "improve" in task_description.lower()
            ):
                return self.delegate_task(
                    {"department": "Executive Board", "description": task_description}
                )  # Architect is in Executive Board
            else:
                return self.delegate_task(
                    {"department": "Engineering", "description": task_description}
                )
        else:
            # Process the backlog
            if not self.backlog:
                return "No tasks in the backlog."

            task = self.backlog.pop(0)  # Get the next task
            return self.delegate_task(task)
