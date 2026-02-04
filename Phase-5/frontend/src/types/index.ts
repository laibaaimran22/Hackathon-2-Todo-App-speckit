export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface Todo {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  priority: string; // high/medium/low
  due_date: string | null; // ISO date string
  recurrence_pattern: string | null; // daily/weekly/monthly
  owner_id: string;
  created_at: string;
  updated_at: string;
  tags: string[]; // Array of tag names
}

export interface CreateTodoRequest {
  title: string;
  description?: string;
  priority?: string;
  due_date?: string;
  recurrence_pattern?: string;
  tag_names?: string[];
}

export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  is_completed?: boolean;
  priority?: string;
  due_date?: string;
  recurrence_pattern?: string;
  tag_names?: string[];
}
