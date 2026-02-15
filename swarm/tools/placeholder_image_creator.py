from PIL import Image


class PlaceholderImageCreator:
    """
    A tool for creating simple placeholder images.
    """

    def __init__(self):
        self.name = "placeholder_image_creator"
        self.description = "Creates a simple placeholder image with a solid color. Takes params: file_path, width, height, color."

    def execute(
        self, file_path: str, width: int, height: int, color: str = "grey"
    ) -> str:
        """
        Creates and saves a placeholder image.
        """
        try:
            width, height = int(width), int(height)
            img = Image.new("RGB", (width, height), color=color)
            img.save(file_path)
            return f"Successfully created placeholder image at {file_path}"
        except Exception as e:
            return f"Error creating image: {e}"
