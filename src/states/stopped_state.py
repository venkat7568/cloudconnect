"""
StoppedState - Resource is paused

Allowed transitions:
- start() → StartedState ✓ (can restart)
- stop() → Error ✗ (already stopped)
- delete() → DeletedState ✓ (safe to delete)
"""

from .resource_state import ResourceState
from ..exceptions import InvalidStateTransitionException


class StoppedState(ResourceState):
    """
    State when resource is stopped/paused.
    
    Resource is:
    - Paused/stopped
    - Can be restarted
    - Can be deleted (safe now)
    - Cannot be stopped again (already stopped)
    """
    
    def start(self, resource) -> None:
        """
        Restart the resource - ALLOWED.
        
        Transitions: Stopped → Started
        """
        # Import here to avoid circular dependency
        from .started_state import StartedState
        
        # Change state
        resource.set_state(StartedState())
        
        # Log operation
        config = resource.get_config()
        region = config.get('region', 'unknown region')
        resource.log(f"restarted in {region}")
    
    def stop(self, resource) -> None:
        """
        Stop the resource - NOT ALLOWED.
        
        Already stopped!
        """
        raise InvalidStateTransitionException(
            current_state="Stopped",
            operation="stop",
            message="Cannot stop: Resource already stopped"
        )
    
    def delete(self, resource) -> None:
        """
        Delete stopped resource - ALLOWED.
        
        Transitions: Stopped → Deleted
        
        This is the normal deletion path!
        """
        # Import here to avoid circular dependency
        from .deleted_state import DeletedState
        
        # Change state
        resource.set_state(DeletedState())
        
        # Set deletion flag
        resource._Resource__is_deleted = True
        
        # Log operation
        resource.log("marked as deleted")
    
    def get_state_name(self) -> str:
        """Returns 'Stopped'"""
        return "Stopped"