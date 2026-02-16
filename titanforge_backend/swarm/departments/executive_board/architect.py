from swarm.agents.base_agent import BaseAgent


class Architect(BaseAgent):
    """
    High-level agent responsible for system architecture, performance monitoring,
    and driving continuous self-improvement.
    """

    def __init__(self, model_name: str = "mock-response"):
        # Architect has access to managers to trigger system changes
        super().__init__(
            role="Architect", department="Executive Board", model_name=model_name
        )

    def execute_task(self, task_description: str) -> str:
        message = self.receive_message()
        if message:
            task_description = message["message"]

        task_id = self._get_task_id(task_description)
        if task_id:
            self.update_task_status(task_id, "in_progress")

        print(f"[{self.role}] Received task: {task_description}")
        # LLM analyzes task_description (e.g., a performance report, a new requirement)
        # and decides if it needs to trigger HR for a new agent, or Engineering for a new tool.
        # This is where the self-improvement loop begins.

        # For prototyping, we'll use simple keyword matching to simulate decision.
        if "hire agent" in task_description.lower():
            self.send_message("hr_manager", task_description)
            result = "Requested HR Manager to hire a new agent."
        elif (
            "build tool" in task_description.lower()
            or "new feature" in task_description.lower()
        ):
            self.send_message("engineering_manager", task_description)
            result = "Requested Engineering Manager to build a new tool/feature."
        else:
            result = f"Architect analyzed: {task_description}"

        if task_id:
            self.update_task_status(task_id, "completed")
        return result
