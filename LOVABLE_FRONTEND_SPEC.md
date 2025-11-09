# TaskFlow Frontend Specification for Lovable

This document contains the complete specification for building the TaskFlow frontend on Lovable. Copy and paste relevant sections when creating your project.

---

## Project Overview

**Application**: TaskFlow - Modern task management application
**Frontend**: Next.js 14+ with TypeScript and Tailwind CSS
**Backend API**: FastAPI at `/api` (proxy configuration needed)
**Primary View**: Kanban board with drag-and-drop
**Additional Features**: Dashboard, dark mode, responsive design

---

## Tech Stack & Dependencies

### package.json Dependencies
```json
{
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "@tanstack/react-query": "^5.28.0",
    "@dnd-kit/core": "^6.1.0",
    "@dnd-kit/sortable": "^8.0.0",
    "@dnd-kit/utilities": "^3.2.2",
    "date-fns": "^3.3.1",
    "zod": "^3.22.4",
    "react-hook-form": "^7.51.0",
    "@hookform/resolvers": "^3.3.4",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.2.0",
    "@playwright/test": "^1.42.0"
  }
}
```

---

## Environment Configuration

### .env.local
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
```

### tailwind.config.ts
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [],
}
export default config
```

### app/globals.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

---

## TypeScript Types

### lib/types/task.ts
```typescript
export type TaskStatus = 'todo' | 'in_progress' | 'completed'
export type TaskPriority = 'low' | 'medium' | 'high'

export interface Task {
  id: number
  title: string
  description: string | null
  status: TaskStatus
  priority: TaskPriority
  category_id: number | null
  category?: Category
  due_date: string | null
  created_at: string
  updated_at: string
}

export interface CreateTaskInput {
  title: string
  description?: string
  status: TaskStatus
  priority: TaskPriority
  category_id?: number
  due_date?: string
}

export interface UpdateTaskInput extends Partial<CreateTaskInput> {}

export interface UpdateTaskStatusInput {
  status: TaskStatus
}
```

### lib/types/category.ts
```typescript
export interface Category {
  id: number
  name: string
  color: string
}

export interface CreateCategoryInput {
  name: string
  color?: string
}

export interface UpdateCategoryInput extends Partial<CreateCategoryInput> {}
```

### lib/types/stats.ts
```typescript
export interface TaskStats {
  total: number
  todo: number
  in_progress: number
  completed: number
  by_priority: {
    low: number
    medium: number
    high: number
  }
  by_category: Record<string, number>
}
```

### lib/types/api.ts
```typescript
export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}

export interface TasksListResponse {
  tasks: Task[]
  total: number
}

export interface CategoriesListResponse {
  categories: Category[]
  total: number
}
```

---

## API Client

### lib/api/client.ts
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'An error occurred' }))
      throw new Error(error.message || `HTTP ${response.status}`)
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

export const apiClient = new ApiClient(API_URL)
```

### lib/api/tasks.ts
```typescript
import { apiClient } from './client'
import type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  UpdateTaskStatusInput,
  TasksListResponse
} from '@/lib/types'

export const tasksApi = {
  getAll: async (params?: {
    status?: string
    priority?: string
    category_id?: number
  }) => {
    const searchParams = new URLSearchParams()
    if (params?.status) searchParams.append('status', params.status)
    if (params?.priority) searchParams.append('priority', params.priority)
    if (params?.category_id) searchParams.append('category_id', String(params.category_id))

    const query = searchParams.toString()
    return apiClient.get<TasksListResponse>(`/api/tasks${query ? `?${query}` : ''}`)
  },

  getById: (id: number) => apiClient.get<Task>(`/api/tasks/${id}`),

  create: (data: CreateTaskInput) => apiClient.post<Task>('/api/tasks', data),

  update: (id: number, data: UpdateTaskInput) =>
    apiClient.put<Task>(`/api/tasks/${id}`, data),

  updateStatus: (id: number, status: TaskStatus) =>
    apiClient.patch<Task>(`/api/tasks/${id}/status`, { status }),

  delete: (id: number) => apiClient.delete<void>(`/api/tasks/${id}`),
}
```

### lib/api/categories.ts
```typescript
import { apiClient } from './client'
import type { Category, CreateCategoryInput, CategoriesListResponse } from '@/lib/types'

