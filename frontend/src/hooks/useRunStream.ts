import { useState } from "react";
import type { QueryEvent } from "../types/query";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export function useRunStream() {
  const [events, setEvents] = useState<QueryEvent[]>([]);

  const stream = async (question: string, sessionId: string) => {
    setEvents([]);
    const response = await fetch(`${API_BASE}/query/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, session_id: sessionId, max_retries: 2 }),
    });
    if (!response.body) {
      return;
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      buffer += decoder.decode(value, { stream: true });
      const chunks = buffer.split("\n\n");
      buffer = chunks.pop() ?? "";
      for (const chunk of chunks) {
        if (!chunk.startsWith("data: ")) {
          continue;
        }
        const raw = chunk.slice(6);
        try {
          const payload = JSON.parse(raw);
          if (payload.type === "event") {
            setEvents((prev) => [...prev, payload.payload]);
          }
        } catch {
          // Ignore malformed stream frames
        }
      }
    }
  };

  return { events, stream };
}

