"use client";

import AgentPipeline from "@/components/AgentPipeline";
import { getStatus } from "@/lib/api";
import { getToken } from "@/lib/auth";
import type { StatusResponse } from "@/lib/types";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function AnalyzePage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [seconds, setSeconds] = useState(45);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    const validToken: string = token;

    async function poll() {
      try {
        const data = await getStatus(params.id, validToken);
        setStatus(data);
        if (data.complete) router.push(`/dashboard/${params.id}`);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load status.");
      }
    }

    void poll();
    const pollId = window.setInterval(poll, 2000);
    const timerId = window.setInterval(
      () => setSeconds((value) => Math.max(value - 1, 0)),
      1000
    );
    return () => {
      window.clearInterval(pollId);
      window.clearInterval(timerId);
    };
  }, [params.id, router]);

  return (
    <main className="min-h-screen bg-bg px-6 py-8">
      <div className="mx-auto max-w-7xl">
        <nav className="flex items-center justify-between">
          <Link href="/" className="font-display text-2xl text-text-primary">
            REIA
          </Link>
          <span className="font-mono text-sm text-text-secondary">
            ETA {seconds}s
          </span>
        </nav>
        <header className="mt-12">
          <p className="font-mono text-xs uppercase text-accent">
            Agent Pipeline
          </p>
          <h1 className="mt-3 font-display text-5xl text-text-primary md:text-7xl">
            Analyzing: {status?.address ?? "Loading property"}
          </h1>
        </header>
        {error ? (
          <p className="mt-8 rounded-xl border border-coral/40 bg-surface p-4 text-coral">
            {error}
          </p>
        ) : null}
        <section className="mt-10">
          {status ? (
            <AgentPipeline agents={status.agents} />
          ) : (
            <div className="rounded-xl border border-border-green bg-surface p-8 text-text-secondary">
              Starting agents...
            </div>
          )}
        </section>
      </div>
    </main>
  );
}