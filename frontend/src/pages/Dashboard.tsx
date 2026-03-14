import { motion } from "framer-motion";
import ConnectionStatusBanner from "../components/ConnectionStatusBanner";
import QueryInputPanel from "../components/QueryInputPanel";
import ResultsTablePanel from "../components/ResultsTablePanel";
import RunTimelinePanel from "../components/RunTimelinePanel";
import SqlPreviewPanel from "../components/SqlPreviewPanel";
import { useRunQuery } from "../hooks/useRunQuery";
import { useRunStream } from "../hooks/useRunStream";

function Dashboard() {
  const { state, submit, sessionId } = useRunQuery();
  const { events, stream } = useRunStream();

  const onSubmit = async (question: string) => {
    if (!question.trim()) {
      return;
    }
    stream(question, sessionId).catch(() => {
      // Streaming failures should not block sync query path.
    });
    await submit(question);
  };

  const dbStatus =
    state.data?.error?.category === "connectivity"
      ? "disconnected"
      : state.data
        ? "connected"
        : "unknown";

  return (
    <main className="min-h-screen bg-space px-4 py-8 text-slate-100 md:px-8">
      <motion.header
        className="mx-auto mb-6 max-w-7xl"
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
      >
        <h1 className="text-2xl font-bold tracking-wide text-cyan-100 md:text-3xl">
          Enterprise Text-to-SQL Control Room
        </h1>
        <p className="mt-2 text-sm text-slate-300">
          Reflexion-enabled SQL generation with schema-aware recovery and MCP tooling.
        </p>
      </motion.header>

      <section className="mx-auto grid max-w-7xl grid-cols-1 gap-4 xl:grid-cols-2">
        <div className="space-y-4">
          <ConnectionStatusBanner status={dbStatus} />
          <QueryInputPanel isLoading={state.isLoading} onSubmit={onSubmit} />
          <SqlPreviewPanel
            sql={state.data?.safe_sql}
            notes={state.data?.reflection_notes ?? (state.error ? [state.error] : [])}
          />
        </div>
        <div className="space-y-4">
          <ResultsTablePanel result={state.data?.result} />
          <RunTimelinePanel events={events.length > 0 ? events : state.data?.events ?? []} />
        </div>
      </section>
    </main>
  );
}

export default Dashboard;

