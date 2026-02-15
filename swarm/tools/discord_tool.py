import requests


class DiscordTool:
    """
    A tool for interacting with Discord via webhooks.
    """

    def __init__(self):
        self.name = "discord_notifier"
        self.description = "Sends messages to a Discord channel via a webhook. Takes params: webhook_url, message."

    def execute(self, webhook_url: str, message: str) -> str:
        """
        Sends a message to the specified Discord webhook.
        """
        if not webhook_url:
            return "Error: Discord webhook URL is not provided."

        payload = {"content": message}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(webhook_url, json=payload, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            return f"Successfully sent message to Discord webhook: {webhook_url}"
        except Exception as e:
            return f"Error sending message to Discord: {e}"
