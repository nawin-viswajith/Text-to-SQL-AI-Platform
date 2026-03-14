import type { QueryRequest, QueryResponse } from "../types/query";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export async function runQuery(payload: QueryRequest): Promise<QueryResponse> {
  const response = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Query request failed with status ${response.status}`);
  }
  return (await response.json()) as QueryResponse;
}

export async function getRun(runId: string): Promise<unknown> {
  const response = await fetch(`${API_BASE}/runs/${runId}`);
  if (!response.ok) {
    throw new Error(`Run fetch failed with status ${response.status}`);
  }
  return response.json();
}

