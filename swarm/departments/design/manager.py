from swarm.agents.base_agent import BaseAgent


class DesignManager(BaseAgent):
    """
    The manager for the Design department.
    """

    def __init__(self, model_name: str = "mock-response"):
        super().__init__(
            role="Design Manager", department="Design", model_name=model_name
        )

    def execute_task(self, task_description: str) -> str:
        message = self.receive_message()
        if message:
            task_description = message["message"]
        print(f"[{self.role}] Received task: {task_description}")
        self.send_message("graphic_designer", task_description)
        return "Task delegated to Graphic Designer."
