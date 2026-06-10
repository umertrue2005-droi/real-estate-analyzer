"use client";

import ReportExport from "@/components/ReportExport";
import { getReport } from "@/lib/api";
import { getToken } from "@/lib/auth";
import type { ReportResponse } from "@/lib/types";
import Link from "next/link";
import { useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { useEffect, useState } from "react";

const sections = ["Executive Summary", "Market Analysis", "Financial Model", "Zoning & Legal", "Risk Assessment", "Recommendation"];

function sectionId(section: string) {
  return section.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

export default function ReportPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    getReport(params.id, token)
      .then(setReport)
      .catch((err: unknown) => setError(err instanceof Error ? err.message : "Unable to load report."));
  }, [params.id, router]);

  if (error) {
    return <main className="grid min-h-screen place-items-center bg-bg px-6 text-coral">{error}</main>;
  }

  if (!report) {
    return <main className="grid min-h-screen place-items-center bg-bg px-6 text-text-secondary">Loading report...</main>;
  }

  return (
    <main className="min-h-screen bg-bg px-6 py-8">
      <div className="mx-auto grid max-w-7xl gap-8 lg:grid-cols-[260px_1fr]">
        <aside className="no-print lg:sticky lg:top-8 lg:self-start">
          <Link href={`/dashboard/${params.id}`} className="font-display text-2xl text-text-primary">
            REIA
          </Link>
          <nav className="mt-8 space-y-2">
            {sections.map((section) => (
              <a key={section} href={`#${sectionId(section)}`} className="block rounded-full border border-border-green px-4 py-3 text-sm text-text-secondary hover:border-accent hover:text-text-primary">
                {section}
              </a>
            ))}
          </nav>
        </aside>

        <article className="print-surface rounded-2xl border border-border-green bg-surface p-6 md:p-10">
          <div className="mb-8 flex flex-col justify-between gap-5 border-b border-border-green pb-8 md:flex-row md:items-center">
            <div>
              <p className="font-mono text-xs uppercase text-accent">Investment Memo</p>
              <h1 className="mt-2 font-display text-5xl text-text-primary">{report.verdict}</h1>
            </div>
            <ReportExport id={params.id} />
          </div>

          <div className="mb-8 grid gap-4 md:grid-cols-3">
            <Callout label="Verdict" value={report.verdict} />
            <Callout label="Recommendation" value={report.recommendation} />
            <Callout label="Sources" value="ATTOM, Rentcast, Walk Score, Census" />
          </div>

          <div className="prose prose-invert max-w-none prose-headings:font-display prose-headings:text-text-primary prose-p:leading-8 prose-p:text-text-secondary prose-strong:text-text-primary">
            <ReactMarkdown
              components={{
                h2: ({ children }) => <h2 id={sectionId(String(children))}>{children}</h2>
              }}
            >
              {report.memo_markdown}
            </ReactMarkdown>
          </div>

          <div className="mt-10 flex flex-wrap gap-2 border-t border-border-green pt-6">
            {["ATTOM", "Rentcast", "Walk Score", "Census"].map((source) => (
              <span key={source} className="rounded-full border border-border-green px-3 py-2 font-mono text-xs text-text-secondary">
                {source}
              </span>
            ))}
          </div>
        </article>
      </div>
    </main>
  );
}

function Callout({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-border-green bg-surface2 p-4">
      <p className="font-mono text-xs uppercase text-accent">{label}</p>
      <p className="mt-2 text-sm leading-6 text-text-primary">{value}</p>
    </div>
  );
}

