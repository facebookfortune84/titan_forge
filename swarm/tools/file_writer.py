class FileWriter:
    """
    A tool for writing content to a file.
    """

    def __init__(self):
        self.name = "file_writer"
        self.description = "Writes content to a specified file."

    def execute(self, file_path: str, content: str) -> str:
        """
        Writes the given content to the specified file.
        """
        try:
            with open(file_path, "w") as f:
                f.write(content)
            return f"Successfully wrote to file: {file_path}"
        except Exception as e:
            return f"Error writing to file '{file_path}': {e}"
