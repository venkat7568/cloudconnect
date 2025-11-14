"""
CreatedState - Initial state after resource creation

Allowed transitions:
- start() → StartedState ✓
- stop() → Error ✗ (not running yet)
- delete() → DeletedState ✓ (cleanup unused)
"""

from .resource_state import ResourceState
from ..exceptions import InvalidStateTransitionException


class CreatedState(ResourceState):
    """
    Initial state when resource is created.
    
    Resource is:
    - Created but not started
    - Can be started
    - Can be deleted (cleanup)
    - Cannot be stopped (not running)
    """
    
    def start(self, resource) -> None:
        """
        Start the resource - ALLOWED.
        
        Transitions: Created → Started
        """
        # Import here to avoid circular dependency
        from .started_state import StartedState
        
        # Change state
        resource.set_state(StartedState())
        
        # Log operation
        config = resource.get_config()
        region = config.get('region', 'unknown region')
        resource.log(f"started in {region}")
    
    def stop(self, resource) -> None:
        """
        Stop the resource - NOT ALLOWED.
        
        Resource not started yet!
        """
        raise InvalidStateTransitionException(
            current_state="Created",
            operation="stop",
            message="Cannot stop: Resource not started yet"
        )
    
    def delete(self, resource) -> None:
        """
        Delete unused resource - ALLOWED.
        
        Transitions: Created → Deleted
        """
        # Import here to avoid circular dependency
        from .deleted_state import DeletedState
        
        # Change state
        resource.set_state(DeletedState())
        
        # Set deletion flag
        resource._Resource__is_deleted = True
        
        # Log operation
        resource.log("marked as deleted (unused)")
    
    def get_state_name(self) -> str:
        """Returns 'Created'"""
        return "Created"