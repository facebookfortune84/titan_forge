import json

from swarm.agents.base_agent import BaseAgent
from swarm.tools.stripe_tool import StripeTool


class BillingManager(BaseAgent):
    """
    The manager for the Finance department, responsible for billing.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [StripeTool()]
        super().__init__(
            role="Billing Manager",
            department="Finance",
            tools=tools,
            model_name=model_name,
        )
        self.pricing_tiers = self.load_pricing()

    def load_pricing(self):
        """Loads pricing tiers from the data file."""
        try:
            # The pricing.json was moved to the frontend public folder.
            # In a real app, this might be a shared location or fetched via API.
            # For now, we'll point to its new location.
            with open("F:/TitanForge/frontend/public/pricing.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading pricing.json: {e}")
            return []

    def execute_task(self, task_description: str) -> str:
        """
        Executes finance-related tasks, like generating payment links.
        """
        message = self.receive_message()
        if message:
            task_description = message["message"]

        print(f"[{self.role}] Received task: {task_description}")
        action = self.think(task_description)

        if action["tool"] == "stripe_payment_link_generator":
            # The LLM will tell us the product name (tier name)
            # We need to find the price and pass both to the tool
            product_name = action["params"].get("product_name", "").lower()
            for tier in self.pricing_tiers:
                if tier["name"].lower() == product_name:
                    action["params"]["amount"] = tier["price"]
                    return self.use_tool(action["tool"], **action["params"])
            return f"Error: Could not find pricing tier named '{product_name}'."

        return "No applicable finance action found."
