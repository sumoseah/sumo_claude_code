'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <html lang="en">
      <body>
        <QueryClientProvider client={queryClient}>
          <nav className="bg-blue-600 text-white p-4 shadow-lg">
            <div className="container mx-auto flex items-center justify-between">
              <h1 className="text-2xl font-bold">TaskFlow</h1>
              <div className="flex gap-4">
                <a href="/" className="hover:underline">Dashboard</a>
                <a href="/tasks" className="hover:underline">Kanban</a>
                <a href="/categories" className="hover:underline">Categories</a>
              </div>
            </div>
          </nav>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
        </QueryClientProvider>
      </body>
    </html>
  )
}
