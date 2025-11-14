# CloudConnect - Cloud Resource Management System

Simple CLI application for managing cloud resources with State, Factory, and Registry patterns.

---

## Quick Start

```bash
cd cloudconnect
python main.py
```

---

## Requirements

- Python 3.8 or higher
- No external dependencies (uses only Python standard library)

---

## Run Tests

```bash
python test_cloudconnect.py
```

Expected output:

```
Total Tests: 108
Passed: 108
Failed: 0
🎉 ALL TESTS PASSED!
```

---

## Resource Types

### 1. AppService

- **Runtime:** python, nodejs, dotnet
- **Region:** EastUS, WestEurope, CentralIndia
- **Replicas:** 1, 2, 3

### 2. StorageAccount

- **Encryption:** yes, no
- **Access Key:** 8+ characters
- **Size:** 1-10000 GB

### 3. CacheDB

- **TTL:** 60-86400 seconds
- **Capacity:** 128-16384 MB
- **Eviction:** LRU, FIFO, LFU

---

## Test Scenario 1: AppService

```bash
python main.py
```

**Create:**

```
Choice: 1
Type: 1
Name: my-app
Runtime: python
Region: WestEurope
Replicas: 2
```

✅ AppService created

**Start:**

```
Choice: 2
Name: my-app
```

✅ Resource started

**Stop:**

```
Choice: 3
Name: my-app
```

✅ Resource stopped

**Delete:**

```
Choice: 4
Name: my-app
Confirm: yes
```

✅ Resource deleted

---

## Test Scenario 2: StorageAccount

**Create:**

```
Choice: 1
Type: 2
Name: my-storage
Encryption: yes
Access Key: myKey12345
Size: 500
```

✅ StorageAccount created

**Start:**

```
Choice: 2
Name: my-storage
```

✅ Resource started

---

## Test Scenario 3: CacheDB

**Create:**

```
Choice: 1
Type: 3
Name: my-cache
TTL: 3600
Capacity: 512
Eviction: LRU
```

✅ CacheDB created

**Start:**

```
Choice: 2
Name: my-cache
```

✅ Resource started

---

## View Logs

```
Choice: 6
Option: 1
```

Logs saved in:

- `logs/appservice.log`
- `logs/storageaccount.log`
- `logs/cachedb.log`

---

## Valid State Transitions

```
Created → Started (start)
Started → Stopped (stop)
Stopped → Started (restart)
Stopped → Deleted (delete)
Created → Deleted (delete unused)
```

---

## Invalid Transitions (Will Show Error)

```
Created → Stopped ❌ (not started yet)
Started → Started ❌ (already running)
Started → Deleted ❌ (must stop first)
Stopped → Stopped ❌ (already stopped)
Deleted → anything ❌ (terminal state)
```

---

## Testing Invalid Operations

### Invalid Configuration

```
Create AppService
Runtime: ruby
```

Expected: ❌ `Invalid runtime 'ruby'`

### Invalid State Transition

```
Create resource → Stop without starting
```

Expected: ❌ `Cannot stop: Resource not started yet`

### Delete Running Resource

```
Start resource → Delete without stopping
```

Expected: ❌ `Cannot delete: Must stop resource first`

### Duplicate Name

```
Create resource "test"
Create another resource "test"
```

Expected: ❌ `Resource 'test' already exists`

### Non-existent Resource

```
Start "does-not-exist"
```

Expected: ❌ `Resource 'does-not-exist' not found`

---

## Complete Test Run (5 Minutes)

```bash
python main.py

# Inputs:
1           # Create
1           # AppService
webapp1     # Name
python      # Runtime
WestEurope  # Region
2           # Replicas
[Enter]

2           # Start
webapp1     # Name
[Enter]

5           # List All
[Enter]

6           # View Logs
1           # All logs
[Enter]

3           # Stop
webapp1     # Name
[Enter]

4           # Delete
webapp1     # Name
yes         # Confirm
[Enter]

8           # Exit
```

---

## Menu Options

```
1. Create Resource
2. Start Resource
3. Stop Resource
4. Delete Resource
5. List All Resources
6. View Logs
7. Show Resource Details
8. Exit
```

---

## Common Input Mistakes

| Wrong         | Right              |
| ------------- | ------------------ |
| Runtime: 1    | Runtime: python    |
| Region: 2     | Region: WestEurope |
| Encryption: 1 | Encryption: yes    |
| Eviction: 1   | Eviction: LRU      |

**Remember:** Type words, not numbers (except replica count, TTL, capacity, size)

---

## File Structure

```
cloudconnect/
├── src/
│   ├── models/              # Resource classes
│   ├── states/              # State pattern
│   ├── services/            # Factory, Registry, Manager
│   ├── utils/               # Logger
│   ├── exceptions/          # Custom exceptions
│   └── app.py               # Main CLI
├── logs/                    # Auto-generated
├── main.py                  # Entry point
├── test_cloudconnect.py     # Test suite
└── README.md                # This file
```

---

## Design Patterns

1. **State Pattern** - Resource lifecycle management
2. **Factory Pattern** - Dynamic resource creation
3. **Registry Pattern** - Self-registration
4. **Template Method Pattern** - Common resource behavior

---

## SOLID Principles

- **S** - Single Responsibility: Each class has one job
- **O** - Open/Closed: Add new resources without modifying code
- **L** - Liskov Substitution: All resources interchangeable
- **I** - Interface Segregation: Focused interfaces
- **D** - Dependency Inversion: Depends on abstractions

---

## Testing Checklist

- [ ] Create AppService
- [ ] Create StorageAccount
- [ ] Create CacheDB
- [ ] Start resource
- [ ] Stop resource
- [ ] Restart resource
- [ ] Delete resource
- [ ] List all resources
- [ ] View logs
- [ ] Try invalid runtime (should fail)
- [ ] Try to stop non-started resource (should fail)
- [ ] Try to delete running resource (should fail)
- [ ] Try duplicate name (should fail)

---

## Troubleshooting

**Module not found:**

```bash
cd cloudconnect
python main.py
```

**Tests fail:**

```bash
python test_cloudconnect.py
```

**No logs showing:**

```bash
mkdir logs
```

**Can't delete resource:**
Stop it first, then delete

---

## Example Session

```
$ python main.py

Enter your choice: 1
Select resource type: 1
Enter resource name: webapp
Select runtime: python
Select region: EastUS
Select replica count: 2
✅ AppService 'webapp' created successfully!

Enter your choice: 2
Enter resource name: webapp
✅ Resource 'webapp' started successfully!

Enter your choice: 5
📦 webapp
   Type: AppService
   State: Started

Enter your choice: 8
👋 Thank you for using CloudConnect!
```

---
