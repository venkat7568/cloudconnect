"""
Custom Exceptions for CloudConnect

SOLID: Single Responsibility - Each exception handles one error type
"""


class CloudConnectException(Exception):
    """Base exception for all CloudConnect errors"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidStateTransitionException(CloudConnectException):
    """
    Raised when an invalid state transition is attempted.
    
    Example: Trying to delete a resource that is still running
    """
    
    def __init__(self, current_state: str, operation: str, message: str = None):
        self.current_state = current_state
        self.operation = operation
        
        # Always include state and operation in the message for debugging
        if message is None:
            message = f"Cannot {operation} from {current_state} state"
        else:
            # Prepend state info to custom message for better debugging
            message = f"[{current_state} → {operation}] {message}"
        
        super().__init__(message)


class ResourceNotFoundException(CloudConnectException):
    """
    Raised when a resource is not found in the manager.
    
    Example: Trying to start a resource that doesn't exist
    """
    
    def __init__(self, resource_name: str):
        message = f"Resource '{resource_name}' not found"
        super().__init__(message)


class ResourceAlreadyExistsException(CloudConnectException):
    """
    Raised when trying to create a resource with a duplicate name.
    """
    
    def __init__(self, resource_name: str):
        message = f"Resource '{resource_name}' already exists"
        super().__init__(message)


class InvalidConfigurationException(CloudConnectException):
    """
    Raised when resource configuration is invalid.
    
    Example: Invalid runtime like "ruby" when only python/nodejs/dotnet allowed
    """
    
    def __init__(self, config_error: str):
        message = f"Invalid configuration: {config_error}"
        super().__init__(message)