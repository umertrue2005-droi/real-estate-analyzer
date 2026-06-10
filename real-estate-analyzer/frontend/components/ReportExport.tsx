"use client";

import { saveReport } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useState } from "react";

export default function ReportExport({ id }: { id: string }) {
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  async function save() {
    const token = getToken();
    if (!token) {
      setError("Sign in again to save.");
      return;
    }
    try {
      await saveReport(id, token);
      setSaved(true);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save.");
    }
  }

  return (
    <div className="no-print flex flex-wrap gap-3">
      <button onClick={() => window.print()} className="rounded-full border border-border-green px-5 py-3 text-sm text-text-primary hover:border-accent">
        Export PDF
      </button>
      <button onClick={save} className="rounded-full bg-accent px-5 py-3 text-sm font-semibold text-bg hover:bg-accent-hover">
        {saved ? "Saved" : "Save Report"}
      </button>
      {error ? <span className="self-center text-sm text-coral">{error}</span> : null}
    </div>
  );
}

