"use client";

import { storeAuth } from "@/lib/auth";
import type { User } from "@/lib/types";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

type AuthResponse = {
  token: string;
  user: User;
};

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("Demo Investor");
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });
      if (!res.ok) {
        const detail = await res.text();
        throw new Error(detail || `Request failed with ${res.status}`);
      }
      const response = (await res.json()) as AuthResponse;
      storeAuth(response.token, response.user);
      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create account.");
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
        <h1 className="mt-8 font-display text-5xl text-text-primary">Create Account</h1>
        <div className="mt-8 space-y-4">
          <input value={name} onChange={(event) => setName(event.target.value)} className="h-12 w-full rounded-xl border border-border-green bg-surface2 px-4 outline-none focus:border-accent" placeholder="Name" />
          <input value={email} onChange={(event) => setEmail(event.target.value)} className="h-12 w-full rounded-xl border border-border-green bg-surface2 px-4 outline-none focus:border-accent" placeholder="Email" type="email" />
          <input value={password} onChange={(event) => setPassword(event.target.value)} className="h-12 w-full rounded-xl border border-border-green bg-surface2 px-4 outline-none focus:border-accent" placeholder="Password" type="password" />
        </div>
        {error ? <p className="mt-4 text-sm text-coral">{error}</p> : null}
        <button disabled={loading} className="mt-6 h-12 w-full rounded-xl bg-accent font-semibold text-bg hover:bg-accent-hover disabled:opacity-60">
          {loading ? "Creating..." : "Create Account"}
        </button>
        <p className="mt-5 text-center text-sm text-text-secondary">
          Already registered?{" "}
          <Link href="/login" className="text-accent">
            Sign in
          </Link>
        </p>
      </form>
    </main>
  );
}
