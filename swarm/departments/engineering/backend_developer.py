from swarm.agents.base_agent import BaseAgent
from swarm.tools.file_reader import FileReader
from swarm.tools.file_writer import FileWriter
from swarm.tools.shell_command import ShellCommand


class BackendDeveloper(BaseAgent):
    """
    A backend developer agent in the Engineering department.
    Equipped with tools to write, read, and execute code.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [FileWriter(), FileReader(), ShellCommand()]
        super().__init__(
            role="Backend Developer",
            department="Engineering",
            tools=tools,
            model_name=model_name,
        )

    def execute_task(self, task_description: str) -> str:
        """
        Executes backend development tasks by using tools and records knowledge.
        """
        # Poll for a message
        message = self.receive_message()
        if message:
            task_description = message["message"]

        task_id = self._get_task_id(task_description)
        if task_id:
            self.update_task_status(task_id, "in_progress")

        print(f"[{self.role}] Received task: {task_description}")

        action = self.think(task_description)
        result = ""

        try:
            if action["tool"] != "none":
                print(
                    f"[{self.role}] Using tool: {action['tool']} with params: {action['params']}"
                )
                result = self.use_tool(action["tool"], **action["params"])

                # Knowledge Base Ingestion & Code Review Trigger
                if action["tool"] == "file_writer":
                    file_path = action["params"].get("file_path")

                    # 1. Save knowledge about the file write
                    print(
                        f"[{self.role}] Saving knowledge about file '{file_path}' to long-term memory."
                    )
                    self.save_to_long_term_memory(
                        document=f"Created or modified file at path: {file_path}",
                        metadata={
                            "tool": "file_writer",
                            "file_path": file_path,
                            "task": task_description,
                        },
                    )

                    # 2. Trigger a code review for the new file
                    print(
                        f"[{self.role}] Triggering code review for file '{file_path}'."
                    )
                    review_task = f"Task ID: {task_id}. Please review the code in the file '{file_path}'."
                    self.send_message("qa_manager", review_task)
            else:
                result = f"Completed backend task: {task_description}"

            if task_id:
                self.update_task_status(task_id, "completed")

            return result
        except Exception as e:
            if task_id:
                self.update_task_status(task_id, "failed")
            return f"An error occurred: {e}"
