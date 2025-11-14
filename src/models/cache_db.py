"""
CacheDB - In-memory cache database

Configuration:
- ttl_seconds: Time to live (how long data stays in cache)
- capacity_mb: Maximum memory capacity
- eviction_policy: How to remove data when full (LRU/FIFO/LFU)
"""

from typing import Dict, Any
from .resource import Resource
from ..exceptions import InvalidConfigurationException


class CacheDB(Resource):
    """
    Represents an in-memory cache database.
    
    Use Case: Fast data caching with automatic expiration
    Example: Redis-like cache with 1-hour TTL and LRU eviction
    
    Extends Resource and provides cache-specific configuration.
    """
    
    # Valid eviction policies
    VALID_EVICTION_POLICIES = ['LRU', 'FIFO', 'LFU']
    
    # Validation constraints
    MIN_TTL_SECONDS = 60  # 1 minute
    MAX_TTL_SECONDS = 86400  # 24 hours
    MIN_CAPACITY_MB = 128  # 128 MB
    MAX_CAPACITY_MB = 16384  # 16 GB
    
    def __init__(self, name: str, ttl_seconds: int, 
                 capacity_mb: int, eviction_policy: str):
        """
        Initialize CacheDB.
        
        Args:
            name: Resource name
            ttl_seconds: Time to live in seconds
            capacity_mb: Memory capacity in MB
            eviction_policy: Eviction strategy (LRU/FIFO/LFU)
        
        Raises:
            InvalidConfigurationException: If configuration is invalid
        """
        # Set specific attributes
        self.__ttl_seconds = ttl_seconds
        self.__capacity_mb = capacity_mb
        self.__eviction_policy = eviction_policy.upper()  # Normalize to uppercase
        
        # Validate configuration
        self.validate_config()
        
        # Call parent constructor
        super().__init__(name)
    
    def get_config(self) -> Dict[str, Any]:
        """
        Returns CacheDB configuration.
        
        Returns:
            Configuration dictionary with TTL, capacity, eviction policy
        """
        return {
            'ttl_seconds': self.__ttl_seconds,
            'capacity_mb': self.__capacity_mb,
            'eviction_policy': self.__eviction_policy
        }
    
    def validate_config(self) -> bool:
        """
        Validates CacheDB configuration.
        
        Returns:
            True if valid
        
        Raises:
            InvalidConfigurationException: If any validation fails
        """
        # Validate TTL
        if not isinstance(self.__ttl_seconds, int):
            raise InvalidConfigurationException(
                "ttl_seconds must be an integer"
            )
        
        if self.__ttl_seconds < self.MIN_TTL_SECONDS or \
           self.__ttl_seconds > self.MAX_TTL_SECONDS:
            raise InvalidConfigurationException(
                f"ttl_seconds must be between {self.MIN_TTL_SECONDS} and "
                f"{self.MAX_TTL_SECONDS} (1 minute to 24 hours)"
            )
        
        # Validate capacity
        if not isinstance(self.__capacity_mb, int):
            raise InvalidConfigurationException(
                "capacity_mb must be an integer"
            )
        
        if self.__capacity_mb < self.MIN_CAPACITY_MB or \
           self.__capacity_mb > self.MAX_CAPACITY_MB:
            raise InvalidConfigurationException(
                f"capacity_mb must be between {self.MIN_CAPACITY_MB} and "
                f"{self.MAX_CAPACITY_MB} (128MB to 16GB)"
            )
        
        # Validate eviction policy
        if self.__eviction_policy not in self.VALID_EVICTION_POLICIES:
            raise InvalidConfigurationException(
                f"Invalid eviction policy '{self.__eviction_policy}'. "
                f"Must be one of: {', '.join(self.VALID_EVICTION_POLICIES)}\n"
                f"  - LRU: Least Recently Used\n"
                f"  - FIFO: First In First Out\n"
                f"  - LFU: Least Frequently Used"
            )
        
        return True
    
    # Getters
    def get_ttl_seconds(self) -> int:
        """Returns TTL"""
        return self.__ttl_seconds
    
    def get_capacity_mb(self) -> int:
        """Returns capacity"""
        return self.__capacity_mb
    
    def get_eviction_policy(self) -> str:
        """Returns eviction policy"""
        return self.__eviction_policy


# Self-register with ResourceRegistry
from ..services.resource_registry import ResourceRegistry
__registered = ResourceRegistry.register('CacheDB', CacheDB)