import { motion } from "framer-motion";
import type { QueryResult } from "../types/query";

type Props = {
  result?: QueryResult | null;
};

function ResultsTablePanel({ result }: Props) {
  const columns = result?.columns ?? [];
  const rows = result?.rows ?? [];

  return (
    <motion.section
      className="panel"
      initial={{ opacity: 0, x: 18 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.35 }}
    >
      <h2 className="panel-title">Query Results</h2>
      <div className="max-h-[380px] overflow-auto rounded-xl border border-white/10">
        <table className="w-full min-w-[420px] border-collapse text-left text-sm">
          <thead>
            <tr className="bg-white/5 text-cyan-100">
              {columns.map((column) => (
                <th key={column} className="px-3 py-2">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td className="px-3 py-4 text-slate-400" colSpan={Math.max(columns.length, 1)}>
                  No rows returned.
                </td>
              </tr>
            ) : (
              rows.map((row, idx) => (
                <tr key={idx} className="border-t border-white/10 hover:bg-white/5">
                  {columns.map((column) => (
                    <td key={`${idx}-${column}`} className="px-3 py-2 text-slate-100">
                      {String(row[column] ?? "")}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs text-slate-300">
        Rows: {result?.row_count ?? 0} | Execution: {result?.execution_ms ?? 0} ms
      </p>
    </motion.section>
  );
}

export default ResultsTablePanel;

