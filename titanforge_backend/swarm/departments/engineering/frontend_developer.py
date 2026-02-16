from swarm.agents.base_agent import BaseAgent
from swarm.tools.file_reader import FileReader
from swarm.tools.file_writer import FileWriter


class FrontendDeveloper(BaseAgent):
    """
    A frontend developer agent in the Engineering department.
    Equipped with tools to create and modify UI files.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [FileWriter(), FileReader()]
        super().__init__(
            role="Frontend Developer",
            department="Engineering",
            tools=tools,
            model_name=model_name,
        )

    def execute_task(self, task_description: str) -> str:
        """
        Executes frontend development tasks by using tools.
        """
        print(f"[{self.role}] Received task: {task_description}")

        # Use the 'think' method to decide on an action
        action = self.think(task_description)

        if action["tool"] != "none":
            # Execute a tool
            print(
                f"[{self.role}] Using tool: {action['tool']} with params: {action['params']}"
            )
            return self.use_tool(action["tool"], **action["params"])
        else:
            # If no tool is applicable, just return a confirmation
            return f"Completed frontend task: {task_description}"
