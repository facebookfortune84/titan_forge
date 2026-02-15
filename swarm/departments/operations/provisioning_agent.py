from typing import Any, Dict

from backend.app import crud, db_models
from backend.app.core.config import settings
from backend.app.database import get_db_session_from_agent
from swarm.agents.base_agent import BaseAgent


class ProvisioningAgent(BaseAgent):
    def __init__(self, model_name: str = settings.LLM_MODEL_NAME):
        super().__init__(
            agent_id="provisioning_agent",
            role="Manages user access to features and resources based on subscription status.",
            goal="Ensure users receive the correct entitlements instantly upon purchase and lose access appropriately upon subscription changes.",
            backstory="A meticulous agent that configures the system to match user entitlements with their purchased plans, maintaining system integrity and customer satisfaction.",
            model_name=model_name,
        )

    def provision_user_access(
        self, user_id: str, subscription_status: str, product_id: str = None
    ) -> Dict[str, Any]:
        """
        Provisions or de-provisions user access based on subscription status.
        :param user_id: The UUID of the user.
        :param subscription_status: The status of the subscription (e.g., 'active', 'canceled', 'past_due').
        :param product_id: The UUID of the product/plan.
        """
        db = next(get_db_session_from_agent())
        user = crud.get_user(db, user_id)
        if not user:
            db.close()
            return {"status": "error", "message": f"User {user_id} not found."}

        # Example provisioning logic (this would be expanded based on actual features)
        if subscription_status == "active":
            user.is_active = True
            # Update user's current_subscription_id if a product_id is provided
            if product_id:
                subscription = (
                    db.query(db_models.Subscription)
                    .filter(
                        db_models.Subscription.user_id == user_id,
                        db_models.Subscription.product_id == product_id,
                        db_models.Subscription.status == "active",
                    )
                    .first()
                )
                if subscription:
                    user.current_subscription_id = subscription.id
            print(
                f"User {user_id} provisioned with active access for product {product_id}."
            )
            # self.send_message("orchestrator", "user_active", {"user_id": user_id, "product_id": product_id})
        elif subscription_status == "canceled" or subscription_status == "past_due":
            user.is_active = False
            user.current_subscription_id = None  # Clear current subscription
            print(
                f"User {user_id} de-provisioned due to status: {subscription_status}."
            )
            # self.send_message("orchestrator", "user_inactive", {"user_id": user_id, "reason": subscription_status})
        else:
            print(
                f"Unhandled subscription status for user {user_id}: {subscription_status}"
            )
            db.close()
            return {
                "status": "warning",
                "message": f"Unhandled subscription status: {subscription_status}",
            }

        db.add(user)
        db.commit()
        db.close()
        return {
            "status": "success",
            "message": f"User {user_id} access updated to {subscription_status}.",
        }

    def initiate_productized_service(
        self, user_id: str, product_id: str, task_description: str
    ) -> Dict[str, Any]:
        """
        Initiates a specific agent workflow for a productized service.
        :param user_id: The UUID of the user who purchased the service.
        :param product_id: The UUID of the productized service.
        :param task_description: A description of the task to be performed by agents.
        """
        db = next(get_db_session_from_agent())
        user = crud.get_user(db, user_id)
        product = (
            db.query(db_models.Product)
            .filter(db_models.Product.id == product_id)
            .first()
        )

        if not user or not product:
            db.close()
            return {"status": "error", "message": "User or Product not found."}

        # Here, you would instruct the Orchestrator or a specific department agent
        # For example, sending a message to the Orchestrator
        # self.send_message("orchestrator", "new_productized_service", {
        #     "user_id": user_id,
        #     "product_id": product_id,
        #     "product_name": product.name,
        #     "task_description": task_description
        # })
        db.close()
        print(
            f"Initiated productized service '{product.name}' for user {user_id} with task: {task_description}"
        )
        return {
            "status": "success",
            "message": f"Productized service '{product.name}' initiated for user {user_id}.",
        }
