export type QueryRequest = {
  question: string;
  session_id: string;
  user_id?: string;
  connection_id?: string;
  max_retries?: number;
};

export type AgentError = {
  code?: string;
  message: string;
  category:
    | "schema_mismatch"
    | "syntax"
    | "permission"
    | "connectivity"
    | "timeout"
    | "unknown";
  retryable: boolean;
};

export type QueryResult = {
  columns: string[];
  rows: Record<string, unknown>[];
  row_count: number;
  truncated: boolean;
  execution_ms?: number;
};

export type QueryEvent = {
  node: string;
  at: string;
  retry_count: number;
  has_error: boolean;
  error_category?: string | null;
  next_step?: string | null;
};

export type QueryResponse = {
  run_id: string;
  session_id: string;
  status: string;
  question: string;
  safe_sql?: string | null;
  result?: QueryResult | null;
  error?: AgentError | null;
  retries_used: number;
  reflection_notes: string[];
  events: QueryEvent[];
};

