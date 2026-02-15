from pathlib import Path

from app.core.config import settings
from litellm import completion


class AgentCreator:
    """
    A tool for creating new agent Python files based on a role description.
    """

    def __init__(self):
        self.name = "agent_creator"
        self.description = "Creates a new Python file for an agent. Takes params: agent_name, role_description."
        self.agent_template = self._get_agent_template()

    def _get_agent_template(self):
        # A simple template for a new agent. The LLM will fill this in.
        return r"""
from swarm.agents.base_agent import BaseAgent
# Import any tools this agent might need

class {agent_class_name}(BaseAgent):
    \"\"\"
    An autonomous agent designed for the role of {role_description}.
    \"\"\"
    def __init__(self, model_name: str = "mock-response"):
        # Define the tools this agent has access to
        tools = [] # Example: [FileWriter(), FileReader()]
        super().__init__(role="{agent_name}", department="{department}", tools=tools, model_name=model_name)

    def execute_task(self, task_description: str) -> str:
        # Poll for new messages (tasks)
        message = self.receive_message()
        if message:
            task_description = message['message']
        
        task_id = self._get_task_id(task_description)
        if task_id:
            self.update_task_status(task_id, "in_progress")

        print(f"[{self.role}] Received task: {{task_description}}")
        action = self.think(task_description) # Let the LLM decide the best action

        try:
            if action["tool"] != "none":
                print(f"[{self.role}] Using tool: {{action['tool']}} with params: {{action['params']}}")
                result = self.use_tool(action["tool"], **action["params"])
            else:
                result = f"{{self.role}} performed its duties: {{task_description}}"
            
            if task_id:
                self.update_task_status(task_id, "completed")
            return result
        except Exception as e:
            if task_id:
                self.update_task_status(task_id, "failed")
            return f"An error occurred during {{self.role}}'s task: {{e}}"
"""

    def execute(self, agent_name: str, role_description: str) -> str:
        """
        Creates a new agent Python file and uses the LLM to fill in its details.
        """
        try:
            agent_class_name = "".join(
                [word.capitalize() for word in agent_name.split()]
            )
            file_name = f"{agent_name.replace(' ', '_').lower()}.py"

            # Determine save path (e.g., a 'new_recruits' subfolder for review)
            save_path = Path(
                "F:/TitanForge/swarm/departments/human_capital/new_recruits"
            )
            save_path.mkdir(parents=True, exist_ok=True)
            file_path = save_path / file_name

            # Use LLM to fill in the template
            template = self.agent_template.format(
                agent_class_name=agent_class_name,
                agent_name=agent_name,
                department="HumanCapital",
                role_description=role_description,
            )
            llm_prompt = f"""
            You are an expert Python software engineer. Your task is to generate the Python code for a new autonomous agent.
            The agent should inherit from `BaseAgent`.
            Fill in the template below for an agent named '{agent_name}' with the role description: '{role_description}'.
            
            Based on the role, determine what tools (from the `swarm.tools` directory) this agent should have access to.
            Import these tools at the top.
            
            Provide only the Python code, with no additional commentary or markdown.
            
            Template:
            {template}
            """

            messages = [{"role": "user", "content": llm_prompt}]
            # Use a higher temperature for more creative agent code generation
            response = completion(
                model=settings.LLM_MODEL_NAME, messages=messages, temperature=0.7
            )
            generated_code = response.choices[0].message.content

            with open(file_path, "w") as f:
                f.write(generated_code)

            # Add new agent to agent_registry for dynamic update (simulated for now)
            # In a real system, the MCP would need to dynamically load/register agents.
            print(
                f"--- Dynamically registering new agent: {agent_name.replace(' ', '_').lower()} ---"
            )

            return f"Successfully created new agent file: {file_path}. Agent '{agent_name}' is ready for review and integration."

        except Exception as e:
            return f"Error creating agent: {e}"
