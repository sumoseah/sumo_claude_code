# TaskFlow Frontend

Modern task management application frontend built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

- **Dashboard** - View task statistics and recent tasks
- **Kanban Board** - Drag-and-drop task management across three columns (Todo, In Progress, Done)
- **Categories** - Create and manage task categories with custom colors

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Query (@tanstack/react-query)
- DnD Kit (@dnd-kit) for drag-and-drop

## Backend

Connected to FastAPI backend at: `https://sumo-claude-code.onrender.com`

## Deployment

Deployed on Vercel. The app automatically proxies `/api/*` requests to the backend.

## Local Development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)
