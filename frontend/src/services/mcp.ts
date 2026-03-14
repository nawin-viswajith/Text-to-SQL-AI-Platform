const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";
const MCP_CLIENT_ID = "ui-dashboard";

export async function callMcpTool(toolName: string, toolInput: Record<string, unknown>) {
  const response = await fetch(`${API_BASE}/mcp/tools/${toolName}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Client-Id": MCP_CLIENT_ID,
    },
    body: JSON.stringify({ tool_input: toolInput }),
  });
  if (!response.ok) {
    throw new Error(`MCP tool call failed: ${response.status}`);
  }
  return response.json();
}

