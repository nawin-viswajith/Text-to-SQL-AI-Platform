import { useMemo, useState } from "react";
import { runQuery } from "../services/api";
import type { QueryRequest, QueryResponse } from "../types/query";

type QueryState = {
  isLoading: boolean;
  data?: QueryResponse;
  error?: string;
};

export function useRunQuery() {
  const [state, setState] = useState<QueryState>({ isLoading: false });
  const sessionId = useMemo(() => `session-${crypto.randomUUID()}`, []);

  const submit = async (question: string) => {
    const payload: QueryRequest = {
      question,
      session_id: sessionId,
      max_retries: 2,
    };
    setState({ isLoading: true });
    try {
      const data = await runQuery(payload);
      setState({ isLoading: false, data });
      return data;
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown query error";
      setState({ isLoading: false, error: message });
      return null;
    }
  };

  return { state, submit, sessionId };
}

