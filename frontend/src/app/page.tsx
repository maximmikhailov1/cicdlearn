"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export default function Home() {
  const [health, setHealth] = useState<{ status?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then(setHealth)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <main style={{ padding: "2rem", maxWidth: "40rem", margin: "0 auto" }}>
      <h1>cicdlearn</h1>
      <p>CI/CD learning project — FastAPI + Next.js + PostgreSQL + MongoDB</p>
      <section style={{ marginTop: "1.5rem" }}>
        <h2>Backend health</h2>
        {error && <p style={{ color: "#f88" }}>Error: {error}</p>}
        {health && <p data-testid="health-status">Status: {health.status ?? "unknown"}</p>}
        {!health && !error && <p>Loading…</p>}
      </section>
    </main>
  );
}
