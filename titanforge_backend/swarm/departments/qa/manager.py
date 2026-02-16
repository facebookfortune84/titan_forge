from swarm.agents.base_agent import BaseAgent


class QAManager(BaseAgent):
    """
    The manager for the QA department.
    """

    def __init__(self, model_name: str = "mock-response"):
        super().__init__(role="QA Manager", department="QA", model_name=model_name)

    def execute_task(self, task_description: str) -> str:
        message = self.receive_message()
        if message:
            task_description = message["message"]
        print(f"[{self.role}] Received task: {task_description}")

        # Simple heuristic to delegate to the correct QA agent
        if (
            "review" in task_description.lower()
            or "analyze" in task_description.lower()
        ):
            self.send_message("code_reviewer", task_description)
            return "Task delegated to Code Reviewer."
        else:
            self.send_message("test_engineer", task_description)
            return "Task delegated to Test Engineer."
