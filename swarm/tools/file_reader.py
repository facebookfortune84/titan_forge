class FileReader:
    """
    A tool for reading content from a file.
    """

    def __init__(self):
        self.name = "file_reader"
        self.description = "Reads content from a specified file."

    def execute(self, file_path: str) -> str:
        """
        Reads the content of the specified file.
        """
        try:
            with open(file_path, "r") as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file '{file_path}': {e}"
