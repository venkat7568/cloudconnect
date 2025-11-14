"""
CloudConnectApp - Main CLI Application

SOLID Principles:
- SRP: Only handles user interface
- DIP: Depends on abstractions (Manager, Factory, Logger)
"""

import sys
from typing import Optional
from .services.resource_manager import ResourceManager
from .services.resource_factory import ResourceFactory
from .utils.logger import Logger
from .exceptions import (
    CloudConnectException,
    ResourceNotFoundException,
    InvalidStateTransitionException,
    InvalidConfigurationException
)


class CloudConnectApp:
    """
    Command-line interface for CloudConnect.
    
    Responsibilities:
    - Display menus
    - Get user input
    - Coordinate between services
    - Display results
    
    Does NOT:
    - Create resources (delegates to Factory)
    - Store resources (delegates to Manager)
    - Log operations (delegates to Logger)
    """
    
    def __init__(self):
        """Initialize application components"""
        self.__manager = ResourceManager()
        self.__logger = Logger()
    
    def run(self) -> None:
        """
        Main application loop.
        
        Displays menu and processes user choices until exit.
        """
        print("\n" + "="*60)
        print("🌩️  CLOUDCONNECT - Cloud Resource Management System")
        print("="*60)
        
        while True:
            try:
                self.__print_menu()
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '1':
                    self.__create_resource()
                elif choice == '2':
                    self.__start_resource()
                elif choice == '3':
                    self.__stop_resource()
                elif choice == '4':
                    self.__delete_resource()
                elif choice == '5':
                    self.__list_resources()
                elif choice == '6':
                    self.__view_logs()
                elif choice == '7':
                    self.__show_resource_details()
                elif choice == '8':
                    print("\n👋 Thank you for using CloudConnect!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                
                input("\n[Press Enter to continue...]")
                
            except KeyboardInterrupt:
                print("\n\n👋 Exiting CloudConnect...")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("\n[Press Enter to continue...]")
    
    def __print_menu(self) -> None:
        """Displays main menu"""
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Create Resource")
        print("2. Start Resource")
        print("3. Stop Resource")
        print("4. Delete Resource")
        print("5. List All Resources")
        print("6. View Logs")
        print("7. Show Resource Details")
        print("8. Exit")
        print("="*60)
    
    def __create_resource(self) -> None:
        """Handles resource creation workflow"""
        print("\n" + "="*60)
        print("CREATE RESOURCE")
        print("="*60)
        
        try:
            # Step 1: Select resource type
            available_types = ResourceFactory.get_available_types()
            print("\nAvailable resource types:")
            for idx, resource_type in enumerate(available_types, 1):
                print(f"{idx}. {resource_type}")
            
            type_choice = input("\nSelect resource type (number): ").strip()
            
            try:
                type_idx = int(type_choice) - 1
                if type_idx < 0 or type_idx >= len(available_types):
                    print("❌ Invalid selection")
                    return
                resource_type = available_types[type_idx]
            except ValueError:
                print("❌ Please enter a valid number")
                return
            
            # Step 2: Get resource name
            name = input("\nEnter resource name: ").strip()
            if not name:
                print("❌ Resource name cannot be empty")
                return
            
            # Check if already exists
            if self.__manager.resource_exists(name):
                print(f"❌ Resource '{name}' already exists")
                return
            
            # Step 3: Get configuration based on type
            config = self.__get_resource_config(resource_type)
            if config is None:
                return  # User cancelled or error
            
            # Step 4: Create resource using Factory
            resource = ResourceFactory.create_resource(resource_type, name, config)
            
            # Step 5: Add to manager
            self.__manager.add_resource(resource)
            
            # Step 6: Show success
            print(f"\n✅ {resource_type} '{name}' created successfully!")
            print(f"📍 Current state: {resource.get_state().get_state_name()}")
            
        except InvalidConfigurationException as e:
            print(f"\n❌ Configuration error: {e.message}")
        except CloudConnectException as e:
            print(f"\n❌ {e.message}")
    
    def __get_resource_config(self, resource_type: str) -> Optional[dict]:
        """
        Gets configuration for specific resource type.
        
        Args:
            resource_type: Type of resource
        
        Returns:
            Configuration dictionary or None if error
        """
        try:
            if resource_type == 'AppService':
                return self.__get_appservice_config()
            elif resource_type == 'StorageAccount':
                return self.__get_storage_config()
            elif resource_type == 'CacheDB':
                return self.__get_cache_config()
            else:
                print(f"❌ Unknown resource type: {resource_type}")
                return None
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            return None
    
    def __get_appservice_config(self) -> dict:
        """Gets AppService configuration from user"""
        print("\n--- AppService Configuration ---")
        
        # Runtime
        print("\nAvailable runtimes: python, nodejs, dotnet")
        runtime = input("Select runtime: ").strip().lower()
        
        # Region
        print("\nAvailable regions: EastUS, WestEurope, CentralIndia")
        region = input("Select region: ").strip()
        
        # Replica count
        print("\nReplica count options: 1, 2, 3")
        replica_count = int(input("Select replica count: ").strip())
        
        return {
            'runtime': runtime,
            'region': region,
            'replica_count': replica_count
        }
    
    def __get_storage_config(self) -> dict:
        """Gets StorageAccount configuration from user"""
        print("\n--- StorageAccount Configuration ---")
        
        # Encryption
        encryption_input = input("\nEnable encryption? (yes/no): ").strip().lower()
        encryption_enabled = encryption_input in ['yes', 'y', 'true']
        
        # Access key
        access_key = input("Enter access key (min 8 characters): ").strip()
        
        # Max size
        max_size_gb = int(input("Enter max storage size (GB, 1-10000): ").strip())
        
        return {
            'encryption_enabled': encryption_enabled,
            'access_key': access_key,
            'max_size_gb': max_size_gb
        }
    
    def __get_cache_config(self) -> dict:
        """Gets CacheDB configuration from user"""
        print("\n--- CacheDB Configuration ---")
        
        # TTL
        print("\nTTL (Time To Live) in seconds")
        print("Range: 60 (1 minute) to 86400 (24 hours)")
        ttl_seconds = int(input("Enter TTL: ").strip())
        
        # Capacity
        print("\nCapacity in MB")
        print("Range: 128 MB to 16384 MB (16 GB)")
        capacity_mb = int(input("Enter capacity: ").strip())
        
        # Eviction policy
        print("\nEviction policies:")
        print("  LRU  - Least Recently Used")
        print("  FIFO - First In First Out")
        print("  LFU  - Least Frequently Used")
        eviction_policy = input("Select policy: ").strip().upper()
        
        return {
            'ttl_seconds': ttl_seconds,
            'capacity_mb': capacity_mb,
            'eviction_policy': eviction_policy
        }
    
    def __start_resource(self) -> None:
        """Handles starting a resource"""
        print("\n" + "="*60)
        print("START RESOURCE")
        print("="*60)
        
        try:
            # Show available resources
            resources = self.__manager.get_resource_names()
            if not resources:
                print("\n⚠️  No resources available. Create a resource first.")
                return
            
            print("\nAvailable resources:")
            for name in resources:
                resource = self.__manager.get_resource(name)
                state = resource.get_state().get_state_name()
                print(f"  - {name} ({state})")
            
            # Get resource name
            name = input("\nEnter resource name to start: ").strip()
            
            # Get resource
            resource = self.__manager.get_resource(name)
            
            # Start it
            resource.start()
            
            print(f"\n✅ Resource '{name}' started successfully!")
            print(f"📍 Current state: {resource.get_state().get_state_name()}")
            
        except ResourceNotFoundException as e:
            print(f"\n❌ {e.message}")
        except InvalidStateTransitionException as e:
            print(f"\n❌ {e.message}")
        except CloudConnectException as e:
            print(f"\n❌ {e.message}")
    
    def __stop_resource(self) -> None:
        """Handles stopping a resource"""
        print("\n" + "="*60)
        print("STOP RESOURCE")
        print("="*60)
        
        try:
            # Show available resources
            resources = self.__manager.get_resource_names()
            if not resources:
                print("\n⚠️  No resources available.")
                return
            
            print("\nAvailable resources:")
            for name in resources:
                resource = self.__manager.get_resource(name)
                state = resource.get_state().get_state_name()
                print(f"  - {name} ({state})")
            
            # Get resource name
            name = input("\nEnter resource name to stop: ").strip()
            
            # Get resource
            resource = self.__manager.get_resource(name)
            
            # Stop it
            resource.stop()
            
            print(f"\n✅ Resource '{name}' stopped successfully!")
            print(f"📍 Current state: {resource.get_state().get_state_name()}")
            
        except ResourceNotFoundException as e:
            print(f"\n❌ {e.message}")
        except InvalidStateTransitionException as e:
            print(f"\n❌ {e.message}")
        except CloudConnectException as e:
            print(f"\n❌ {e.message}")
    
    def __delete_resource(self) -> None:
        """Handles deleting a resource (soft delete)"""
        print("\n" + "="*60)
        print("DELETE RESOURCE")
        print("="*60)
        
        try:
            # Show available resources
            resources = self.__manager.get_resource_names()
            if not resources:
                print("\n⚠️  No resources available.")
                return
            
            print("\nAvailable resources:")
            for name in resources:
                resource = self.__manager.get_resource(name)
                state = resource.get_state().get_state_name()
                print(f"  - {name} ({state})")
            
            # Get resource name
            name = input("\nEnter resource name to delete: ").strip()
            
            # Get resource
            resource = self.__manager.get_resource(name)
            
            # Confirm deletion
            confirm = input(f"\n⚠️  Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Deletion cancelled.")
                return
            
            # Delete it (soft delete)
            resource.delete()
            
            print(f"\n✅ Resource '{name}' deleted successfully!")
            print("📝 Note: This is a soft deletion. Metadata is preserved for audit trail.")
            print(f"📍 Current state: {resource.get_state().get_state_name()}")
            
        except ResourceNotFoundException as e:
            print(f"\n❌ {e.message}")
        except InvalidStateTransitionException as e:
            print(f"\n❌ {e.message}")
        except CloudConnectException as e:
            print(f"\n❌ {e.message}")
    
    def __list_resources(self) -> None:
        """Lists all resources"""
        print("\n" + "="*60)
        print("ALL RESOURCES")
        print("="*60)
        
        try:
            resources = self.__manager.list_resources(include_deleted=True)
            
            if not resources:
                print("\n⚠️  No resources found. Create a resource first.")
                return
            
            print(f"\nTotal resources: {len(resources)}")
            print("\n" + "-"*60)
            
            for resource in resources:
                name = resource.get_name()
                resource_type = resource.__class__.__name__
                state = resource.get_state().get_state_name()
                deleted = "🗑️  DELETED" if resource.is_deleted() else ""
                
                print(f"\n📦 {name}")
                print(f"   Type: {resource_type}")
                print(f"   State: {state} {deleted}")
                print(f"   Created: {resource.get_created_at().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Show configuration
                config = resource.get_config()
                print(f"   Config: {config}")
            
            print("\n" + "-"*60)
            
        except CloudConnectException as e:
            print(f"\n❌ {e.message}")
    
    def __view_logs(self) -> None:
        """Displays operation logs"""
        print("\n" + "="*60)
        print("VIEW LOGS")
        print("="*60)
        
        print("\nOptions:")
        print("1. View all logs")
        print("2. View logs for specific resource type")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            self.__logger.view_logs()
        elif choice == '2':
            types = ResourceFactory.get_available_types()
            print("\nAvailable types:")
            for idx, resource_type in enumerate(types, 1):
                print(f"{idx}. {resource_type}")
            
            type_choice = input("\nSelect type (number): ").strip()
            try:
                type_idx = int(type_choice) - 1
                if 0 <= type_idx < len(types):
                    self.__logger.view_logs(types[type_idx])
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Please enter a valid number")
        else:
            print("❌ Invalid choice")
    
    def __show_resource_details(self) -> None:
        """Shows detailed information about a resource"""
        print("\n" + "="*60)
        print("RESOURCE DETAILS")
        print("="*60)
        
        try:
            resources = self.__manager.get_resource_names(include_deleted=True)
            if not resources:
                print("\n⚠️  No resources available.")
                return
            
            print("\nAvailable resources:")
            for name in resources:
                print(f"  - {name}")
            
            name = input("\nEnter resource name: ").strip()
            
            resource = self.__manager.get_resource(name)
            
            print("\n" + "="*60)
            print(f"📦 {resource.get_name()}")
            print("="*60)
            print(f"Type: {resource.__class__.__name__}")
            print(f"State: {resource.get_state().get_state_name()}")
            print(f"Created: {resource.get_created_at().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Deleted: {'Yes' if resource.is_deleted() else 'No'}")
            print("\nConfiguration:")
            config = resource.get_config()
            for key, value in config.items():
                print(f"  {key}: {value}")
            print("="*60)
            
        except ResourceNotFoundException as e:
            print(f"\n❌ {e.message}")
        except CloudConnectException as e:
            print(f"\n❌ {e.message}")