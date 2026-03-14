import { Link } from "react-router-dom";

function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-space px-4 text-slate-100">
      <div className="panel max-w-md text-center">
        <h1 className="text-2xl font-bold text-cyan-100">404</h1>
        <p className="mt-2 text-sm text-slate-300">This route does not exist.</p>
        <Link to="/" className="mt-4 inline-block rounded-xl bg-cyan-300 px-4 py-2 text-slate-900">
          Go to Dashboard
        </Link>
      </div>
    </main>
  );
}

export default NotFound;

