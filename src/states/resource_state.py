"""
ResourceState - Abstract Base Class for State Pattern

SOLID Principles:
- OCP: Open for extension (new states), closed for modification
- LSP: All states substitutable
- ISP: Focused interface (only 4 methods)
- DIP: Resource depends on this abstraction
"""

from abc import ABC, abstractmethod


class ResourceState(ABC):
    """
    Abstract base class for resource lifecycle states.
    
    Design Pattern: STATE PATTERN
    - Encapsulates state-specific behavior
    - Allows state transitions
    - Validates operations based on current state
    
    Each state knows:
    - Which operations are allowed
    - What state to transition to
    - How to log operations
    """
    
    @abstractmethod
    def start(self, resource) -> None:
        """
        Handle start request.
        
        Args:
            resource: Resource instance to operate on
        
        Raises:
            InvalidStateTransitionException: If start not allowed from this state
        """
        pass
    
    @abstractmethod
    def stop(self, resource) -> None:
        """
        Handle stop request.
        
        Args:
            resource: Resource instance to operate on
        
        Raises:
            InvalidStateTransitionException: If stop not allowed from this state
        """
        pass
    
    @abstractmethod
    def delete(self, resource) -> None:
        """
        Handle delete request (soft deletion).
        
        Args:
            resource: Resource instance to operate on
        
        Raises:
            InvalidStateTransitionException: If delete not allowed from this state
        """
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        """
        Returns the name of this state.
        
        Returns:
            State name (e.g., "Created", "Started", "Stopped", "Deleted")
        """
        pass