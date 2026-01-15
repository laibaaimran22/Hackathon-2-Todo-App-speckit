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
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTodoRequest {
  title: string;
}

export interface UpdateTodoRequest {
  title?: string;
  is_completed?: boolean;
}
