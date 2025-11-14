"""
ResourceFactory - Factory Pattern implementation

SOLID Principles:
- SRP: Only creates resources
- OCP: New types don't require factory changes
- DIP: Depends on ResourceRegistry abstraction

Design Pattern: FACTORY PATTERN
- Creates resources dynamically by type
- Decoupled from concrete resource classes
"""

from typing import Dict, Any
from .resource_registry import ResourceRegistry
from ..models.resource import Resource


class ResourceFactory:
    """
    Creates resources dynamically without if-else chains.
    
    Pattern: Factory Pattern with Registry
    
    Usage:
        resource = ResourceFactory.create_resource(
            'AppService',
            'my-app',
            {'runtime': 'python', 'region': 'WestEurope', 'replica_count': 2}
        )
    
    Key Benefits:
    - No if-else chains
    - Adding new resource type = just create class and register
    - Follows OCP (Open/Closed Principle)
    """
    
    @staticmethod
    def create_resource(resource_type: str, name: str, config: Dict[str, Any]) -> Resource:
        """
        Creates a resource dynamically.
        
        Args:
            resource_type: Type of resource (e.g., 'AppService')
            name: Resource name
            config: Configuration dictionary
        
        Returns:
            Resource instance
        
        Raises:
            KeyError: If resource type not registered
            InvalidConfigurationException: If configuration is invalid
        
        Example:
            resource = ResourceFactory.create_resource(
                'AppService',
                'my-app',
                {'runtime': 'python', 'region': 'WestEurope', 'replica_count': 2}
            )
        """
        # Step 1: Query registry for class
        resource_class = ResourceRegistry.get(resource_type)
        
        # Step 2: Instantiate with configuration
        # Equivalent to: AppService(name, runtime=..., region=..., replica_count=...)
        return resource_class(name, **config)
    
    @staticmethod
    def get_available_types() -> list:
        """
        Returns list of available resource types.
        
        Returns:
            List of type names
        """
        return ResourceRegistry.list_types()