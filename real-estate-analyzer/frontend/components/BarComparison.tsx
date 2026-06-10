type Bar = {
  label: string;
  value: number;
};

export default function BarComparison({ bars }: { bars: Bar[] }) {
  const max = Math.max(...bars.map((bar) => bar.value), 1);
  return (
    <div className="rounded-2xl border border-border-green bg-surface p-6">
      <h2 className="font-display text-2xl text-text-primary">Price Per Square Foot</h2>
      <div className="mt-6 space-y-5">
        {bars.map((bar) => (
          <div key={bar.label}>
            <div className="mb-2 flex justify-between gap-4 text-sm">
              <span className="text-text-secondary">{bar.label}</span>
              <span className="font-mono text-text-primary">${bar.value}/sqft</span>
            </div>
            <div className="h-3 rounded-full bg-surface2">
              <div className="h-3 rounded-full bg-accent" style={{ width: `${Math.max((bar.value / max) * 100, 8)}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

