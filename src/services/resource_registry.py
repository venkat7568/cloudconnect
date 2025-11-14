"""
ResourceRegistry - Registry Pattern implementation

SOLID Principles:
- SRP: Only manages resource type registration
- OCP: New types register themselves (no modification needed)

Design Pattern: REGISTRY PATTERN
- Self-registration mechanism
- Decouples Factory from concrete classes
"""

from typing import Dict, Type, List


class ResourceRegistry:
    """
    Maintains a registry of resource types.
    
    Pattern: Registry (Singleton-like with class variables)
    
    Usage:
        # Register (done automatically by resource classes):
        ResourceRegistry.register('AppService', AppService)
        
        # Retrieve:
        resource_class = ResourceRegistry.get('AppService')
        
        # List all:
        types = ResourceRegistry.list_types()
    """
    
    # Class variable - shared across all instances
    __registry: Dict[str, Type] = {}
    
    @classmethod
    def register(cls, name: str, resource_class: Type) -> Type:
        """
        Registers a resource class.
        
        Called automatically by resource classes via __registered pattern.
        
        Args:
            name: Resource type name (e.g., 'AppService')
            resource_class: The class itself (not an instance)
        
        Returns:
            The resource class (for convenience in __registered pattern)
        """
        cls.__registry[name] = resource_class
        return resource_class
    
    @classmethod
    def get(cls, name: str) -> Type:
        """
        Retrieves a resource class by name.
        
        Args:
            name: Resource type name
        
        Returns:
            The resource class
        
        Raises:
            KeyError: If resource type not found
        """
        if name not in cls.__registry:
            available = ', '.join(cls.__registry.keys())
            raise KeyError(
                f"Unknown resource type: '{name}'\n"
                f"Available types: {available}"
            )
        
        return cls.__registry[name]
    
    @classmethod
    def list_types(cls) -> List[str]:
        """
        Returns list of all registered resource type names.
        
        Returns:
            List of type names (e.g., ['AppService', 'StorageAccount', 'CacheDB'])
        """
        return list(cls.__registry.keys())
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Checks if a resource type is registered.
        
        Args:
            name: Resource type name
        
        Returns:
            True if registered, False otherwise
        """
        return name in cls.__registry
    
    @classmethod
    def clear(cls) -> None:
        """
        Clears the registry.
        
        WARNING: For testing purposes only!
        """
        cls.__registry.clear()