# TaskFlow API - Usage Examples

This document provides practical examples of how to use the TaskFlow API endpoints.

## Base URL

```
http://localhost:8000
```

## Categories

### 1. Get All Categories

**Request:**
```http
GET /api/categories
```

**Response (200 OK):**
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Work",
      "color": "#3B82F6"
    },
    {
      "id": 2,
      "name": "Personal",
      "color": "#10B981"
    }
  ],
  "total": 2
}
```

### 2. Create a Category

**Request:**
```http
POST /api/categories
Content-Type: application/json

{
  "name": "Work",
  "color": "#3B82F6"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Work",
  "color": "#3B82F6"
}
```

**Error Response - Duplicate Name (409 Conflict):**
```json
{
  "message": "Category with name 'Work' already exists",
  "status_code": 409,
  "details": {}
}
```

### 3. Get a Specific Category

**Request:**
```http
GET /api/categories/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Work",
  "color": "#3B82F6"
}
```

**Error Response - Not Found (404):**
```json
{
  "message": "Category with id '999' not found",
  "status_code": 404,
  "details": {}
}
```

## Tasks

### 1. Get All Tasks

**Request:**
```http
GET /api/tasks
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project proposal",
      "description": "Write and submit the Q1 project proposal",
      "status": "in_progress",
      "priority": "high",
      "category_id": 1,
      "category": {
        "id": 1,
        "name": "Work",
        "color": "#3B82F6"
      },
      "due_date": "2025-10-30T17:00:00",
      "created_at": "2025-10-22T10:00:00",
      "updated_at": "2025-10-22T14:30:00"
    }
  ],
  "total": 1
}
```

### 2. Get Tasks with Filters

**Filter by Status:**
```http
GET /api/tasks?status=completed
```

**Filter by Priority:**
```http
GET /api/tasks?priority=high
```

**Filter by Category:**
```http
GET /api/tasks?category_id=1
```

**Multiple Filters:**
```http
GET /api/tasks?status=in_progress&priority=high&category_id=1
```

### 3. Create a Task

**Request - Full Task:**
```http
POST /api/tasks
Content-Type: application/json

{
  "title": "Complete project proposal",
  "description": "Write and submit the Q1 project proposal",
  "status": "todo",
  "priority": "high",
  "category_id": 1,
  "due_date": "2025-10-30T17:00:00"
}
```

**Request - Minimal Task (only required field):**
```http
POST /api/tasks
Content-Type: application/json

{
  "title": "Quick task"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the Q1 project proposal",
  "status": "todo",
  "priority": "high",
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Work",
    "color": "#3B82F6"
  },
  "due_date": "2025-10-30T17:00:00",
  "created_at": "2025-10-22T10:00:00",
  "updated_at": "2025-10-22T10:00:00"
}
```

**Error Response - Invalid Category (404):**
```json
{
  "message": "Category with id '999' not found",
  "status_code": 404,
  "details": {}
}
```

### 4. Get a Specific Task

**Request:**
```http
GET /api/tasks/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the Q1 project proposal",
  "status": "in_progress",
  "priority": "high",
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Work",
    "color": "#3B82F6"
  },
  "due_date": "2025-10-30T17:00:00",
  "created_at": "2025-10-22T10:00:00",
  "updated_at": "2025-10-22T14:30:00"
}
```

### 5. Update a Task

**Request - Full Update:**
```http
PUT /api/tasks/1
Content-Type: application/json

{
  "title": "Complete project proposal (Updated)",
  "description": "Write, review, and submit the Q1 project proposal",
  "status": "in_progress",
  "priority": "high",
  "category_id": 1,
  "due_date": "2025-10-31T17:00:00"
}
```

**Request - Partial Update (only changed fields):**
```http
PUT /api/tasks/1
Content-Type: application/json

{
  "status": "completed",
  "priority": "medium"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project proposal (Updated)",
  "description": "Write, review, and submit the Q1 project proposal",
  "status": "completed",
  "priority": "medium",
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Work",
    "color": "#3B82F6"
  },
  "due_date": "2025-10-31T17:00:00",
  "created_at": "2025-10-22T10:00:00",
  "updated_at": "2025-10-22T15:00:00"
}
```

### 6. Update Task Status Only

**Request:**
```http
PATCH /api/tasks/1/status
Content-Type: application/json

