import { useEffect, useState } from "react";

type Status = { label: string; ok: boolean; detail?: string };

export default function App() {
  const [rows, setRows] = useState<Status[]>([]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const checks: Status[] = [];

      try {
        const res = await fetch("/health");
        checks.push({
          label: "API /health",
          ok: res.ok,
          detail: res.ok ? await res.text() : res.statusText,
        });
      } catch (e) {
        checks.push({
          label: "API /health",
          ok: false,
          detail: String(e),
        });
      }

      try {
        const res = await fetch("/ai/health");
        const j = await res.json().catch(() => ({}));
        checks.push({
          label: "AI worker /ai/health",
          ok: res.ok,
          detail: JSON.stringify(j),
        });
      } catch (e) {
        checks.push({
          label: "AI worker /ai/health",
          ok: false,
          detail: String(e),
        });
      }

      if (!cancelled) setRows(checks);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main style={{ fontFamily: "system-ui", padding: "2rem", maxWidth: 640 }}>
      <h1>Resume AI</h1>
      <p>Frontend + API + AI worker (via Nginx paths /api, /ai).</p>
      <ul>
        {rows.map((r) => (
          <li key={r.label}>
            <strong>{r.label}</strong>: {r.ok ? "ok" : "fail"}
            {r.detail ? <pre style={{ fontSize: 12 }}>{r.detail}</pre> : null}
          </li>
        ))}
      </ul>
    </main>
  );
}
