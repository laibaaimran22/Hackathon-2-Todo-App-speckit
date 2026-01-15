"""
MCP (Model Context Protocol) server for Cohere AI integration.
Exposes task management tools to the AI agent.
"""

import json
import uuid
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio

# Import task tools using direct file path import to avoid naming conflicts
import importlib.util
import os

# Get the path to task_tools.py
task_tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'task_tools.py')
task_tools_spec = importlib.util.spec_from_file_location("task_tools", task_tools_path)
task_tools_module = importlib.util.module_from_spec(task_tools_spec)
task_tools_spec.loader.exec_module(task_tools_module)

# Import the functions
add_task_tool = task_tools_module.add_task_tool
get_tasks_tool = task_tools_module.get_tasks_tool
update_task_tool = task_tools_module.update_task_tool
delete_task_tool = task_tools_module.delete_task_tool
mark_complete_tool = task_tools_module.mark_complete_tool


class ToolCall(BaseModel):
    """Represents a tool call from the AI agent."""
    tool_name: str
    arguments: Dict[str, Any]


class ToolResult(BaseModel):
    """Represents the result of a tool call."""
    tool_name: str
    result: Dict[str, Any]
    call_id: str


class MCPRequest(BaseModel):
    """Represents an MCP request from the AI agent."""
    type: str
    tools: Optional[List[Dict]] = None
    calls: Optional[List[ToolCall]] = None


class MCPServer:
    """MCP server implementation for task management tools."""

    def __init__(self):
        self.tools = {
            "add_task": {
                "name": "add_task",
                "description": "Add a new task to the user's list",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "The description of the task (optional)"},
                        "token": {"type": "string", "description": "JWT authentication token"}
                    },
                    "required": ["title", "token"]
                }
            },
            "get_tasks": {
                "name": "get_tasks",
                "description": "Retrieve the user's tasks",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "completed", "pending"],
                            "description": "Filter by status (optional, default: all)"
                        },
                        "token": {"type": "string", "description": "JWT authentication token"}
                    },
                    "required": ["token"]
                }
            },
            "update_task": {
                "name": "update_task",
                "description": "Update an existing task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title_to_find": {"type": "string", "description": "The title of the task to find (optional if task_id is provided)"},
                        "new_title": {"type": "string", "description": "New title (optional)"},
                        "description": {"type": "string", "description": "New description (optional)"},
                        "token": {"type": "string", "description": "JWT authentication token"}
                    },
                    "required": ["token"]
                }
            },
            "delete_task": {
                "name": "delete_task",
                "description": "Delete a task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"},
                        "title_to_delete": {"type": "string", "description": "The title of the task to delete (optional if task_id is provided)"},
                        "token": {"type": "string", "description": "JWT authentication token"}
                    },
                    "required": ["token"]
                }
            },
            "mark_complete": {
                "name": "mark_complete",
                "description": "Toggle the completion status of a task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to toggle"},
                        "title_to_mark": {"type": "string", "description": "The title of the task to mark (optional if task_id is provided)"},
                        "token": {"type": "string", "description": "JWT authentication token"}
                    },
                    "required": ["token"]
                }
            }
        }

    async def get_tools(self) -> List[Dict]:
        """Return the list of available tools."""
        return list(self.tools.values())

    async def call_tool(self, tool_call: ToolCall, token: str) -> ToolResult:
        """Execute a tool call."""
        tool_name = tool_call.tool_name

        if tool_name not in self.tools:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")

        # Add token to arguments if not already present
        args = tool_call.arguments.copy()
        if 'token' not in args:
            args['token'] = token

        # Call the appropriate tool function
        try:
            if tool_name == "add_task":
                result = await add_task_tool(
                    title=args.get("title"),
                    description=args.get("description", ""),
                    token=token
                )
            elif tool_name == "get_tasks":
                result = await get_tasks_tool(
                    status=args.get("status"),
                    token=token
                )
            elif tool_name == "update_task":
                result = await update_task_tool(
                    task_id=args.get("task_id"),
                    title_to_find=args.get("title_to_find"),
                    new_title=args.get("new_title"),
                    description=args.get("description"),
                    token=token
                )
            elif tool_name == "delete_task":
                result = await delete_task_tool(
                    task_id=args.get("task_id"),
                    title_to_delete=args.get("title_to_delete"),
                    token=token
                )
            elif tool_name == "mark_complete":
                result = await mark_complete_tool(
                    task_id=args.get("task_id"),
                    title_to_mark=args.get("title_to_mark"),
                    token=token
                )
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            result = {"error": f"Tool execution failed: {str(e)}"}

        call_id = str(uuid.uuid4())
        return ToolResult(tool_name=tool_name, result=result, call_id=call_id)

    async def process_calls(self, calls: List[ToolCall], token: str) -> List[ToolResult]:
        """Process multiple tool calls."""
        results = []
        for call in calls:
            result = await self.call_tool(call, token)
            results.append(result)
        return results


# Global MCP server instance
mcp_server = MCPServer()


# FastAPI app for MCP endpoints
app = FastAPI(title="Todo Chatbot MCP Server", version="1.0.0")


@app.get("/tools")
async def get_mcp_tools():
    """Endpoint to get available tools."""
    tools = await mcp_server.get_tools()
    return {"tools": tools}


from fastapi import Request

@app.post("/call-tools")
async def call_mcp_tools(request: MCPRequest, req: Request):
    """Endpoint to call tools."""
    if request.type != "call-tools":
        raise HTTPException(status_code=400, detail="Invalid request type")

    if not request.calls:
        raise HTTPException(status_code=400, detail="No tool calls provided")

    # Extract token from Authorization header
    auth_header = req.headers.get("authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix
    elif request.calls and request.calls[0].arguments.get("token"):
        # Fallback to token in arguments if not in header
        token = request.calls[0].arguments["token"]

    if not token:
        raise HTTPException(status_code=401, detail="Authorization token required")

    results = await mcp_server.process_calls(request.calls, token)
    return {"results": [result.dict() for result in results]}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mcp-server"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)