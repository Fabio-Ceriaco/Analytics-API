from .routing import router


# Define the public API of the module
# This allows for easier imports from other parts of the application
# For example, from api.events import router
__all__ = ["router"]
