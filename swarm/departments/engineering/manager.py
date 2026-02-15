from swarm.agents.base_agent import BaseAgent
from swarm.tools.file_reader import FileReader
from swarm.tools.file_writer import FileWriter


class EngineeringManager(BaseAgent):
    """
    The manager for the Engineering department.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [FileWriter(), FileReader()]
        super().__init__(
            role="Engineering Manager",
            department="Engineering",
            tools=tools,
            model_name=model_name,
        )

    def execute_task(self, task_description: str) -> str:
        """
        Delegates tasks to the appropriate developers or executes them directly.
        """
        # First, check for messages from the CEO
        message = self.receive_message()
        if message:
            task_description = message["message"]

        print(f"[{self.role}] Received task: {task_description}")

        # Use the 'think' method to decide on an action
        action = self.think(task_description)

        if action["tool"] != "none":
            # Execute a tool
            return self.use_tool(action["tool"], **action["params"])
        else:
            # Delegate to other agents
            if "backend" in task_description.lower():
                self.send_message("backend_developer", task_description)
                return "Task delegated to Backend Developer."
            elif "frontend" in task_description.lower():
                self.send_message("frontend_developer", task_description)
                return "Task delegated to Frontend Developer."
            else:
                return "Could not determine the appropriate developer for the task."
