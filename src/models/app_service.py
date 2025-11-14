"""
AppService - Web application hosting service

Configuration:
- runtime: Programming language (python/nodejs/dotnet)
- region: Deployment location (EastUS/WestEurope/CentralIndia)
- replica_count: Number of instances (1/2/3)
"""

from typing import Dict, Any
from .resource import Resource
from ..exceptions import InvalidConfigurationException


class AppService(Resource):
    """
    Represents a web application service.
    
    Use Case: Host web applications with multiple replicas
    Example: Node.js app running in West Europe with 2 replicas
    
    Extends Resource and provides app-specific configuration.
    """
    
    # Valid configuration values
    VALID_RUNTIMES = ['python', 'nodejs', 'dotnet']
    VALID_REGIONS = ['EastUS', 'WestEurope', 'CentralIndia']
    VALID_REPLICA_COUNTS = [1, 2, 3]
    
    def __init__(self, name: str, runtime: str, region: str, replica_count: int):
        """
        Initialize AppService.
        
        Args:
            name: Resource name
            runtime: Programming language
            region: Deployment region
            replica_count: Number of instances
        
        Raises:
            InvalidConfigurationException: If configuration is invalid
        """
        # Set specific attributes
        self.__runtime = runtime
        self.__region = region
        self.__replica_count = replica_count
        
        # Validate configuration BEFORE calling parent constructor
        # (parent logs creation, so we need valid config)
        self.validate_config()
        
        # Call parent constructor (sets common attributes)
        super().__init__(name)
    
    def get_config(self) -> Dict[str, Any]:
        """
        Returns AppService configuration.
        
        Returns:
            Configuration dictionary with runtime, region, replica_count
        """
        return {
            'runtime': self.__runtime,
            'region': self.__region,
            'replica_count': self.__replica_count
        }
    
    def validate_config(self) -> bool:
        """
        Validates AppService configuration.
        
        Returns:
            True if valid
        
        Raises:
            InvalidConfigurationException: If any validation fails
        """
        # Validate runtime
        if self.__runtime not in self.VALID_RUNTIMES:
            raise InvalidConfigurationException(
                f"Invalid runtime '{self.__runtime}'. "
                f"Must be one of: {', '.join(self.VALID_RUNTIMES)}"
            )
        
        # Validate region
        if self.__region not in self.VALID_REGIONS:
            raise InvalidConfigurationException(
                f"Invalid region '{self.__region}'. "
                f"Must be one of: {', '.join(self.VALID_REGIONS)}"
            )
        
        # Validate replica count
        if self.__replica_count not in self.VALID_REPLICA_COUNTS:
            raise InvalidConfigurationException(
                f"Invalid replica count {self.__replica_count}. "
                f"Must be one of: {', '.join(map(str, self.VALID_REPLICA_COUNTS))}"
            )
        
        return True
    
    # Getters for specific attributes
    def get_runtime(self) -> str:
        """Returns runtime"""
        return self.__runtime
    
    def get_region(self) -> str:
        """Returns region"""
        return self.__region
    
    def get_replica_count(self) -> int:
        """Returns replica count"""
        return self.__replica_count


# Self-register with ResourceRegistry
# This line executes when module is imported
from ..services.resource_registry import ResourceRegistry
__registered = ResourceRegistry.register('AppService', AppService)