"""
Resource - Abstract Base Class

SOLID Principles:
- SRP: Manages common resource attributes and lifecycle
- OCP: Open for extension (new resource types)
- LSP: All subclasses substitutable
- DIP: Depends on ResourceState abstraction

Design Pattern: Template Method Pattern
- Defines skeleton (lifecycle methods)
- Subclasses provide details (config, validation)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any

from ..states.created_state import CreatedState
from ..utils.logger import Logger


class Resource(ABC):
    """
    Abstract base class for all cloud resources.
    
    Common Attributes:
    - name: Resource identifier
    - state: Current lifecycle state
    - logger: For operation logging
    - created_at: Creation timestamp
    - is_deleted: Soft deletion flag
    
    Common Methods:
    - Lifecycle: start(), stop(), delete()
    - State management: get_state(), set_state()
    - Logging: log()
    
    Abstract Methods (subclasses must implement):
    - get_config(): Return resource-specific configuration
    - validate_config(): Validate resource-specific configuration
    """
    
    def __init__(self, name: str):
        """
        Initialize common resource attributes.
        
        Args:
            name: Unique resource identifier
        
        Raises:
            ValueError: If name is empty
        """
        # Validate name
        if not name or not name.strip():
            raise ValueError("Resource name cannot be empty")
        
        # Initialize attributes
        self.__name = name.strip()
        self.__state = CreatedState()  # Initial state
        self.__logger = Logger()
        self.__created_at = datetime.now()
        self.__is_deleted = False
        
        # Log creation
        self.log("created")
    
    # ==================== LIFECYCLE METHODS ====================
    
    def start(self) -> None:
        """
        Start the resource.
        
        Delegates to current state - State Pattern!
        
        Raises:
            InvalidStateTransitionException: If start not allowed from current state
        """
        self.__state.start(self)
    
    def stop(self) -> None:
        """
        Stop the resource.
        
        Delegates to current state - State Pattern!
        
        Raises:
            InvalidStateTransitionException: If stop not allowed from current state
        """
        self.__state.stop(self)
    
    def delete(self) -> None:
        """
        Delete the resource (soft deletion).
        
        Delegates to current state - State Pattern!
        Metadata is preserved for audit trail.
        
        Raises:
            InvalidStateTransitionException: If delete not allowed from current state
        """
        self.__state.delete(self)
    
    # ==================== GETTERS ====================
    
    def get_name(self) -> str:
        """Returns resource name"""
        return self.__name
    
    def get_state(self):
        """Returns current state object"""
        return self.__state
    
    def get_created_at(self) -> datetime:
        """Returns creation timestamp"""
        return self.__created_at
    
    def is_deleted(self) -> bool:
        """Returns True if resource is deleted"""
        return self.__is_deleted
    
    # ==================== STATE MANAGEMENT ====================
    
    def set_state(self, state) -> None:
        """
        Changes current state.
        
        Called by state objects during transitions.
        
        Args:
            state: New ResourceState instance
        """
        self.__state = state
    
    # ==================== LOGGING ====================
    
    def log(self, message: str) -> None:
        """
        Logs an operation.
        
        Args:
            message: Operation description
        """
        resource_type = self.__class__.__name__
        config = self.get_config()
        self.__logger.log(resource_type, message, config)
    
    # ==================== ABSTRACT METHODS ====================
    
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """
        Returns resource configuration.
        
        MUST be implemented by subclasses.
        Each resource type has different configuration.
        
        Returns:
            Configuration dictionary
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validates resource configuration.
        
        MUST be implemented by subclasses.
        Each resource type has different validation rules.
        
        Returns:
            True if valid
        
        Raises:
            InvalidConfigurationException: If configuration is invalid
        """
        pass
    
    # ==================== STRING REPRESENTATION ====================
    
    def __str__(self) -> str:
        """String representation for display"""
        state_name = self.__state.get_state_name()
        return f"{self.__class__.__name__} '{self.__name}' (State: {state_name})"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging"""
        return f"{self.__class__.__name__}(name={self.__name}, state={self.__state.get_state_name()})"