{
  "status": "completed"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the Q1 project proposal",
  "status": "completed",
  "priority": "high",
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Work",
    "color": "#3B82F6"
  },
  "due_date": "2025-10-30T17:00:00",
  "created_at": "2025-10-22T10:00:00",
  "updated_at": "2025-10-22T16:00:00"
}
```

### 7. Delete a Task

**Request:**
```http
DELETE /api/tasks/1
```

**Response (204 No Content):**
```
(No response body)
```

**Error Response - Not Found (404):**
```json
{
  "message": "Task with id '999' not found",
  "status_code": 404,
  "details": {}
}
```

## JavaScript/Fetch Examples

### Create a Category

```javascript
const createCategory = async () => {
  const response = await fetch('http://localhost:8000/api/categories', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'Work',
      color: '#3B82F6'
    })
  });

  const category = await response.json();
  console.log('Created category:', category);
};
```

### Get All Tasks with Filters

```javascript
const getTasks = async (filters = {}) => {
  const params = new URLSearchParams(filters);
  const response = await fetch(`http://localhost:8000/api/tasks?${params}`);
  const data = await response.json();
  console.log(`Found ${data.total} tasks:`, data.tasks);
};

// Usage
getTasks({ status: 'in_progress', priority: 'high' });
```

### Create a Task

```javascript
const createTask = async (taskData) => {
  const response = await fetch('http://localhost:8000/api/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }

  const task = await response.json();
  console.log('Created task:', task);
  return task;
};

// Usage
createTask({
  title: 'Complete project proposal',
  description: 'Write and submit the Q1 project proposal',
  status: 'todo',
  priority: 'high',
  category_id: 1,
  due_date: '2025-10-30T17:00:00'
});
```

### Update Task Status

```javascript
const updateTaskStatus = async (taskId, newStatus) => {
  const response = await fetch(`http://localhost:8000/api/tasks/${taskId}/status`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: newStatus })
  });

  const task = await response.json();
  console.log('Updated task:', task);
  return task;
};

// Usage
updateTaskStatus(1, 'completed');
```

### Delete a Task

```javascript
const deleteTask = async (taskId) => {
  const response = await fetch(`http://localhost:8000/api/tasks/${taskId}`, {
    method: 'DELETE'
  });

  if (response.ok) {
    console.log('Task deleted successfully');
  }
};

// Usage
deleteTask(1);
```

## cURL Examples

### Create a Category

```bash
curl -X POST "http://localhost:8000/api/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Work",
    "color": "#3B82F6"
  }'
```

### Get All Tasks

```bash
curl "http://localhost:8000/api/tasks"
```

### Get Tasks with Filters

```bash
curl "http://localhost:8000/api/tasks?status=in_progress&priority=high"
```

### Create a Task

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project proposal",
    "description": "Write and submit the Q1 project proposal",
    "status": "todo",
    "priority": "high",
    "category_id": 1,
    "due_date": "2025-10-30T17:00:00"
  }'
```

### Update a Task

```bash
curl -X PUT "http://localhost:8000/api/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "priority": "medium"
  }'
```

### Update Task Status

```bash
curl -X PATCH "http://localhost:8000/api/tasks/1/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Delete a Task

```bash
curl -X DELETE "http://localhost:8000/api/tasks/1"
```

## Common Workflows

### 1. Setting up a new project

```javascript
// Step 1: Create categories
const workCategory = await createCategory({ name: 'Work', color: '#3B82F6' });
const personalCategory = await createCategory({ name: 'Personal', color: '#10B981' });

// Step 2: Create tasks
await createTask({
  title: 'Project planning',
  priority: 'high',
  category_id: workCategory.id
});

await createTask({
  title: 'Code review',
  priority: 'medium',
  category_id: workCategory.id
});
```

### 2. Task progression workflow

```javascript
// Create a new task
const task = await createTask({ title: 'Implement feature X' });

// Start working on it
await updateTaskStatus(task.id, 'in_progress');

// Complete it
await updateTaskStatus(task.id, 'completed');
```

### 3. Getting pending high-priority work tasks

```javascript
const response = await fetch(
  'http://localhost:8000/api/tasks?status=todo&priority=high&category_id=1'
);
const data = await response.json();
console.log(`You have ${data.total} urgent tasks to complete`);
```

## Status Values

- `todo` - Task not yet started
- `in_progress` - Task currently being worked on
- `completed` - Task finished

## Priority Values

- `low` - Low priority task
- `medium` - Medium priority task (default)
- `high` - High priority task

## Tips

1. **Always validate responses**: Check the HTTP status code before processing the response
2. **Use appropriate HTTP methods**: GET for reading, POST for creating, PUT for updating, PATCH for partial updates, DELETE for deleting
3. **Include category relationships**: Tasks automatically include category details in responses
4. **Filter efficiently**: Use query parameters to filter tasks instead of filtering on the client side
5. **Handle errors gracefully**: All error responses follow the same format with `message`, `status_code`, and `details`
