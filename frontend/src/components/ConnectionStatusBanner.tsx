type Props = {
  status: "connected" | "disconnected" | "unknown";
};

function ConnectionStatusBanner({ status }: Props) {
  const styles =
    status === "connected"
      ? "bg-emerald-500/15 text-emerald-200 border-emerald-400/40"
      : status === "disconnected"
        ? "bg-rose-500/15 text-rose-200 border-rose-400/40"
        : "bg-slate-500/15 text-slate-200 border-slate-400/40";

  return (
    <div className={`rounded-xl border px-4 py-2 text-sm ${styles}`}>
      Database Status: <span className="font-semibold">{status.toUpperCase()}</span>
    </div>
  );
}

export default ConnectionStatusBanner;

