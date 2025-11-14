"""
DeletedState - Terminal state (soft deletion)

Allowed transitions:
- start() → Error ✗ (cannot revive)
- stop() → Error ✗ (already deleted)
- delete() → Error ✗ (already deleted)

ALL operations blocked - this is FINAL state!
"""

from .resource_state import ResourceState
from ..exceptions import InvalidStateTransitionException


class DeletedState(ResourceState):
    """
    Terminal state - resource is soft-deleted.
    
    Resource is:
    - Marked as deleted (soft deletion)
    - Metadata preserved for audit trail
    - Cannot be revived
    - No operations allowed
    
    This is a TERMINAL state!
    """
    
    def start(self, resource) -> None:
        """
        Start deleted resource - NOT ALLOWED.
        
        Soft deletion is permanent!
        """
        raise InvalidStateTransitionException(
            current_state="Deleted",
            operation="start",
            message="Cannot start: Resource is deleted (soft deletion)"
        )
    
    def stop(self, resource) -> None:
        """
        Stop deleted resource - NOT ALLOWED.
        
        Already deleted!
        """
        raise InvalidStateTransitionException(
            current_state="Deleted",
            operation="stop",
            message="Cannot stop: Resource is deleted"
        )
    
    def delete(self, resource) -> None:
        """
        Delete again - NOT ALLOWED.
        
        Already deleted!
        """
        raise InvalidStateTransitionException(
            current_state="Deleted",
            operation="delete",
            message="Cannot delete: Resource already deleted"
        )
    
    def get_state_name(self) -> str:
        """Returns 'Deleted'"""
        return "Deleted"