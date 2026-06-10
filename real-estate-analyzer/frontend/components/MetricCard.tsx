type MetricCardProps = {
  label: string;
  value: string;
  tone?: "green" | "amber" | "red" | "neutral";
  helper?: string;
};

const toneClass: Record<NonNullable<MetricCardProps["tone"]>, string> = {
  green: "text-accent",
  amber: "text-amber",
  red: "text-coral",
  neutral: "text-text-primary"
};

export default function MetricCard({ label, value, tone = "neutral", helper }: MetricCardProps) {
  return (
    <article className="rounded-xl border border-border-green bg-surface p-6">
      <p className="font-mono text-xs uppercase text-text-secondary">{label}</p>
      <p className={`mt-3 font-display text-5xl ${toneClass[tone]}`}>{value}</p>
      {helper ? <p className="mt-3 text-sm text-text-secondary">{helper}</p> : null}
    </article>
  );
}

