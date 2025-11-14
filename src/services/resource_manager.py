"""
ResourceManager - Storage and retrieval of resources

SOLID Principles:
- SRP: Only manages resource storage/retrieval
- OCP: Can extend with new management features

Design Pattern: Repository Pattern
- Abstracts storage mechanism
- Provides CRUD operations
"""

from typing import Dict, List
from ..models.resource import Resource
from ..exceptions import ResourceNotFoundException, ResourceAlreadyExistsException


class ResourceManager:
    """
    Manages storage and retrieval of resources.
    
    Pattern: Repository Pattern
    - In-memory storage using dictionary
    - Quick O(1) lookup by name
    - Could be extended to use database later
    
    Usage:
        manager = ResourceManager()
        manager.add_resource(resource)
        resource = manager.get_resource('my-app')
    """
    
    def __init__(self):
        """Initialize with empty storage"""
        self.__resources: Dict[str, Resource] = {}
    
    def add_resource(self, resource: Resource) -> None:
        """
        Adds a resource to storage.
        
        Args:
            resource: Resource instance to add
        
        Raises:
            ResourceAlreadyExistsException: If resource with same name exists
        """
        name = resource.get_name()
        
        # Check for duplicates
        if name in self.__resources:
            raise ResourceAlreadyExistsException(name)
        
        # Add to storage
        self.__resources[name] = resource
    
    def get_resource(self, name: str) -> Resource:
        """
        Retrieves a resource by name.
        
        Args:
            name: Resource name
        
        Returns:
            Resource instance
        
        Raises:
            ResourceNotFoundException: If resource not found
        """
        if name not in self.__resources:
            raise ResourceNotFoundException(name)
        
        return self.__resources[name]
    
    def remove_resource(self, name: str) -> None:
        """
        Removes a resource from storage.
        
        Note: This is physical removal (hard delete).
        Different from resource.delete() which is soft delete.
        
        Args:
            name: Resource name
        
        Raises:
            ResourceNotFoundException: If resource not found
        """
        if name not in self.__resources:
            raise ResourceNotFoundException(name)
        
        del self.__resources[name]
    
    def list_resources(self, include_deleted: bool = False) -> List[Resource]:
        """
        Returns list of all resources.
        
        Args:
            include_deleted: If False, excludes soft-deleted resources
        
        Returns:
            List of Resource instances
        """
        resources = list(self.__resources.values())
        
        if not include_deleted:
            # Filter out soft-deleted resources
            resources = [r for r in resources if not r.is_deleted()]
        
        return resources
    
    def get_resource_names(self, include_deleted: bool = False) -> List[str]:
        """
        Returns list of resource names.
        
        Args:
            include_deleted: If False, excludes soft-deleted resources
        
        Returns:
            List of resource names
        """
        resources = self.list_resources(include_deleted)
        return [r.get_name() for r in resources]
    
    def resource_exists(self, name: str) -> bool:
        """
        Checks if a resource exists.
        
        Args:
            name: Resource name
        
        Returns:
            True if exists, False otherwise
        """
        return name in self.__resources
    
    def count(self, include_deleted: bool = False) -> int:
        """
        Returns count of resources.
        
        Args:
            include_deleted: If False, excludes soft-deleted resources
        
        Returns:
            Number of resources
        """
        return len(self.list_resources(include_deleted))
    
    def clear(self) -> None:
        """
        Removes all resources from storage.
        
        WARNING: Destructive operation! Use with caution.
        """
        self.__resources.clear()