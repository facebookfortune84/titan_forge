import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests
from litellm import completion


class BaseAgent(ABC):
    """
    The base class for all agents in the TitanForge swarm.
    It includes capabilities for tool usage, communication, and memory,
    and uses an LLM for intelligent decision-making.
    """

    def __init__(
        self,
        role: str,
        department: str,
        tools: List[Any] = [],
        model_name: str = "mock-response",
    ):
        self.agent_id = role.replace(" ", "_").lower()  # A unique ID for the agent
        self.role = role
        self.department = department
        self.tools = {tool.name: tool for tool in tools}
        self.model_name = model_name
        self.mcp_api_url = "http://127.0.0.1:8000"  # URL of the MCP

    def get_tool_descriptions(self) -> str:
        """Returns a string describing the available tools."""
        if not self.tools:
            return "No tools available."
        return "\n".join(
            [f"- {name}: {tool.description}" for name, tool in self.tools.items()]
        )

    def think(self, task_description: str) -> Dict[str, Any]:
        """
        The "brain" of the agent. Uses an LLM to decide which tool to use.
        """
        if not self.tools:
            return {"tool": "none", "params": {}}

        tool_descriptions = self.get_tool_descriptions()

        system_prompt = f"""
        You are an intelligent agent's thinking module. Your role is to choose the best tool to accomplish a given task.
        You must respond in JSON format.

        The available tools are:
        {tool_descriptions}

        Based on the user's task, decide which tool to use.
        If no tool is appropriate, respond with "{{'tool': 'none', 'params': {{}}}}".
        If a tool is appropriate, respond with a JSON object containing the tool name and its parameters.
        For example: {{"tool": "file_writer", "params": {{"file_path": "example.txt", "content": "Hello from the agent!"}}}}

        Parameter values should be extracted directly from the user's task.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {task_description}"},
        ]

        try:
            response = completion(model=self.model_name, messages=messages)

            # The actual message content from the LLM is in choices[0].message.content
            llm_output_str = response.choices[0].message.content

            # Parse the JSON string from the LLM's response
            decision = json.loads(llm_output_str)

            # Basic validation of the decision
            if "tool" in decision and "params" in decision:
                return decision
            else:
                print(
                    f"Warning: LLM output is not in the expected format: {llm_output_str}"
                )
                return {"tool": "none", "params": {}}

        except Exception as e:
            print(f"Error during LLM completion or JSON parsing: {e}")
            return {"tool": "none", "params": {}}

    def use_tool(self, tool_name: str, **kwargs) -> str:
        """
        Executes a tool with the given parameters.
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."
        try:
            tool = self.tools[tool_name]
            return tool.execute(**kwargs)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {e}"

    # --- Communication Methods ---

    def send_message(self, recipient_id: str, message: str):
        """Sends a message to another agent via the MCP message bus."""
        try:
            response = requests.post(
                f"{self.mcp_api_url}/messages/send",
                json={
                    "sender_id": self.agent_id,
                    "recipient_id": recipient_id,
                    "message": message,
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to send message: {e}"}

    def receive_message(self):
        """Receives a message from the agent's queue on the MCP message bus."""
        try:
            response = requests.get(
                f"{self.mcp_api_url}/messages/receive/{self.agent_id}"
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message")
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to receive message: {e}"}

    # --- Memory Methods ---

    def save_to_long_term_memory(self, document: str, metadata: Dict[str, Any]):
        """Saves a document to the long-term memory via the MCP."""
        try:
            response = requests.post(
                f"{self.mcp_api_url}/memory/long_term/add",
                json={
                    "agent_id": self.agent_id,
                    "document": document,
                    "metadata": metadata,
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to save to long-term memory: {e}"}

    def retrieve_from_long_term_memory(self, query_text: str, n_results: int = 3):
        """Retrieves documents from the long-term memory via the MCP."""
        try:
            response = requests.post(
                f"{self.mcp_api_url}/memory/long_term/query",
                json={
                    "agent_id": self.agent_id,
                    "query_text": query_text,
                    "n_results": n_results,
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to retrieve from long-term memory: {e}"}

    def save_to_short_term_memory(self, key: str, value: Any):
        """Saves a key-value pair to the short-term memory via the MCP."""
        try:
            response = requests.post(
                f"{self.mcp_api_url}/memory/short_term/add",
                json={"agent_id": self.agent_id, "key": key, "value": value},
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to save to short-term memory: {e}"}

    def retrieve_from_short_term_memory(self):
        """Retrieves the short-term memory for the agent via the MCP."""
        try:
            response = requests.get(
                f"{self.mcp_api_url}/memory/short_term/{self.agent_id}"
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to retrieve from short-term memory: {e}"}

    # --- Task Management Methods ---

    def _get_task_id(self, task_description: str) -> str | None:
        """Extracts the task ID from the task description string."""
        if not task_description:
            return None
        match = re.search(r"Task ID: ([\w-]+)", task_description)
        return match.group(1) if match else None

    def update_task_status(self, task_id: str, status: str):
        """Updates the status of a task via the MCP."""
        try:
            response = requests.put(
                f"{self.mcp_api_url}/tasks/{task_id}",
                json={"status": status, "agent_id": self.agent_id},
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating task status: {e}")
            return {"error": f"Failed to update task status: {e}"}

    @abstractmethod
    def execute_task(self, task_description: str) -> str:
        """
        Execute a given task.
        """
        pass

    def __repr__(self):
        return f"BaseAgent(role='{self.role}', department='{self.department}')"
