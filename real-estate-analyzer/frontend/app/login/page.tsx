"use client";

import { login } from "@/lib/api";
import { storeAuth } from "@/lib/auth";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await login(email, password);
      storeAuth(response.token, response.user);
      const nextPath = new URLSearchParams(window.location.search).get("next");
      router.push(nextPath ?? "/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-bg px-6">
      <form onSubmit={submit} className="w-full max-w-md rounded-2xl border border-border-green bg-surface p-8 shadow-glow">
        <Link href="/" className="font-display text-2xl text-text-primary">
          REIA
        </Link>
        <h1 className="mt-8 font-display text-5xl text-text-primary">Sign In</h1>
        <div className="mt-8 space-y-4">
          <input value={email} onChange={(event) => setEmail(event.target.value)} className="h-12 w-full rounded-xl border border-border-green bg-surface2 px-4 outline-none focus:border-accent" placeholder="Email" type="email" />
          <input value={password} onChange={(event) => setPassword(event.target.value)} className="h-12 w-full rounded-xl border border-border-green bg-surface2 px-4 outline-none focus:border-accent" placeholder="Password" type="password" />
        </div>
        {error ? <p className="mt-4 text-sm text-coral">{error}</p> : null}
        <button disabled={loading} className="mt-6 h-12 w-full rounded-xl bg-accent font-semibold text-bg hover:bg-accent-hover disabled:opacity-60">
          {loading ? "Signing in..." : "Sign In"}
        </button>
        <p className="mt-5 text-center text-sm text-text-secondary">
          Need an account?{" "}
          <Link href="/register" className="text-accent">
            Create one
          </Link>
        </p>
      </form>
    </main>
  );
}
