type Verdict = "Favorable" | "Proceed with Caution" | "High Risk";

const borderClass: Record<Verdict, string> = {
  Favorable: "border-l-accent",
  "Proceed with Caution": "border-l-amber",
  "High Risk": "border-l-coral"
};

export default function VerdictBox({ verdict, text }: { verdict: Verdict; text: string }) {
  return (
    <div className={`h-full rounded-2xl border border-l-4 border-border-green ${borderClass[verdict]} bg-surface p-6`}>
      <p className="font-mono text-xs uppercase text-text-secondary">AI Verdict</p>
      <h2 className="mt-3 font-display text-4xl text-text-primary">{verdict}</h2>
      <p className="mt-4 leading-7 text-text-secondary">{text}</p>
    </div>
  );
}

