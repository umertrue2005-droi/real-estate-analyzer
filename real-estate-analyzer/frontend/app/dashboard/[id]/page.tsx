"use client";

import BarComparison from "@/components/BarComparison";
import MetricCard from "@/components/MetricCard";
import RiskRing from "@/components/RiskRing";
import VerdictBox from "@/components/VerdictBox";
import { getResults } from "@/lib/api";
import { getToken } from "@/lib/auth";
import type { ResultsResponse } from "@/lib/types";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

function percent(value: number) {
  return `${value.toFixed(1)}%`;
}

function capTone(value: number): "green" | "amber" | "red" {
  if (value > 5) return "green";
  if (value >= 3) return "amber";
  return "red";
}

function riskTone(value: number): "green" | "amber" | "red" {
  if (value < 30) return "green";
  if (value <= 60) return "amber";
  return "red";
}

export default function DashboardPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [results, setResults] = useState<ResultsResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    getResults(params.id, token)
      .then(setResults)
      .catch((err: unknown) => setError(err instanceof Error ? err.message : "Unable to load results."));
  }, [params.id, router]);

  if (error) {
    return (
      <main className="grid min-h-screen place-items-center bg-bg px-6 text-coral">
        <div className="rounded-xl border border-coral/40 bg-surface p-8">{error}</div>
      </main>
    );
  }

  if (!results) {
    return (
      <main className="grid min-h-screen place-items-center bg-bg px-6 text-text-secondary">
        <div className="rounded-xl border border-border-green bg-surface p-8">Loading dashboard...</div>
      </main>
    );
  }

  const topComp = Math.max(...results.market_data.comp_properties.map((comp) => comp.price_per_sqft));

  return (
    <main className="min-h-screen bg-bg px-6 py-8">
      <div className="mx-auto max-w-7xl">
        <nav className="flex items-center justify-between">
          <Link href="/" className="font-display text-2xl text-text-primary">
            REIA
          </Link>
          <Link href={`/report/${params.id}`} className="rounded-full bg-accent px-5 py-3 text-sm font-semibold text-bg hover:bg-accent-hover">
            View Full Report {"->"}
          </Link>
        </nav>

        <header className="mt-10">
          <p className="font-mono text-xs uppercase text-accent">Investment Dashboard</p>
          <h1 className="mt-3 font-display text-5xl text-text-primary md:text-7xl">{results.address}</h1>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard label="Cap Rate" value={percent(results.financial_data.cap_rate)} tone={capTone(results.financial_data.cap_rate)} />
          <MetricCard label="Cash-on-Cash Return" value={percent(results.financial_data.cash_on_cash)} tone={results.financial_data.cash_on_cash > 8 ? "green" : "amber"} />
          <article className="rounded-xl border border-border-green bg-surface p-6">
            <p className="font-mono text-xs uppercase text-text-secondary">Risk Score</p>
            <div className="mt-4 flex items-center justify-between">
              <RiskRing score={results.risk_data.risk_score} />
              <span className={`font-display text-4xl ${riskTone(results.risk_data.risk_score) === "green" ? "text-accent" : riskTone(results.risk_data.risk_score) === "amber" ? "text-amber" : "text-coral"}`}>/100</span>
            </div>
          </article>
          <MetricCard label="Break-even Occupancy" value={percent(results.financial_data.break_even_occ)} helper="Expense coverage threshold" />
        </section>

        <section className="mt-5 grid gap-5 lg:grid-cols-2">
          <BarComparison
            bars={[
              { label: "Subject", value: results.market_data.price_per_sqft },
              { label: "ZIP Median", value: Math.round(results.market_data.median_price / 1714) },
              { label: "City Avg", value: Math.round(results.market_data.city_avg_price / 1714) },
              { label: "Top Comp", value: topComp }
            ]}
          />
          <VerdictBox verdict={results.report_data.verdict} text={results.report_data.summary} />
        </section>

        <section className="mt-5 grid gap-5 lg:grid-cols-3">
          <Panel title="Neighborhood">
            <Line label="Walk Score" value={String(results.risk_data.walk_score)} />
            <Line label="Transit Score" value={String(results.risk_data.transit_score)} />
            <Line label="Bike Score" value={String(results.risk_data.bike_score)} />
            <Line label="Flood Zone" value={results.risk_data.flood_zone} />
            <Line label="Crime Index" value={`${results.risk_data.crime_index}/100`} />
          </Panel>
          <Panel title="Rental">
            <Line label="Est. Monthly Rent" value={`$${results.financial_data.monthly_rent_est.toLocaleString()}`} />
            <Line label="Annual Gross Rent" value={`$${results.financial_data.annual_gross_rent.toLocaleString()}`} />
            <Line label="Vacancy Rate" value={percent(results.financial_data.vacancy_rate * 100)} />
            <Line label="GRM" value={String(results.financial_data.GRM)} />
          </Panel>
          <Panel title="Zoning">
            <Line label="Zone Code" value={results.zoning_data.zone_code} />
            <Line label="Permitted Uses" value={results.zoning_data.permitted_uses.join(", ")} />
            <Line label="Recent Permits" value={String(results.zoning_data.recent_permits)} />
            <Line label="Restrictions" value={results.zoning_data.restrictions.join(", ")} />
          </Panel>
        </section>
      </div>
    </main>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <article className="rounded-2xl border border-border-green bg-surface p-6">
      <h2 className="font-display text-3xl text-text-primary">{title}</h2>
      <div className="mt-5 space-y-4">{children}</div>
    </article>
  );
}

function Line({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between gap-5 border-b border-border-green pb-3 text-sm">
      <span className="text-text-secondary">{label}</span>
      <span className="max-w-[60%] text-right font-mono text-text-primary">{value}</span>
    </div>
  );
}

