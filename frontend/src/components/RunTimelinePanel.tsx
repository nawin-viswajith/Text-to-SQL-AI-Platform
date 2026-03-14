import { motion } from "framer-motion";
import type { QueryEvent } from "../types/query";

type Props = {
  events: QueryEvent[];
};

function RunTimelinePanel({ events }: Props) {
  return (
    <motion.section
      className="panel"
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.08, duration: 0.35 }}
    >
      <h2 className="panel-title">LangGraph Timeline</h2>
      <div className="space-y-2 text-xs">
        {events.length === 0 ? (
          <p className="text-slate-400">No timeline events yet.</p>
        ) : (
          events.map((event, idx) => (
            <div
              key={`${event.node}-${idx}`}
              className="rounded-lg border border-white/10 bg-black/20 px-3 py-2"
            >
              <p className="font-semibold text-cyan-100">{event.node}</p>
              <p className="text-slate-300">
                next: {event.next_step ?? "finish"} | retry: {event.retry_count}
              </p>
            </div>
          ))
        )}
      </div>
    </motion.section>
  );
}

export default RunTimelinePanel;