export const categoriesApi = {
  getAll: () => apiClient.get<CategoriesListResponse>('/api/categories'),

  getById: (id: number) => apiClient.get<Category>(`/api/categories/${id}`),

  create: (data: CreateCategoryInput) => apiClient.post<Category>('/api/categories', data),

  delete: (id: number) => apiClient.delete<void>(`/api/categories/${id}`),
}
```

---

## React Query Hooks

### lib/hooks/useTasks.ts
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { tasksApi } from '@/lib/api/tasks'
import type { CreateTaskInput, UpdateTaskInput, TaskStatus } from '@/lib/types'

export const useTasks = (filters?: { status?: string; priority?: string; category_id?: number }) => {
  return useQuery({
    queryKey: ['tasks', filters],
    queryFn: () => tasksApi.getAll(filters),
  })
}

export const useTask = (id: number) => {
  return useQuery({
    queryKey: ['tasks', id],
    queryFn: () => tasksApi.getById(id),
    enabled: !!id,
  })
}

export const useCreateTask = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateTaskInput) => tasksApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export const useUpdateTask = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateTaskInput }) =>
      tasksApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export const useUpdateTaskStatus = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, status }: { id: number; status: TaskStatus }) =>
      tasksApi.updateStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export const useDeleteTask = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: number) => tasksApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}
```

### lib/hooks/useCategories.ts
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { categoriesApi } from '@/lib/api/categories'
import type { CreateCategoryInput } from '@/lib/types'

export const useCategories = () => {
  return useQuery({
    queryKey: ['categories'],
    queryFn: () => categoriesApi.getAll(),
  })
}

export const useCreateCategory = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateCategoryInput) => categoriesApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] })
    },
  })
}

export const useDeleteCategory = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: number) => categoriesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] })
    },
  })
}
```

---

## Key Components

### components/tasks/KanbanBoard.tsx

**Description**: Main Kanban board with three columns (Todo, In Progress, Done)

**Features**:
- Drag-and-drop between columns using @dnd-kit
- Optimistic updates
- Responsive: columns stack on mobile
- Shows task count per column
- Loading and empty states

**Props**: None (fetches data internally)

**Implementation Notes**:
- Uses DndContext from @dnd-kit/core
- Three droppable columns for each status
- On drop, calls `useUpdateTaskStatus` mutation
- Groups tasks by status before rendering

### components/tasks/TaskCard.tsx

**Description**: Individual task card (draggable)

**Props**:
```typescript
interface TaskCardProps {
  task: Task
  onEdit?: (task: Task) => void
  onDelete?: (id: number) => void
}
```

**Features**:
- Shows title, description (truncated), priority badge, category badge
- Due date with visual indicator (overdue in red)
- Edit and delete buttons
- Draggable handle
- Hover effects

### components/tasks/TaskForm.tsx

**Description**: Form for creating/editing tasks

**Props**:
```typescript
interface TaskFormProps {
  task?: Task  // If editing
  onSuccess?: () => void
  onCancel?: () => void
}
```

**Features**:
- React Hook Form with Zod validation
- Fields: title (required), description, status, priority, category, due date
- Error messages inline
- Submit and cancel buttons
- Uses `useCreateTask` or `useUpdateTask` mutations

### components/dashboard/StatsCard.tsx

**Description**: Card showing a single statistic

**Props**:
```typescript
interface StatsCardProps {
  title: string
  value: number
  icon?: React.ReactNode
  trend?: { value: number; positive: boolean }
  color?: string
}
```

**Features**:
- Large number display
- Optional icon
- Optional trend indicator
- Customizable color accent

### components/dashboard/BarChart.tsx

**Description**: Custom CSS-based bar chart (no libraries)

**Props**:
```typescript
interface BarChartProps {
  data: Array<{ label: string; value: number; color?: string }>
  maxValue?: number
}
```

**Implementation**:
- Uses Tailwind flex for bars
- Dynamic width based on percentage
- Animated with transitions
- Horizontal bars with labels

### components/layout/Navigation.tsx

**Description**: Top navigation bar

**Features**:
- Logo/app name
- Navigation links (Dashboard, Tasks, Categories)
- Dark mode toggle
- Mobile hamburger menu
- Active link highlighting

---

## Page Implementations

### app/page.tsx (Dashboard)

**Features**:
- 4 stats cards: Total tasks, Todo, In Progress, Completed
- Bar chart showing tasks by priority
- Pie chart showing tasks by category
- Recent tasks list (last 5)
- Links to create new task

**Data**:
- Fetches all tasks and computes stats client-side
- Fetches categories for pie chart

### app/tasks/page.tsx (Kanban Board)

**Features**:
- Main KanbanBoard component
- Filter bar above board (by priority, category)
- "Create Task" button
- Task count display

### app/tasks/list/page.tsx (List View)

**Features**:
- Table view of all tasks
- Sortable columns (title, priority, status, due date)
- Filter dropdowns
- Pagination
- Row click to edit

### app/categories/page.tsx

**Features**:
- Grid of category cards
- Each card shows color, name, task count
- "Create Category" button
- Delete category (with confirmation)
- Simple form: name input + color picker

---

## Styling Guidelines

### Color Scheme
- **Primary**: Blue (#3B82F6) - actions, links
- **Success**: Green (#10B981) - completed tasks
- **Warning**: Yellow (#F59E0B) - medium priority
- **Danger**: Red (#EF4444) - high priority, delete actions
- **Muted**: Gray (#6B7280) - low priority, secondary text

### Component Styling
- **Cards**: White background (light), dark gray (dark mode), rounded-lg, shadow-sm
- **Buttons**: Rounded-md, px-4, py-2, hover effects
- **Badges**: Rounded-full, px-2.5, py-0.5, text-xs, font-medium
- **Inputs**: Border, rounded-md, px-3, py-2, focus:ring-2

### Responsive Breakpoints
- **Mobile**: < 640px (sm)
- **Tablet**: 640px - 1024px (md, lg)
- **Desktop**: > 1024px (xl)

---

## Testing Requirements

### tests/e2e/kanban.spec.ts

```typescript
import { test, expect } from '@playwright/test'

