import { useState } from "react";
import { motion } from "framer-motion";

type Props = {
  isLoading: boolean;
  onSubmit: (question: string) => void;
};

function QueryInputPanel({ isLoading, onSubmit }: Props) {
  const [question, setQuestion] = useState("");

  return (
    <motion.section
      className="panel"
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      <h2 className="panel-title">Natural Language Input</h2>
      <textarea
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Example: Show top 10 customers by revenue in Q1."
        className="min-h-40 w-full rounded-xl border border-white/20 bg-black/20 p-3 text-sm text-slate-100 outline-none focus:border-cyan-300"
      />
      <button
        onClick={() => onSubmit(question)}
        disabled={isLoading || !question.trim()}
        className="mt-3 rounded-xl bg-cyan-300 px-4 py-2 font-medium text-slate-900 transition hover:bg-cyan-200 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isLoading ? "Running..." : "Run Query"}
      </button>
    </motion.section>
  );
}

export default QueryInputPanel;

