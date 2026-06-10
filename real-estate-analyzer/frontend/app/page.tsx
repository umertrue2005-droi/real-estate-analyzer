"use client";

import SearchBar from "@/components/SearchBar";
import { createAnalysis } from "@/lib/api";
import { getToken, getUser, clearAuth } from "@/lib/auth";
import type { User } from "@/lib/types";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function HomePage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    setUser(getUser());
  }, []);

  async function analyze(address: string) {
    const token = getToken();
    if (!token) {
      router.push(`/login?next=${encodeURIComponent(`/?address=${address}`)}`);
      return;
    }
    const result = await createAnalysis(address, token);
    router.push(`/analyze/${result.analysis_id}`);
  }

  return (
    <main className="min-h-screen bg-bg">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">
        <Link href="/" className="font-display text-2xl text-text-primary">
          REIA
        </Link>
        <div className="flex items-center gap-4 text-sm text-text-secondary">
          {user ? (
            <>
              <span>{user.name}</span>
              <button
                onClick={() => {
                  clearAuth();
                  setUser(null);
                }}
                className="rounded-full border border-border-green px-4 py-2 hover:border-accent hover:text-text-primary"
              >
                Sign out
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="hover:text-text-primary">
                Login
              </Link>
              <Link href="/register" className="rounded-full border border-border-green px-4 py-2 hover:border-accent hover:text-text-primary">
                Register
              </Link>
            </>
          )}
        </div>
      </nav>

      <section className="mx-auto flex min-h-[calc(100vh-96px)] max-w-7xl flex-col justify-center px-6 pb-14">
        <div className="max-w-4xl">
          <p className="mb-5 inline-flex rounded-full border border-border-green px-4 py-2 font-mono text-xs uppercase text-accent">
            Five-agent underwriting
          </p>
          <h1 className="font-display text-6xl leading-none text-text-primary md:text-8xl">Analyze any property. In seconds.</h1>
          <p className="mt-6 max-w-2xl text-xl leading-8 text-text-secondary">
            Five AI agents evaluate investment potential and generate a full memo.
          </p>
        </div>
        <div className="mt-10">
          <SearchBar onAnalyze={analyze} />
        </div>
      </section>
    </main>
  );
}

