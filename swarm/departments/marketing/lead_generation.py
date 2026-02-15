from swarm.agents.base_agent import BaseAgent
from swarm.tools.email_tool import \
    EmailTool  # Assuming email_tool is available


class LeadGeneration(BaseAgent):
    """
    An agent focused on generating leads and customer acquisition.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [EmailTool()]  # To send outreach emails
        super().__init__(
            role="Lead Generation Agent",
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
        action = self.think(task_description)  # LLM decides best action for lead gen

        try:
            if action["tool"] != "none":
                result = self.use_tool(action["tool"], **action["params"])
            else:
                # Simulate lead generation and outreach
                print(
                    f"[{self.role}] Simulating searching for leads based on: {task_description}"
                )
                # Example: LLM might generate a list of target companies
                # Then use email_tool to send a templated email
                email_subject = "Exclusive Offer: Autonomous Software Solutions"
                email_body = f"""Dear Prospective Client,

I found your company while exploring opportunities related to {task_description}. TitanForge offers cutting-edge autonomous software development. Would you be interested in a demo?

Best regards,
The TitanForge Team"""

                # Use the email tool (if LLM decided to)
                # For this example, we directly call it based on a simple heuristic
                if (
                    "send email" in task_description.lower()
                    or "outreach" in task_description.lower()
                ):
                    # For a real LLM, it would provide 'to_address'
                    to_address = "prospect@example.com"  # Placeholder
                    email_result = self.use_tool(
                        "email_sender",
                        to_address=to_address,
                        subject=email_subject,
                        body=email_body,
                    )
                    result = f"Simulated lead search and email outreach to {to_address}. Result: {email_result}"
                else:
                    result = f"Simulated lead search complete for: {task_description}"

            if task_id:
                self.update_task_status(task_id, "completed")
            return result
        except Exception as e:
            if task_id:
                self.update_task_status(task_id, "failed")
            return f"An error occurred during lead generation task: {e}"
