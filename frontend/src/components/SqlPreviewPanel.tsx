import { motion } from "framer-motion";

type Props = {
  sql?: string | null;
  notes: string[];
};

function SqlPreviewPanel({ sql, notes }: Props) {
  return (
    <motion.section
      className="panel"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.05, duration: 0.35 }}
    >
      <h2 className="panel-title">Generated SQL</h2>
      <pre className="code-block">{sql || "-- SQL will appear here after execution."}</pre>
      <h3 className="mt-4 text-sm font-semibold text-cyan-100">Reflexion Notes</h3>
      <ul className="mt-2 space-y-1 text-xs text-slate-300">
        {notes.length === 0 ? (
          <li>No notes yet.</li>
        ) : (
          notes.map((note, idx) => <li key={`${idx}-${note}`}>- {note}</li>)
        )}
      </ul>
    </motion.section>
  );
}

export default SqlPreviewPanel;

