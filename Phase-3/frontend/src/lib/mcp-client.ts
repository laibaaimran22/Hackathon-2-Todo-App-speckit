interface ToolCall {
  tool_name: string;
  arguments: Record<string, any>;
}

interface ToolResult {
  tool_name: string;
  result: Record<string, any>;
  call_id: string;
}

interface MCPRequest {
  type: string;
  tools?: Array<any>;
  calls?: ToolCall[];
}

interface MCPResponse {
  results?: ToolResult[];
  tools?: Array<any>;
}

export class MCPClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    // Use environment variable or default to backend /mcp endpoint for production
    // Ensure proper URL formatting by removing trailing slash from API URL if present
    const apiUrl = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || '';
    this.baseUrl = baseUrl || process.env.NEXT_PUBLIC_MCP_BASE_URL || `${apiUrl}/mcp`;
  }

  async getTools(): Promise<any[]> {
    try {
      const response = await fetch(`${this.baseUrl}/tools`);
      if (!response.ok) {
        throw new Error(`Failed to fetch tools: ${response.statusText}`);
      }
      const data: MCPResponse = await response.json();
      return data.tools || [];
    } catch (error) {
      console.error('Error fetching tools:', error);
      throw error;
    }
  }

  async callTools(calls: ToolCall[], token: string): Promise<ToolResult[]> {
    try {
      const requestBody: MCPRequest = {
        type: "call-tools",
        calls: calls
      };

      const response = await fetch(`${this.baseUrl}/call-tools`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`Failed to call tools: ${response.statusText}`);
      }

      const data: MCPResponse = await response.json();
      return data.results || [];
    } catch (error) {
      console.error('Error calling tools:', error);
      throw error;
    }
  }
}