# Import the necessary modules
from .load_settings import load_settings

# Create pro client from load settings
class ProClient:
    def __init__(self):
        self.settings = load_settings()
        # Additional initialization can go here

    def some_method(self):
        # Method implementation
        pass

# Register tools
class ToolRegistrar:
    def __init__(self):
        self.tools = []

    def register_tool(self, tool):
        self.tools.append(tool)

    def get_tools(self):
        return self.tools

registrar = ToolRegistrar()