test.describe('Kanban Board', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/tasks')
  })

  test('should display three columns', async ({ page }) => {
    await expect(page.getByText('To Do')).toBeVisible()
    await expect(page.getByText('In Progress')).toBeVisible()
    await expect(page.getByText('Done')).toBeVisible()
  })

  test('should create a new task', async ({ page }) => {
    await page.getByRole('button', { name: 'Create Task' }).click()
    await page.getByLabel('Title').fill('Test Task')
    await page.getByLabel('Priority').selectOption('high')
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('Test Task')).toBeVisible()
  })

  test('should drag task between columns', async ({ page }) => {
    // Create a task first
    await page.getByRole('button', { name: 'Create Task' }).click()
    await page.getByLabel('Title').fill('Draggable Task')
    await page.getByRole('button', { name: 'Create' }).click()

    // Drag from Todo to In Progress
    const task = page.getByText('Draggable Task')
    const inProgressColumn = page.getByTestId('column-in_progress')

    await task.dragTo(inProgressColumn)

    // Verify it moved
    await expect(inProgressColumn.getByText('Draggable Task')).toBeVisible()
  })
})
```

---

## Deployment Checklist

- [ ] All TypeScript types defined
- [ ] API client configured with correct base URL
- [ ] React Query provider set up in layout
- [ ] Theme provider for dark mode
- [ ] All 30+ components implemented
- [ ] Kanban board with drag-drop working
- [ ] Dashboard charts rendering correctly
- [ ] Forms with validation
- [ ] Mobile responsive design
- [ ] Dark mode toggle working
- [ ] E2E tests passing
- [ ] Environment variables configured
- [ ] Backend API proxy configured
- [ ] Error handling and loading states
- [ ] Empty states for no data

---

## Quick Start for Lovable

1. **Create new Next.js project** with TypeScript + Tailwind
2. **Install dependencies** from package.json above
3. **Copy configuration files**: next.config.js, tailwind.config.ts, globals.css
4. **Create folder structure**: lib/, components/, app/, tests/
5. **Implement types** in lib/types/
6. **Build API client** in lib/api/
7. **Create hooks** in lib/hooks/
8. **Implement UI components** in components/
9. **Build pages** in app/
10. **Write tests** in tests/e2e/
11. **Test locally** with backend running
12. **Deploy to Lovable**

---

## Support

- **Backend API Documentation**: http://localhost:8000/docs
- **Backend README**: `/Users/linus/taskflow-app/backend/README.md`
- **This Specification**: `/Users/linus/taskflow-app/LOVABLE_FRONTEND_SPEC.md`

---

Good luck building on Lovable! 🚀
