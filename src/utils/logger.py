"""
Logger - Records operations to console and file

SOLID Principles:
- SRP: Only handles logging (not business logic)
- OCP: Can extend with new output methods
"""

import os
from datetime import datetime
from typing import Dict, Any


class Logger:
    """
    Handles dual output logging (console + file).
    
    Design Pattern: Observer-like pattern
    - Observes operations and logs them
    - Multiple outputs without coupling
    """
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize logger.
        
        Args:
            log_dir: Directory for log files
        """
        self.__log_dir = log_dir
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log(self, resource_type: str, message: str, config: Dict[str, Any] = None) -> None:
        """
        Records an operation with dual output.
        
        Args:
            resource_type: Type of resource (AppService, StorageAccount, etc.)
            message: What happened (created, started, stopped, etc.)
            config: Resource configuration for context
        """
        # Get timestamp
        timestamp = self.get_timestamp()
        
        # Format message
        formatted_message = self.__format_message(timestamp, resource_type, message, config)
        
        # Write to console
        self.__write_to_console(formatted_message)
        
        # Write to file
        filename = f"{self.__log_dir}/{resource_type.lower()}.log"
        self.__write_to_file(filename, formatted_message)
    
    def view_logs(self, resource_type: str = None, lines: int = None) -> None:
        """
        Displays logs for a resource type.
        
        Args:
            resource_type: Type to show logs for (None = all)
            lines: Number of recent lines (None = all)
        """
        if resource_type:
            filename = f"{self.__log_dir}/{resource_type.lower()}.log"
            self.__display_file(filename, lines)
        else:
            # Show all log files
            for filename in os.listdir(self.__log_dir):
                if filename.endswith('.log'):
                    print(f"\n=== {filename} ===")
                    self.__display_file(f"{self.__log_dir}/{filename}", lines)
    
    def get_timestamp(self) -> str:
        """
        Returns current timestamp formatted.
        
        Returns:
            Formatted time string (e.g., "10:42 AM")
        """
        return datetime.now().strftime("%I:%M %p")
    
    def __format_message(self, timestamp: str, resource_type: str, 
                        message: str, config: Dict[str, Any]) -> str:
        """
        Formats log message with timestamp and details.
        
        Args:
            timestamp: Time string
            resource_type: Resource type
            message: Operation description
            config: Configuration details
        
        Returns:
            Formatted log entry
        """
        # Build config string
        config_parts = []
        if config:
            if 'region' in config:
                config_parts.append(f"region={config['region']}")
            if 'runtime' in config:
                config_parts.append(f"runtime={config['runtime']}")
            if 'replica_count' in config:
                config_parts.append(f"replicas={config['replica_count']}")
        
        config_str = f" ({', '.join(config_parts)})" if config_parts else ""
        
        return f"[{timestamp}] {resource_type}: {message}{config_str}"
    
    def __write_to_console(self, message: str) -> None:
        """
        Writes message to console (stdout).
        
        Args:
            message: Formatted message
        """
        print(message)
    
    def __write_to_file(self, filename: str, message: str) -> None:
        """
        Appends message to log file.
        
        Args:
            filename: Full path to log file
            message: Formatted message
        """
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    
    def __display_file(self, filename: str, lines: int = None) -> None:
        """
        Displays contents of a log file.
        
        Args:
            filename: Path to log file
            lines: Number of recent lines to show
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.readlines()
                
                if lines:
                    content = content[-lines:]  # Last N lines
                
                for line in content:
                    print(line.rstrip())
        except FileNotFoundError:
            print(f"No logs found: {filename}")