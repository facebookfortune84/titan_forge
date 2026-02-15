from typing import Any, Dict, List, Optional

from backend.app.core.config import settings
from swarm.agents.base_agent import BaseAgent
from swarm.tools.email_tool import EmailTool


class NotificationAgent(BaseAgent):
    def __init__(self, model_name: str = settings.LLM_MODEL_NAME):
        super().__init__(
            agent_id="notification_agent",
            role="Handles all automated external and internal communications.",
            goal="Ensure timely and relevant delivery of information to users and internal teams.",
            backstory="A diligent messenger, this agent ensures that every important update, alert, or confirmation reaches its intended recipient, fostering transparency and responsiveness.",
            model_name=model_name,
        )
        self.email_tool = EmailTool()
        # Potentially add other communication tools here (e.g., DiscordTool, SMSTool)

    def send_user_email(
        self,
        to_email: str | List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sends an email to a user or list of users.
        :param to_email: Recipient email address(es).
        :param subject: Subject of the email.
        :param body: Plain text body of the email.
        :param html_body: Optional HTML body.
        """
        if not self.email_tool._configured:
            return {"status": "error", "message": "Email service not configured."}

        success = self.email_tool.send_email(to_email, subject, body, html_body)
        if success:
            print(f"User email sent to {to_email} with subject: '{subject}'")
            return {"status": "success", "message": f"Email sent to {to_email}."}
        else:
            print(f"Failed to send user email to {to_email} with subject: '{subject}'")
            return {
                "status": "error",
                "message": f"Failed to send email to {to_email}.",
            }

    def send_internal_alert(
        self, message: str, severity: str = "info"
    ) -> Dict[str, Any]:
        """
        Sends an internal alert (e.g., to Discord, Slack, etc.).
        For now, this will just print to console.
        :param message: The alert message.
        :param severity: Severity level (info, warning, error).
        """
        # In a real scenario, this would integrate with a DiscordTool or similar
        print(f"INTERNAL ALERT [{severity.upper()}]: {message}")
        return {"status": "success", "message": "Internal alert logged."}

    def process_notification_request(
        self, notification_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        A general handler for various notification requests.
        :param notification_type: Type of notification (e.g., "welcome", "payment_succeeded", "subscription_canceled").
        :param data: Dictionary containing context for the notification (e.g., user_email, amount).
        """
        if notification_type == "welcome":
            user_email = data.get("user_email")
            if user_email:
                subject = "Welcome to TitanForge!"
                body = f"Hello {data.get('user_name', '')},\n\nWelcome to TitanForge! We're excited to have you on board.\n\nRegards,\nYour TitanForge Team"
                html_body = f"""
                <html>
                    <body>
                        <p>Hello {data.get('user_name', 'there')},</p>
                        <p>Welcome to <strong>TitanForge</strong>! We're excited to have you on board.</p>
                        <p>You can get started by logging into your dashboard <a href="{settings.FRONTEND_URL}/dashboard">here</a>.</p>
                        <p>Regards,<br>Your TitanForge Team</p>
                    </body>
                </html>
                """
                return self.send_user_email(user_email, subject, body, html_body)
            else:
                return {
                    "status": "error",
                    "message": "Missing user_email for welcome notification.",
                }

        elif notification_type == "payment_succeeded":
            user_email = data.get("user_email")
            amount = data.get("amount")
            currency = data.get("currency")
            if user_email and amount and currency:
                subject = "Your TitanForge Payment Was Successful!"
                body = f"Hello,\n\nYour payment of {amount} {currency} to TitanForge was successful. Thank you for your business!\n\nRegards,\nYour TitanForge Team"
                html_body = f"""
                <html>
                    <body>
                        <p>Hello,</p>
                        <p>Your payment of <strong>{amount} {currency}</strong> to TitanForge was successful. Thank you for your business!</p>
                        <p>You can view your subscription details in your dashboard.</p>
                        <p>Regards,<br>Your TitanForge Team</p>
                    </body>
                </html>
                """
                return self.send_user_email(user_email, subject, body, html_body)
            else:
                return {
                    "status": "error",
                    "message": "Missing payment details for success notification.",
                }

        elif notification_type == "subscription_canceled":
            user_email = data.get("user_email")
            if user_email:
                subject = "Your TitanForge Subscription Has Been Canceled"
                body = "Hello,\n\nYour subscription to TitanForge has been canceled as per your request.\nWe're sorry to see you go! You can resubscribe anytime.\n\nRegards,\nYour TitanForge Team"
                return self.send_user_email(user_email, subject, body)
            else:
                return {
                    "status": "error",
                    "message": "Missing user_email for cancellation notification.",
                }

        elif notification_type == "internal_error":
            error_message = data.get("error_message", "An unknown error occurred.")
            return self.send_internal_alert(
                f"Application Error: {error_message}", severity="error"
            )

        else:
            return {
                "status": "error",
                "message": f"Unknown notification type: {notification_type}",
            }
