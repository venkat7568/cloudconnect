#!/usr/bin/env python3
"""
CloudConnect - Comprehensive Test Script

Tests all components, design patterns, and workflows.
Run this BEFORE running the main application to ensure everything works!

Usage:
    python test_cloudconnect.py
"""

import sys
import os
from datetime import datetime

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestResult:
    """Tracks test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def pass_test(self, test_name):
        self.passed += 1
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} {test_name}")
    
    def fail_test(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"{Colors.FAIL}✗{Colors.ENDC} {test_name}")
        print(f"  {Colors.FAIL}Error: {error}{Colors.ENDC}")
    
    def print_summary(self):
        total = self.passed + self.failed
        print("\n" + "="*70)
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.ENDC}")
        print("="*70)
        print(f"Total Tests: {total}")
        print(f"{Colors.OKGREEN}Passed: {self.passed}{Colors.ENDC}")
        print(f"{Colors.FAIL}Failed: {self.failed}{Colors.ENDC}")
        
        if self.failed > 0:
            print(f"\n{Colors.FAIL}Failed Tests:{Colors.ENDC}")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        
        print("="*70)
        
        if self.failed == 0:
            print(f"{Colors.OKGREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.FAIL}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.ENDC}")
            return False


def print_header(text):
    """Prints a section header"""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{Colors.ENDC}")


def test_file_structure():
    """Test 1: Verify all files and directories exist"""
    print_header("TEST 1: File Structure")
    
    result = TestResult()
    
    required_structure = {
        'directories': [
            'src',
            'src/models',
            'src/states',
            'src/services',
            'src/utils',
            'src/exceptions',
            'logs'
        ],
        'files': [
            'main.py',
            'README.md',
            'requirements.txt',
            'src/__init__.py',
            'src/app.py',
            'src/models/__init__.py',
            'src/models/resource.py',
            'src/models/app_service.py',
            'src/models/storage_account.py',
            'src/models/cache_db.py',
            'src/states/__init__.py',
            'src/states/resource_state.py',
            'src/states/created_state.py',
            'src/states/started_state.py',
            'src/states/stopped_state.py',
            'src/states/deleted_state.py',
            'src/services/__init__.py',
            'src/services/resource_manager.py',
            'src/services/resource_factory.py',
            'src/services/resource_registry.py',
            'src/utils/__init__.py',
            'src/utils/logger.py',
            'src/exceptions/__init__.py',
            'src/exceptions/exceptions.py'
        ]
    }
    
    # Check directories
    for directory in required_structure['directories']:
        if os.path.isdir(directory):
            result.pass_test(f"Directory exists: {directory}")
        else:
            result.fail_test(f"Directory exists: {directory}", "Directory not found")
    
    # Check files
    for file_path in required_structure['files']:
        if os.path.isfile(file_path):
            result.pass_test(f"File exists: {file_path}")
        else:
            result.fail_test(f"File exists: {file_path}", "File not found")
    
    return result


def test_imports():
    """Test 2: Verify all imports work"""
    print_header("TEST 2: Module Imports")
    
    result = TestResult()
    
    imports_to_test = [
        ('src.exceptions.exceptions', ['CloudConnectException', 'InvalidStateTransitionException']),
        ('src.utils.logger', ['Logger']),
        ('src.states.resource_state', ['ResourceState']),
        ('src.states.created_state', ['CreatedState']),
        ('src.states.started_state', ['StartedState']),
        ('src.states.stopped_state', ['StoppedState']),
        ('src.states.deleted_state', ['DeletedState']),
        ('src.models.resource', ['Resource']),
        ('src.models.app_service', ['AppService']),
        ('src.models.storage_account', ['StorageAccount']),
        ('src.models.cache_db', ['CacheDB']),
        ('src.services.resource_registry', ['ResourceRegistry']),
        ('src.services.resource_factory', ['ResourceFactory']),
        ('src.services.resource_manager', ['ResourceManager']),
        ('src.app', ['CloudConnectApp'])
    ]
    
    for module_name, classes in imports_to_test:
        try:
            module = __import__(module_name, fromlist=classes)
            for class_name in classes:
                if hasattr(module, class_name):
                    result.pass_test(f"Import {module_name}.{class_name}")
                else:
                    result.fail_test(f"Import {module_name}.{class_name}", "Class not found in module")
        except ImportError as e:
            result.fail_test(f"Import {module_name}", str(e))
        except Exception as e:
            result.fail_test(f"Import {module_name}", str(e))
    
    return result


def test_exceptions():
    """Test 3: Verify exceptions work"""
    print_header("TEST 3: Custom Exceptions")
    
    result = TestResult()
    
    try:
        from src.exceptions.exceptions import (
            CloudConnectException,
            InvalidStateTransitionException,
            ResourceNotFoundException,
            InvalidConfigurationException
        )
        
        # Test CloudConnectException
        try:
            raise CloudConnectException("Test error")
        except CloudConnectException as e:
            if str(e) == "Test error":
                result.pass_test("CloudConnectException raised and caught")
            else:
                result.fail_test("CloudConnectException", "Message not preserved")
        
        # Test InvalidStateTransitionException
        try:
            raise InvalidStateTransitionException("Started", "delete", "Cannot delete running resource")
        except InvalidStateTransitionException as e:
            if "Started" in str(e) and "delete" in str(e):
                result.pass_test("InvalidStateTransitionException works")
            else:
                result.fail_test("InvalidStateTransitionException", "Details not preserved")
        
        # Test ResourceNotFoundException
        try:
            raise ResourceNotFoundException("test-resource")
        except ResourceNotFoundException as e:
            if "test-resource" in str(e):
                result.pass_test("ResourceNotFoundException works")
            else:
                result.fail_test("ResourceNotFoundException", "Resource name not in message")
        
        # Test InvalidConfigurationException
        try:
            raise InvalidConfigurationException("Invalid runtime")
        except InvalidConfigurationException as e:
            if "Invalid runtime" in str(e):
                result.pass_test("InvalidConfigurationException works")
            else:
                result.fail_test("InvalidConfigurationException", "Error message not preserved")
        
    except Exception as e:
        result.fail_test("Exception tests", str(e))
    
    return result


def test_logger():
    """Test 4: Verify Logger works"""
    print_header("TEST 4: Logger")
    
    result = TestResult()
    
    try:
        from src.utils.logger import Logger
        
        # Create logger
        logger = Logger("test_logs")
        result.pass_test("Logger instantiation")
        
        # Test timestamp
        timestamp = logger.get_timestamp()
        if timestamp and len(timestamp) > 0:
            result.pass_test("Logger get_timestamp()")
        else:
            result.fail_test("Logger get_timestamp()", "Empty timestamp")
        
        # Test logging
        logger.log("TestResource", "test operation", {"test": "value"})
        result.pass_test("Logger log() method")
        
        # Check if log file was created
        if os.path.exists("test_logs/testresource.log"):
            result.pass_test("Logger creates log file")
            
            # Clean up test logs
            os.remove("test_logs/testresource.log")
            os.rmdir("test_logs")
        else:
            result.fail_test("Logger creates log file", "File not created")
        
    except Exception as e:
        result.fail_test("Logger tests", str(e))
    
    return result


def test_resource_registry():
    """Test 5: Verify ResourceRegistry works"""
    print_header("TEST 5: ResourceRegistry")
    
    result = TestResult()
    
    try:
        from src.services.resource_registry import ResourceRegistry
        from src.models.app_service import AppService
        
        # Check if resources are registered
        types = ResourceRegistry.list_types()
        
        expected_types = ['AppService', 'StorageAccount', 'CacheDB']
        for expected_type in expected_types:
            if expected_type in types:
                result.pass_test(f"ResourceRegistry has {expected_type}")
            else:
                result.fail_test(f"ResourceRegistry has {expected_type}", "Type not registered")
        
        # Test get method
        try:
            app_class = ResourceRegistry.get('AppService')
            if app_class == AppService:
                result.pass_test("ResourceRegistry.get() returns correct class")
            else:
                result.fail_test("ResourceRegistry.get()", "Wrong class returned")
        except Exception as e:
            result.fail_test("ResourceRegistry.get()", str(e))
        
        # Test invalid type
        try:
            ResourceRegistry.get('NonExistentType')
            result.fail_test("ResourceRegistry invalid type", "Should raise KeyError")
        except KeyError:
            result.pass_test("ResourceRegistry raises KeyError for invalid type")
        
    except Exception as e:
        result.fail_test("ResourceRegistry tests", str(e))
    
    return result


def test_resource_factory():
    """Test 6: Verify ResourceFactory works"""
    print_header("TEST 6: ResourceFactory")
    
    result = TestResult()
    
    try:
        from src.services.resource_factory import ResourceFactory
        from src.models.app_service import AppService
        
        # Test creating AppService
        config = {
            'runtime': 'python',
            'region': 'WestEurope',
            'replica_count': 2
        }
        
        resource = ResourceFactory.create_resource('AppService', 'test-app', config)
        
        if isinstance(resource, AppService):
            result.pass_test("ResourceFactory creates AppService")
        else:
            result.fail_test("ResourceFactory creates AppService", "Wrong type returned")
        
        if resource.get_name() == 'test-app':
            result.pass_test("ResourceFactory sets resource name")
        else:
            result.fail_test("ResourceFactory sets resource name", "Name not set correctly")
        
        # Test available types
        types = ResourceFactory.get_available_types()
        if len(types) >= 3:
            result.pass_test("ResourceFactory.get_available_types()")
        else:
            result.fail_test("ResourceFactory.get_available_types()", "Not enough types returned")
        
    except Exception as e:
        result.fail_test("ResourceFactory tests", str(e))
    
    return result


def test_resource_classes():
    """Test 7: Verify all resource classes work"""
    print_header("TEST 7: Resource Classes")
    
    result = TestResult()
    
    try:
        from src.models.app_service import AppService
        from src.models.storage_account import StorageAccount
        from src.models.cache_db import CacheDB
        
        # Test AppService
        try:
            app = AppService('test-app', 'python', 'WestEurope', 2)
            result.pass_test("AppService instantiation")
            
            config = app.get_config()
            if config['runtime'] == 'python' and config['region'] == 'WestEurope':
                result.pass_test("AppService.get_config()")
            else:
                result.fail_test("AppService.get_config()", "Config incorrect")
            
        except Exception as e:
            result.fail_test("AppService", str(e))
        
        # Test StorageAccount
        try:
            storage = StorageAccount('test-storage', True, 'testkey123', 500)
            result.pass_test("StorageAccount instantiation")
            
            config = storage.get_config()
            if config['encryption_enabled'] and config['max_size_gb'] == 500:
                result.pass_test("StorageAccount.get_config()")
            else:
                result.fail_test("StorageAccount.get_config()", "Config incorrect")
            
        except Exception as e:
            result.fail_test("StorageAccount", str(e))
        
        # Test CacheDB
        try:
            cache = CacheDB('test-cache', 3600, 512, 'LRU')
            result.pass_test("CacheDB instantiation")
            
            config = cache.get_config()
            if config['ttl_seconds'] == 3600 and config['eviction_policy'] == 'LRU':
                result.pass_test("CacheDB.get_config()")
            else:
                result.fail_test("CacheDB.get_config()", "Config incorrect")
            
        except Exception as e:
            result.fail_test("CacheDB", str(e))
        
        # Test invalid configuration
        try:
            invalid_app = AppService('invalid', 'ruby', 'WestEurope', 2)
            result.fail_test("AppService validation", "Should reject invalid runtime")
        except Exception:
            result.pass_test("AppService rejects invalid configuration")
        
    except Exception as e:
        result.fail_test("Resource classes tests", str(e))
    
    return result


def test_states():
    """Test 8: Verify state pattern works"""
    print_header("TEST 8: State Pattern")
    
    result = TestResult()
    
    try:
        from src.models.app_service import AppService
        from src.states.created_state import CreatedState
        from src.states.started_state import StartedState
        from src.states.stopped_state import StoppedState
        from src.states.deleted_state import DeletedState
        from src.exceptions.exceptions import InvalidStateTransitionException
        
        # Create resource
        resource = AppService('state-test', 'python', 'WestEurope', 2)
        
        # Check initial state
        if isinstance(resource.get_state(), CreatedState):
            result.pass_test("Resource starts in CreatedState")
        else:
            result.fail_test("Resource starts in CreatedState", "Wrong initial state")
        
        # Test Created → Started
        try:
            resource.start()
            if isinstance(resource.get_state(), StartedState):
                result.pass_test("Transition: Created → Started")
            else:
                result.fail_test("Transition: Created → Started", "Wrong state after start")
        except Exception as e:
            result.fail_test("Transition: Created → Started", str(e))
        
        # Test Started → Started (should fail)
        try:
            resource.start()
            result.fail_test("Started → Started blocked", "Should raise exception")
        except InvalidStateTransitionException:
            result.pass_test("Started → Started blocked")
        
        # Test Started → Stopped
        try:
            resource.stop()
            if isinstance(resource.get_state(), StoppedState):
                result.pass_test("Transition: Started → Stopped")
            else:
                result.fail_test("Transition: Started → Stopped", "Wrong state after stop")
        except Exception as e:
            result.fail_test("Transition: Started → Stopped", str(e))
        
        # Test Stopped → Started (restart)
        try:
            resource.start()
            if isinstance(resource.get_state(), StartedState):
                result.pass_test("Transition: Stopped → Started (restart)")
            else:
                result.fail_test("Transition: Stopped → Started", "Wrong state after restart")
        except Exception as e:
            result.fail_test("Transition: Stopped → Started", str(e))
        
        # Test Started → Deleted (should fail - must stop first)
        try:
            resource.delete()
            result.fail_test("Started → Deleted blocked", "Should raise exception")
        except InvalidStateTransitionException:
            result.pass_test("Started → Deleted blocked (safety)")
        
        # Test Stopped → Deleted
        try:
            resource.stop()  # Stop first
            resource.delete()
            if isinstance(resource.get_state(), DeletedState):
                result.pass_test("Transition: Stopped → Deleted")
            else:
                result.fail_test("Transition: Stopped → Deleted", "Wrong state after delete")
        except Exception as e:
            result.fail_test("Transition: Stopped → Deleted", str(e))
        
        # Test Deleted → anything (all should fail)
        try:
            resource.start()
            result.fail_test("Deleted → Started blocked", "Should raise exception")
        except InvalidStateTransitionException:
            result.pass_test("Deleted → Started blocked (terminal state)")
        
        # Check is_deleted flag
        if resource.is_deleted():
            result.pass_test("is_deleted() flag set correctly")
        else:
            result.fail_test("is_deleted() flag", "Flag not set after deletion")
        
    except Exception as e:
        result.fail_test("State pattern tests", str(e))
    
    return result


def test_resource_manager():
    """Test 9: Verify ResourceManager works"""
    print_header("TEST 9: ResourceManager")
    
    result = TestResult()
    
    try:
        from src.services.resource_manager import ResourceManager
        from src.models.app_service import AppService
        from src.exceptions.exceptions import ResourceNotFoundException, ResourceAlreadyExistsException
        
        manager = ResourceManager()
        result.pass_test("ResourceManager instantiation")
        
        # Test adding resource
        resource = AppService('manager-test', 'python', 'WestEurope', 2)
        manager.add_resource(resource)
        result.pass_test("ResourceManager.add_resource()")
        
        # Test getting resource
        retrieved = manager.get_resource('manager-test')
        if retrieved == resource:
            result.pass_test("ResourceManager.get_resource()")
        else:
            result.fail_test("ResourceManager.get_resource()", "Wrong resource returned")
        
        # Test duplicate name
        try:
            duplicate = AppService('manager-test', 'nodejs', 'EastUS', 1)
            manager.add_resource(duplicate)
            result.fail_test("ResourceManager duplicate prevention", "Should raise exception")
        except ResourceAlreadyExistsException:
            result.pass_test("ResourceManager prevents duplicates")
        
        # Test get non-existent
        try:
            manager.get_resource('does-not-exist')
            result.fail_test("ResourceManager non-existent resource", "Should raise exception")
        except ResourceNotFoundException:
            result.pass_test("ResourceManager raises exception for non-existent")
        
        # Test list resources
        resources = manager.list_resources()
        if len(resources) == 1:
            result.pass_test("ResourceManager.list_resources()")
        else:
            result.fail_test("ResourceManager.list_resources()", f"Expected 1, got {len(resources)}")
        
        # Test resource_exists
        if manager.resource_exists('manager-test'):
            result.pass_test("ResourceManager.resource_exists() - True")
        else:
            result.fail_test("ResourceManager.resource_exists() - True", "Should return True")
        
        if not manager.resource_exists('non-existent'):
            result.pass_test("ResourceManager.resource_exists() - False")
        else:
            result.fail_test("ResourceManager.resource_exists() - False", "Should return False")
        
        # Test count
        count = manager.count()
        if count == 1:
            result.pass_test("ResourceManager.count()")
        else:
            result.fail_test("ResourceManager.count()", f"Expected 1, got {count}")
        
        # Test remove
        manager.remove_resource('manager-test')
        if manager.count() == 0:
            result.pass_test("ResourceManager.remove_resource()")
        else:
            result.fail_test("ResourceManager.remove_resource()", "Resource not removed")
        
    except Exception as e:
        result.fail_test("ResourceManager tests", str(e))
    
    return result


def test_full_lifecycle():
    """Test 10: Complete resource lifecycle"""
    print_header("TEST 10: Complete Resource Lifecycle")
    
    result = TestResult()
    
    try:
        from src.services.resource_factory import ResourceFactory
        from src.services.resource_manager import ResourceManager
        
        manager = ResourceManager()
        
        # Create AppService
        config = {'runtime': 'python', 'region': 'WestEurope', 'replica_count': 2}
        resource = ResourceFactory.create_resource('AppService', 'lifecycle-test', config)
        manager.add_resource(resource)
        result.pass_test("Lifecycle: Create resource")
        
        # Start
        resource.start()
        if resource.get_state().get_state_name() == "Started":
            result.pass_test("Lifecycle: Start resource")
        else:
            result.fail_test("Lifecycle: Start resource", "Wrong state")
        
        # Stop
        resource.stop()
        if resource.get_state().get_state_name() == "Stopped":
            result.pass_test("Lifecycle: Stop resource")
        else:
            result.fail_test("Lifecycle: Stop resource", "Wrong state")
        
        # Restart
        resource.start()
        if resource.get_state().get_state_name() == "Started":
            result.pass_test("Lifecycle: Restart resource")
        else:
            result.fail_test("Lifecycle: Restart resource", "Wrong state")
        
        # Stop before delete
        resource.stop()
        
        # Delete
        resource.delete()
        if resource.get_state().get_state_name() == "Deleted":
            result.pass_test("Lifecycle: Delete resource")
        else:
            result.fail_test("Lifecycle: Delete resource", "Wrong state")
        
        # Verify it's in manager with deleted flag
        retrieved = manager.get_resource('lifecycle-test')
        if retrieved.is_deleted():
            result.pass_test("Lifecycle: Soft deletion preserves metadata")
        else:
            result.fail_test("Lifecycle: Soft deletion", "Deleted flag not set")
        
    except Exception as e:
        result.fail_test("Full lifecycle tests", str(e))
    
    return result


def test_all_resource_types():
    """Test 11: All three resource types"""
    print_header("TEST 11: All Resource Types")
    
    result = TestResult()
    
    try:
        from src.services.resource_factory import ResourceFactory
        from src.services.resource_manager import ResourceManager
        
        manager = ResourceManager()
        
        # Create AppService
        app_config = {'runtime': 'python', 'region': 'WestEurope', 'replica_count': 2}
        app = ResourceFactory.create_resource('AppService', 'test-app', app_config)
        manager.add_resource(app)
        app.start()
        result.pass_test("AppService complete workflow")
        
        # Create StorageAccount
        storage_config = {'encryption_enabled': True, 'access_key': 'secretkey123', 'max_size_gb': 500}
        storage = ResourceFactory.create_resource('StorageAccount', 'test-storage', storage_config)
        manager.add_resource(storage)
        storage.start()
        result.pass_test("StorageAccount complete workflow")
        
        # Create CacheDB
        cache_config = {'ttl_seconds': 3600, 'capacity_mb': 512, 'eviction_policy': 'LRU'}
        cache = ResourceFactory.create_resource('CacheDB', 'test-cache', cache_config)
        manager.add_resource(cache)
        cache.start()
        result.pass_test("CacheDB complete workflow")
        
        # Verify all in manager
        resources = manager.list_resources()
        if len(resources) == 3:
            result.pass_test("All three resource types in manager")
        else:
            result.fail_test("All three resource types", f"Expected 3, got {len(resources)}")
        
        # Verify different types
        types = set([r.__class__.__name__ for r in resources])
        expected_types = {'AppService', 'StorageAccount', 'CacheDB'}
        if types == expected_types:
            result.pass_test("All resource types are different classes")
        else:
            result.fail_test("Resource type diversity", f"Expected {expected_types}, got {types}")
        
    except Exception as e:
        result.fail_test("All resource types test", str(e))
    
    return result


def test_validation():
    """Test 12: Configuration validation"""
    print_header("TEST 12: Configuration Validation")
    
    result = TestResult()
    
    try:
        from src.models.app_service import AppService
        from src.models.storage_account import StorageAccount
        from src.models.cache_db import CacheDB
        from src.exceptions.exceptions import InvalidConfigurationException
        
        # Test invalid AppService configurations
        invalid_configs = [
            ('ruby', 'WestEurope', 2, "Invalid runtime"),
            ('python', 'Mars', 2, "Invalid region"),
            ('python', 'WestEurope', 10, "Invalid replica count")
        ]
        
        for runtime, region, replicas, desc in invalid_configs:
            try:
                AppService('test', runtime, region, replicas)
                result.fail_test(f"AppService validation: {desc}", "Should raise exception")
            except InvalidConfigurationException:
                result.pass_test(f"AppService rejects: {desc}")
        
        # Test invalid StorageAccount configurations
        try:
            StorageAccount('test', True, 'short', 500)  # Key too short
            result.fail_test("StorageAccount: short key", "Should raise exception")
        except InvalidConfigurationException:
            result.pass_test("StorageAccount rejects: short access key")
        
        try:
            StorageAccount('test', True, 'longkey123', 0)  # Invalid size
            result.fail_test("StorageAccount: invalid size", "Should raise exception")
        except InvalidConfigurationException:
            result.pass_test("StorageAccount rejects: invalid size")
        
        # Test invalid CacheDB configurations
        try:
            CacheDB('test', 10, 512, 'LRU')  # TTL too short
            result.fail_test("CacheDB: invalid TTL", "Should raise exception")
        except InvalidConfigurationException:
            result.pass_test("CacheDB rejects: invalid TTL")
        
        try:
            CacheDB('test', 3600, 50, 'LRU')  # Capacity too small
            result.fail_test("CacheDB: invalid capacity", "Should raise exception")
        except InvalidConfigurationException:
            result.pass_test("CacheDB rejects: invalid capacity")
        
        try:
            CacheDB('test', 3600, 512, 'INVALID')  # Invalid policy
            result.fail_test("CacheDB: invalid policy", "Should raise exception")
        except InvalidConfigurationException:
            result.pass_test("CacheDB rejects: invalid eviction policy")
        
    except Exception as e:
        result.fail_test("Validation tests", str(e))
    
    return result


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("="*70)
    print("🧪 CLOUDCONNECT - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"{Colors.ENDC}")
    print(f"Testing all components, patterns, and workflows...")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Collect all results
    all_results = []
    
    # Run all tests
    all_results.append(test_file_structure())
    all_results.append(test_imports())
    all_results.append(test_exceptions())
    all_results.append(test_logger())
    all_results.append(test_resource_registry())
    all_results.append(test_resource_factory())
    all_results.append(test_resource_classes())
    all_results.append(test_states())
    all_results.append(test_resource_manager())
    all_results.append(test_full_lifecycle())
    all_results.append(test_all_resource_types())
    all_results.append(test_validation())
    
    # Calculate total results
    total_result = TestResult()
    for r in all_results:
        total_result.passed += r.passed
        total_result.failed += r.failed
        total_result.errors.extend(r.errors)
    
    # Print final summary
    print(f"\n{Colors.BOLD}Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    total_result.print_summary()
    
    # Return exit code
    if total_result.failed == 0:
        print(f"\n{Colors.OKGREEN}✓ All systems operational - ready to run main application!{Colors.ENDC}")
        return 0
    else:
        print(f"\n{Colors.FAIL}✗ Please fix the issues above before running main application{Colors.ENDC}")
        return 1


if __name__ == '__main__':
    sys.exit(main())