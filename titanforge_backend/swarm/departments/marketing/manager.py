from swarm.agents.base_agent import BaseAgent

# No longer need to import the agent class directly
# from .content_creator import ContentCreator


class MarketingManager(BaseAgent):
    """
    The manager for the Marketing department.
    """

    def __init__(self, model_name: str = "mock-response"):
        super().__init__(
            role="Marketing Manager", department="Marketing", model_name=model_name
        )

    def execute_task(self, task_description: str) -> str:
        """
        Delegates marketing tasks.
        """
        # First, check for messages from the CEO
        message = self.receive_message()
        if message:
            task_description = message["message"]

        print(f"[{self.role}] Received task: {task_description}")

        # Delegate the task to the content creator
        self.send_message("content_creator", task_description)
        return "Task delegated to Content Creator."
