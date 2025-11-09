'use client'

import { useQuery } from '@tanstack/react-query'

interface Task {
  id: number
  title: string
  description: string | null
  status: string
  priority: string
  created_at: string
}

export default function DashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['tasks'],
    queryFn: async () => {
      const res = await fetch('/api/tasks')
      if (!res.ok) throw new Error('Failed to fetch tasks')
      const json = await res.json()
      return json.tasks || []
    },
  })

  const tasks = data as Task[] || []
  const stats = {
    total: tasks.length,
    todo: tasks.filter((t: Task) => t.status === 'todo').length,
    inProgress: tasks.filter((t: Task) => t.status === 'in_progress').length,
    completed: tasks.filter((t: Task) => t.status === 'completed').length,
  }

  if (isLoading) return <div className="text-center py-8">Loading...</div>
  if (error) return <div className="text-center py-8 text-red-600">Error: {(error as Error).message}</div>

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-bold">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">Total Tasks</div>
          <div className="text-3xl font-bold mt-2">{stats.total}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">To Do</div>
          <div className="text-3xl font-bold mt-2 text-blue-500">{stats.todo}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">In Progress</div>
          <div className="text-3xl font-bold mt-2 text-yellow-500">{stats.inProgress}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">Completed</div>
          <div className="text-3xl font-bold mt-2 text-green-500">{stats.completed}</div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-semibold mb-4">Recent Tasks</h2>
        {tasks.length === 0 ? (
          <p className="text-gray-500">No tasks yet. Create one to get started!</p>
        ) : (
          <div className="space-y-3">
            {tasks.slice(0, 5).map((task: Task) => (
              <div key={task.id} className="flex items-center justify-between py-2 border-b">
                <div>
                  <div className="font-medium">{task.title}</div>
                  <div className="text-sm text-gray-500">{task.status.replace('_', ' ')}</div>
                </div>
                <span className="text-sm px-3 py-1 rounded-full bg-gray-100 capitalize">
                  {task.priority}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="text-center text-gray-600">
        <p>Backend connected to: https://sumo-claude-code.onrender.com</p>
      </div>
    </div>
  )
}
