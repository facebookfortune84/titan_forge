from swarm.agents.base_agent import BaseAgent
from swarm.tools.discord_tool import DiscordTool


class CommunityManager(BaseAgent):
    """
    Manages community engagement and communication channels.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [DiscordTool()]
        super().__init__(
            role="Community Manager",
            department="Marketing",
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
        action = self.think(
            task_description
        )  # LLM decides best action for community management

        try:
            if action["tool"] == "discord_notifier":
                result = self.use_tool(action["tool"], **action["params"])
            else:
                result = f"Community Manager handled: {task_description}"

            if task_id:
                self.update_task_status(task_id, "completed")
            return result
        except Exception as e:
            if task_id:
                self.update_task_status(task_id, "failed")
            return f"An error occurred during community task: {e}"
