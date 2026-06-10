"use client";

import { FormEvent, useState } from "react";

type SearchBarProps = {
  onAnalyze: (address: string) => Promise<void>;
};

const quickPicks = ["78702 Austin TX", "33101 Miami FL", "10001 New York NY", "90210 Beverly Hills CA"];

export default function SearchBar({ onAnalyze }: SearchBarProps) {
  const [address, setAddress] = useState("2401 E 6th St, Austin, TX 78702");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!address.trim()) {
      setError("Enter an address or ZIP code.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await onAnalyze(address.trim());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to start analysis.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full max-w-4xl">
      <form onSubmit={submit} className="flex flex-col gap-3 rounded-2xl border border-border-green bg-surface p-3 shadow-glow md:flex-row">
        <input
          value={address}
          onChange={(event) => setAddress(event.target.value)}
          className="min-h-14 flex-1 rounded-xl border border-border-green bg-surface2 px-5 text-base text-text-primary outline-none placeholder:text-text-muted focus:border-accent"
          placeholder="Enter property address or ZIP"
        />
        <button
          type="submit"
          disabled={loading}
          className="min-h-14 rounded-xl bg-accent px-7 font-semibold text-bg transition hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Analyzing..." : "Analyze ->"}
        </button>
      </form>
      {error ? <p className="mt-3 text-sm text-coral">{error}</p> : null}
      <div className="mt-5 flex flex-wrap gap-2">
        {quickPicks.map((pick) => (
          <button
            key={pick}
            type="button"
            onClick={() => setAddress(pick)}
            className="rounded-full border border-border-green bg-surface px-4 py-2 font-mono text-xs text-text-secondary transition hover:border-accent hover:text-text-primary"
          >
            {pick}
          </button>
        ))}
      </div>
    </div>
  );
}

