"""
StartedState - Resource is running

Allowed transitions:
- start() → Error ✗ (already running)
- stop() → StoppedState ✓
- delete() → Error ✗ (must stop first - SAFETY)
"""

from .resource_state import ResourceState
from ..exceptions import InvalidStateTransitionException


class StartedState(ResourceState):
    """
    State when resource is running.
    
    Resource is:
    - Currently running
    - Can be stopped
    - Cannot be started (already running)
    - Cannot be deleted (safety - must stop first)
    """
    
    def start(self, resource) -> None:
        """
        Start the resource - NOT ALLOWED.
        
        Already running!
        """
        raise InvalidStateTransitionException(
            current_state="Started",
            operation="start",
            message="Cannot start: Resource already running"
        )
    
    def stop(self, resource) -> None:
        """
        Stop the running resource - ALLOWED.
        
        Transitions: Started → Stopped
        """
        # Import here to avoid circular dependency
        from .stopped_state import StoppedState
        
        # Change state
        resource.set_state(StoppedState())
        
        # Log operation
        resource.log("stopped")
    
    def delete(self, resource) -> None:
        """
        Delete running resource - NOT ALLOWED (SAFETY).
        
        Must stop before deleting!
        """
        raise InvalidStateTransitionException(
            current_state="Started",
            operation="delete",
            message="Cannot delete: Must stop resource first"
        )
    
    def get_state_name(self) -> str:
        """Returns 'Started'"""
        return "Started"