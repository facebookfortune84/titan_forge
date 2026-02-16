import subprocess


class ShellCommand:
    """
    A tool for executing shell commands.
    """

    def __init__(self):
        self.name = "shell_command"
        self.description = "Executes a shell command. Use with extreme caution."

    def execute(self, command: str) -> str:
        """
        Executes the given shell command.
        """
        print(f"WARNING: Executing shell command: {command}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error executing command: {result.stderr}"
        except Exception as e:
            return f"Error executing command '{command}': {e}"
