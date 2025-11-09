# TaskFlow API Contract

## Base URL
`http://localhost:8000/api/v1`

## Authentication
Currently no authentication required (can be added later)

## Endpoints

### Tasks

#### GET /tasks
Get all tasks with optional filters
- **Query Parameters:**
  - `status` (optional): filter by status (todo, in_progress, done)
  - `priority` (optional): filter by priority (low, medium, high)
  - `category_id` (optional): filter by category ID
  - `search` (optional): search in title and description
- **Response:** `200 OK`
```json
[
  {
    "id": "string",
    "title": "string",
    "description": "string | null",
    "status": "todo" | "in_progress" | "done",
    "priority": "low" | "medium" | "high",
    "category_id": "string | null",
    "due_date": "string (ISO 8601) | null",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)"
  }
]
```

#### GET /tasks/{id}
Get a single task by ID
- **Response:** `200 OK` (same schema as task object above)
- **Error:** `404 Not Found`

#### POST /tasks
Create a new task
- **Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "status": "todo" | "in_progress" | "done" (default: "todo"),
  "priority": "low" | "medium" | "high" (default: "medium"),
  "category_id": "string (optional)",
  "due_date": "string (ISO 8601, optional)"
}
```
- **Response:** `201 Created` (task object)
- **Error:** `400 Bad Request` (validation errors)

#### PUT /tasks/{id}
Update an existing task
- **Request Body:** Same as POST (all fields optional except constraints)
- **Response:** `200 OK` (updated task object)
- **Error:** `404 Not Found`, `400 Bad Request`

#### PATCH /tasks/{id}/status
Update only the status of a task
- **Request Body:**
```json
{
  "status": "todo" | "in_progress" | "done"
}
```
- **Response:** `200 OK` (updated task object)

#### DELETE /tasks/{id}
Delete a task
- **Response:** `204 No Content`
- **Error:** `404 Not Found`

### Categories

#### GET /categories
Get all categories
- **Response:** `200 OK`
```json
[
  {
    "id": "string",
    "name": "string",
    "color": "string (hex color)",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)"
  }
]
```

#### GET /categories/{id}
Get a single category by ID
- **Response:** `200 OK` (category object)
- **Error:** `404 Not Found`

#### POST /categories
Create a new category
- **Request Body:**
```json
{
  "name": "string (required)",
  "color": "string (hex color, optional, default: random)"
}
```
- **Response:** `201 Created` (category object)
- **Error:** `400 Bad Request`

#### PUT /categories/{id}
Update a category
- **Request Body:**
```json
{
  "name": "string (optional)",
  "color": "string (optional)"
}
```
- **Response:** `200 OK` (updated category object)
- **Error:** `404 Not Found`, `400 Bad Request`

#### DELETE /categories/{id}
Delete a category
- **Response:** `204 No Content`
- **Error:** `404 Not Found`, `400 Bad Request` (if category has tasks)

### Dashboard/Statistics

#### GET /tasks/stats
Get task statistics for dashboard
- **Response:** `200 OK`
```json
{
  "total": "number",
  "by_status": {
    "todo": "number",
    "in_progress": "number",
    "done": "number"
  },
  "by_priority": {
    "low": "number",
    "medium": "number",
    "high": "number"
  },
  "overdue": "number",
  "due_today": "number",
  "due_this_week": "number"
}
```

## Error Response Format

All error responses follow this structure:
```json
{
  "detail": "Error message" | [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## Data Validation Rules

### Task
- `title`: required, 1-200 characters
- `description`: optional, max 2000 characters
- `status`: must be one of: "todo", "in_progress", "done"
- `priority`: must be one of: "low", "medium", "high"
- `due_date`: must be valid ISO 8601 date string

### Category
- `name`: required, 1-50 characters, unique
- `color`: must be valid hex color (e.g., "#FF5733")
