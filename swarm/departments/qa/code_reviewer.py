from swarm.agents.base_agent import BaseAgent
from swarm.tools.file_reader import FileReader


class CodeReviewer(BaseAgent):
    """
    An agent that reviews code for quality and adherence to standards.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [FileReader()]
        super().__init__(
            role="Code Reviewer", department="QA", tools=tools, model_name=model_name
        )

    def execute_task(self, task_description: str) -> str:
        """
        Executes a code review task.
        """
        message = self.receive_message()
        if message:
            task_description = message["message"]

        task_id = self._get_task_id(task_description)
        if task_id:
            self.update_task_status(task_id, "in_progress")

        print(f"[{self.role}] Received task: {task_description}")

        # The think method will decide to use the file_reader tool
        action = self.think(f"I need to read the file to review it. {task_description}")

        try:
            if action["tool"] == "file_reader":
                file_path = action["params"].get("file_path")
                print(f"[{self.role}] Reading file '{file_path}' for review.")
                code_content = self.use_tool("file_reader", file_path=file_path)

                # Now, use the LLM again to perform the review
                review_prompt = f"""
                You are a senior software engineer performing a code review.
                Analyze the following code for quality, bugs, and adherence to best practices.
                Provide a concise summary of your findings.

                Code to review:
                ```
                {code_content}
                ```
                """
                
                review_response = self.think(
                    review_prompt
                )  # Using think method again for LLM call

                review_summary = review_response.get("params", {}).get(
                    "summary", "Could not generate review."
                )

                # Save the review to long-term memory
                self.save_to_long_term_memory(
                    document=f"Code review for {file_path}: {review_summary}",
                    metadata={"task": "code_review", "file_path": file_path},
                )
                result = f"Review for {file_path} complete. Findings saved to memory."
            else:
                result = (
                    "Could not perform code review because no file path was specified."
                )

            if task_id:
                self.update_task_status(task_id, "completed")
            return result
        except Exception as e:
            if task_id:
                self.update_task_status(task_id, "failed")
            return f"An error occurred during code review: {e}"
