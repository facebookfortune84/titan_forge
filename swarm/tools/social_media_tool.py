import facebook
from app.core.config import settings


class SocialMediaTool:
    def __init__(self):
        self.name = "social_media_poster"
        self.description = (
            "Posts content to social media platforms like Facebook and LinkedIn."
        )
        self.facebook_api = self._setup_facebook()

    def _setup_facebook(self):
        try:
            if settings.FACEBOOK_ACCESS_TOKEN:
                return facebook.GraphAPI(
                    access_token=settings.FACEBOOK_ACCESS_TOKEN, version="v19.0"
                )
            return None
        except Exception as e:
            print(f"Failed to initialize Facebook API: {e}")
            return None

    def post_to_facebook(self, message: str) -> str:
        if not self.facebook_api:
            return "Error: Facebook API is not configured."
        try:
            # In a real app, you might post to a specific page ID, e.g., 'me/feed'
            self.facebook_api.put_object(
                parent_object="me", connection_name="feed", message=message
            )
            return "Successfully posted to Facebook."
        except Exception as e:
            return f"Error posting to Facebook: {e}"

    def post_to_linkedin(self, message: str) -> str:
        # The 'linkedin-api' is unofficial and complex to use reliably here.
        # This serves as a placeholder for a real implementation.
        if not settings.LINKEDIN_ACCESS_TOKEN:
            return "Error: LinkedIn API is not configured."
        print("--- SIMULATING POST TO LINKEDIN ---")
        print(f"Message: {message}")
        print("--- END SIMULATION ---")
        return "Post to LinkedIn is currently a simulation. Integration with a library like 'requests-oauthlib' would be needed for a real implementation."

    def execute(self, platform: str, message: str) -> str:
        if platform.lower() == "facebook":
            return self.post_to_facebook(message)
        elif platform.lower() == "linkedin":
            return self.post_to_linkedin(message)
        else:
            return f"Error: Platform '{platform}' is not supported."
