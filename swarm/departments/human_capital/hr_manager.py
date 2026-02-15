from swarm.agents.base_agent import BaseAgent
from swarm.tools.agent_creator import AgentCreator


class HRManager(BaseAgent):
    """
    Manages human resources tasks, including agent hiring (creation).
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [AgentCreator()]
        super().__init__(
            role="HR Manager",
            department="HumanCapital",
            tools=tools,
            model_name=model_name,
        )

    def execute_task(self, task_description: str) -> str:
        message = self.receive_message()
        if message:
            task_description = message["message"]

        task_id = self._get_task_id(task_description)
        if task_id:
            self.update_task_status(task_id, "in_progress")

        print(f"[{self.role}] Received task: {task_description}")
        action = self.think(task_description)

        try:
            if action["tool"] != "none":
                result = self.use_tool(action["tool"], **action["params"])
            else:
                result = f"HR Manager handled: {task_description}"

            if task_id:
                self.update_task_status(task_id, "completed")
            return result
        except Exception as e:
            if task_id:
                self.update_task_status(task_id, "failed")
            return f"An error occurred during HR task: {e}"
