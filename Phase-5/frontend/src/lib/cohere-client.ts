import { Todo } from '@/types';
import { MCPClient } from './mcp-client';
import { CohereClient as CohereSDK } from 'cohere-ai';

interface CohereResponse {
  text: string;
  todos?: Todo[];
}

interface ToolCall {
  tool_name: string;
  arguments: Record<string, any>;
}

interface CohereTool {
  name: string;
  description: string;
  parameter_definitions: Record<string, any>;
}

export class CohereClient {
  private apiKey: string;
  private mcpClient: MCPClient;
  private cohere: CohereSDK;

  constructor(apiKey?: string) {
    this.apiKey = apiKey || process.env.NEXT_PUBLIC_COHERE_API_KEY || 'JMfQBzVJJIdWvoFhgxTtft8uBYqclvrsRqgtmwzh';
    this.mcpClient = new MCPClient();

    // Initialize the Cohere SDK client
    this.cohere = new CohereSDK({
      token: this.apiKey,
    });
  }

  async chat(message: string, currentTodos: Todo[], token: string): Promise<CohereResponse> {
    try {
      // Define the tools available to the AI
      const tools = [
        {
          name: "add_task",
          description: "Add a new task to the user's list",
          parameter_definitions: {
            title: {
              type: "str",
              description: "The title of the task",
              required: true
            },
            description: {
              type: "str",
              description: "The description of the task (optional)",
              required: false
            },
            token: {
              type: "str",
              description: "JWT authentication token",
              required: true
            }
          }
        },
        {
          name: "get_tasks",
          description: "Retrieve the user's tasks",
          parameter_definitions: {
            status: {
              type: "str",
              description: "Filter by status: 'all', 'completed', 'pending' (optional)",
              required: false
            },
            token: {
              type: "str",
              description: "JWT authentication token",
              required: true
            }
          }
        },
        {
          name: "update_task",
          description: "Update an existing task",
          parameter_definitions: {
            task_id: {
              type: "int",
              description: "The ID of the task to update (optional if title_to_find is provided)",
              required: false
            },
            title_to_find: {
              type: "str",
              description: "The title of the task to find (optional if task_id is provided)",
              required: false
            },
            new_title: {
              type: "str",
              description: "New title (optional)",
              required: false
            },
            description: {
              type: "str",
              description: "New description (optional)",
              required: false
            },
            token: {
              type: "str",
              description: "JWT authentication token",
              required: true
            }
          }
        },
        {
          name: "delete_task",
          description: "Delete a task",
          parameter_definitions: {
            task_id: {
              type: "int",
              description: "The ID of the task to delete (optional if title_to_delete is provided)",
              required: false
            },
            title_to_delete: {
              type: "str",
              description: "The title of the task to delete (optional if task_id is provided)",
              required: false
            },
            token: {
              type: "str",
              description: "JWT authentication token",
              required: true
            }
          }
        },
        {
          name: "mark_complete",
          description: "Toggle the completion status of a task",
          parameter_definitions: {
            task_id: {
              type: "int",
              description: "The ID of the task to toggle (optional if title_to_mark is provided)",
              required: false
            },
            title_to_mark: {
              type: "str",
              description: "The title of the task to mark (optional if task_id is provided)",
              required: false
            },
            token: {
              type: "str",
              description: "JWT authentication token",
              required: true
            }
          }
        }
      ];

      // Call Cohere API to determine which tools to use based on the user message
      const response = await this.cohere.chat({
        message: message,
        tools: tools,
        model: "command-r-08-2024",  // Updated to supported model
      });

      // Check if the response includes tool calls
      if (response.toolCalls && response.toolCalls.length > 0) {
        const toolCalls: ToolCall[] = response.toolCalls.map((toolCall: any) => ({
          tool_name: toolCall.name,
          arguments: { ...toolCall.parameters, token } // Add the token to arguments
        }));

        // Execute the tool calls via MCP
        const results = await this.mcpClient.callTools(toolCalls, token);

        // Process the results and return appropriate response
        if (results.length > 0) {
          // Get the first result
          const result = results[0];

          let updatedTodos = currentTodos;

          if (result && result.result.success) {
            // Update todos based on the tool called
            switch (result.tool_name) {
              case "add_task":
                if (result.result.task) {
                  updatedTodos = [...currentTodos, result.result.task];
                } else {
                  updatedTodos = await this.fetchUpdatedTodos(token);
                }
                break;

              case "update_task":
                if (result.result.task) {
                  updatedTodos = currentTodos.map(todo =>
                    todo.id === result.result.task.id ? result.result.task : todo
                  );
                } else {
                  updatedTodos = await this.fetchUpdatedTodos(token);
                }
                break;

              case "delete_task":
                if (result.result.deleted_task) {
                  updatedTodos = currentTodos.filter(todo =>
                    todo.id !== result.result.deleted_task.id
                  );
                } else {
                  updatedTodos = await this.fetchUpdatedTodos(token);
                }
                break;

              case "mark_complete":
                if (result.result.task) {
                  updatedTodos = currentTodos.map(todo =>
                    todo.id === result.result.task.id ? result.result.task : todo
                  );
                } else {
                  updatedTodos = await this.fetchUpdatedTodos(token);
                }
                break;

              case "get_tasks":
                // For get_tasks, we just return the tasks from the result
                updatedTodos = result.result.tasks || [];

                // Format a proper response with the task list
                const tasks = result.result.tasks || [];
                if (tasks.length > 0) {
                  const statusFilter = toolCalls.find(call => call.tool_name === 'get_tasks')?.arguments?.status;
                  let responseText = '';

                  if (statusFilter === 'completed') {
                    responseText = `Here are your completed tasks (${tasks.length} total):\n\n`;
                  } else if (statusFilter === 'pending') {
                    responseText = `Here are your pending tasks (${tasks.length} total):\n\n`;
                  } else {
                    responseText = `Here are all your tasks (${tasks.length} total):\n\n`;
                  }

                  tasks.forEach((task: Todo, index: number) => {
                    const status = task.is_completed ? '✓' : '○';
                    responseText += `${index + 1}. [${status}] ID: ${task.id} - ${task.title}`;
                    if (task.description) {
                      responseText += `\n   Description: ${task.description}`;
                    }
                    responseText += '\n';
                  });

                  return {
                    text: responseText,
                    todos: updatedTodos
                  };
                } else {
                  let emptyResponse = 'You have no tasks';
                  const statusFilter = toolCalls.find(call => call.tool_name === 'get_tasks')?.arguments?.status;
                  if (statusFilter === 'completed') {
                    emptyResponse = 'You have no completed tasks';
                  } else if (statusFilter === 'pending') {
                    emptyResponse = 'You have no pending tasks';
                  }
                  return {
                    text: emptyResponse,
                    todos: updatedTodos
                  };
                }
                break;
            }

            return {
              text: result.result.message || response.text || "Operation completed successfully",
              todos: updatedTodos
            };
          } else {
            // If there was an error, fetch updated todos to ensure UI is in sync
            const refreshedTodos = await this.fetchUpdatedTodos(token);
            return {
              text: result?.result?.error || "An error occurred while processing your request",
              todos: refreshedTodos
            };
          }
        } else {
          // If no tool calls were made, return the text response
          return {
            text: response.text || "I processed your request",
            todos: currentTodos
          };
        }
      } else {
        // If no tools were called, return the text response from Cohere
        return {
          text: response.text || "I'm here to help you manage your tasks!",
          todos: currentTodos
        };
      }
    } catch (error) {
      console.error('Error calling Cohere API:', error);

      // Return a helpful error message
      return {
        text: "Sorry, I encountered an error processing your request. Please try again.",
        todos: currentTodos
      };
    }
  }

  private async fetchUpdatedTodos(token: string): Promise<Todo[]> {
    try {
      const response = await fetch('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch updated tasks: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching updated todos:', error);
      // Return current todos if fetch fails
      return [];
    }
  }
}