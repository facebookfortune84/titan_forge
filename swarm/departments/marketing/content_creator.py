from swarm.agents.base_agent import BaseAgent
from swarm.tools.blog_tool import BlogTool  # New import
from swarm.tools.file_writer import FileWriter
from swarm.tools.social_media_tool import SocialMediaTool  # New import


class ContentCreator(BaseAgent):
    """
    A content creator agent in the Marketing department.
    """

    def __init__(self, model_name: str = "mock-response"):
        tools = [FileWriter(), BlogTool(), SocialMediaTool()]  # Add new tools
        super().__init__(
            role="Content Creator",
            department="Marketing",
            tools=tools,
            model_name=model_name,
        )

    def execute_task(self, task_description: str) -> str:
        """
        Executes content creation tasks.
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

                # --- New Workflow: Post to Blog and Notify Social Media ---
                if (
                    action["tool"] == "file_writer"
                    and "blog" in task_description.lower()
                ):
                    # Assume the content was meant for a blog post
                    
                    # In a real scenario, the LLM would help craft title/content,
                    # here we'll simulate it.
                    title = f"New Article: {task_description[:50]}..."
                    content_for_blog = action["params"].get(
                        "content", "Default blog content."
                    )  # Use written content

                    # 1. Post to blog
                    print(f"[{self.role}] Publishing content to blog: '{title}'")
                    blog_tool_instance = BlogTool()
                    blog_post_url = blog_tool_instance.execute(
                        title=title, content=content_for_blog
                    )
                    result += f"\nBlog Post Result: {blog_post_url}"

                    # 2. Notify Social Media Manager
                    if "Successfully posted to blog" in blog_post_url:
                        social_media_message = f"New blog post just published! '{title}'. Check it out at {blog_post_url}"
                        self.send_message("social_media_manager", social_media_message)
                        result += "\nSocial Media Manager notified for promotion."
                    else:
                        result += (
                            "\nBlog post failed, not notifying Social Media Manager."
                        )

            else:
                result = f"Generated content for: {task_description}"

            if task_id:
                self.update_task_status(task_id, "completed")

            return result
        except Exception as e:
            if task_id:
                self.update_task_status(task_id, "failed")
            return f"An error occurred: {e}"
