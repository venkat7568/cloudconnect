"""
StorageAccount - Cloud storage service

Configuration:
- encryption_enabled: Whether data is encrypted at rest (True/False)
- access_key: Secret key for authentication
- max_size_gb: Maximum storage capacity in GB
"""

from typing import Dict, Any
from .resource import Resource
from ..exceptions import InvalidConfigurationException


class StorageAccount(Resource):
    """
    Represents a cloud storage account.
    
    Use Case: Store files, documents, and data in the cloud
    Example: 500GB encrypted storage with secure access key
    
    Extends Resource and provides storage-specific configuration.
    """
    
    # Validation constraints
    MIN_SIZE_GB = 1
    MAX_SIZE_GB = 10000  # 10TB max
    MIN_KEY_LENGTH = 8
    
    def __init__(self, name: str, encryption_enabled: bool, 
                 access_key: str, max_size_gb: int):
        """
        Initialize StorageAccount.
        
        Args:
            name: Resource name
            encryption_enabled: Enable encryption at rest
            access_key: Secret authentication key
            max_size_gb: Maximum storage capacity
        
        Raises:
            InvalidConfigurationException: If configuration is invalid
        """
        # Set specific attributes
        self.__encryption_enabled = encryption_enabled
        self.__access_key = access_key
        self.__max_size_gb = max_size_gb
        
        # Validate configuration
        self.validate_config()
        
        # Call parent constructor
        super().__init__(name)
    
    def get_config(self) -> Dict[str, Any]:
        """
        Returns StorageAccount configuration.
        
        Note: Access key is masked for security
        
        Returns:
            Configuration dictionary
        """
        return {
            'encryption_enabled': self.__encryption_enabled,
            'access_key': self.__mask_key(self.__access_key),  # Masked for security
            'max_size_gb': self.__max_size_gb
        }
    
    def validate_config(self) -> bool:
        """
        Validates StorageAccount configuration.
        
        Returns:
            True if valid
        
        Raises:
            InvalidConfigurationException: If any validation fails
        """
        # Validate encryption_enabled is boolean
        if not isinstance(self.__encryption_enabled, bool):
            raise InvalidConfigurationException(
                "encryption_enabled must be True or False"
            )
        
        # Validate access_key
        if not self.__access_key or len(self.__access_key) < self.MIN_KEY_LENGTH:
            raise InvalidConfigurationException(
                f"access_key must be at least {self.MIN_KEY_LENGTH} characters"
            )
        
        # Validate max_size_gb
        if not isinstance(self.__max_size_gb, int):
            raise InvalidConfigurationException(
                "max_size_gb must be an integer"
            )
        
        if self.__max_size_gb < self.MIN_SIZE_GB or self.__max_size_gb > self.MAX_SIZE_GB:
            raise InvalidConfigurationException(
                f"max_size_gb must be between {self.MIN_SIZE_GB} and {self.MAX_SIZE_GB}"
            )
        
        return True
    
    def __mask_key(self, key: str) -> str:
        """
        Masks access key for security.
        
        Shows first 3 and last 3 characters only.
        
        Args:
            key: Full access key
        
        Returns:
            Masked key (e.g., "abc***xyz")
        """
        if len(key) <= 6:
            return "***"
        return f"{key[:3]}***{key[-3:]}"
    
    # Getters
    def get_encryption_enabled(self) -> bool:
        """Returns encryption status"""
        return self.__encryption_enabled
    
    def get_access_key(self) -> str:
        """Returns access key (use carefully - contains secret!)"""
        return self.__access_key
    
    def get_max_size_gb(self) -> int:
        """Returns maximum size"""
        return self.__max_size_gb


# Self-register with ResourceRegistry
from ..services.resource_registry import ResourceRegistry
__registered = ResourceRegistry.register('StorageAccount', StorageAccount)