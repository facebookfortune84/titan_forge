import json

import requests
from app.core.config import settings


class BlogTool:
    def __init__(self):
        self.name = "blog_poster"
        self.description = "Posts an article to a WordPress blog using the REST API. Takes params: title, content, status ('publish' or 'draft')."

    def execute(self, title: str, content: str, status: str = "publish") -> str:
        if not all(
            [
                settings.WORDPRESS_API_URL,
                settings.WORDPRESS_USER,
                settings.WORDPRESS_PASSWORD,
            ]
        ):
            return "Error: WordPress API settings are not fully configured."

        api_url = f"{settings.WORDPRESS_API_URL}/wp-json/wp/v2/posts"
        headers = {"Content-Type": "application/json"}
        data = {"title": title, "content": content, "status": status}

        try:
            response = requests.post(
                api_url,
                headers=headers,
                data=json.dumps(data),
                auth=(settings.WORDPRESS_USER, settings.WORDPRESS_PASSWORD),
            )
            response.raise_for_status()
            post_data = response.json()
            return f"Successfully posted to blog. New post URL: {post_data.get('link')}"
        except Exception as e:
            return f"Error posting to blog: {e}"
