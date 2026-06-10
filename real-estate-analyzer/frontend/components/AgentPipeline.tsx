import type { AgentLog } from "@/lib/types";

const colors: Record<string, string> = {
  "Market Agent": "bg-blue",
  "Financial Agent": "bg-accent",
  "Zoning Agent": "bg-amber",
  "Risk Agent": "bg-coral",
  "Report Agent": "bg-accent"
};

export default function AgentPipeline({ agents }: { agents: AgentLog[] }) {
  return (
    <div className="grid gap-4 lg:grid-cols-5">
      {agents.map((agent) => {
        const running = agent.status === "running";
        const done = agent.status === "done";
        return (
          <article key={agent.name} className="rounded-xl border border-border-green bg-surface p-5">
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-3">
                <span className={`h-3 w-3 rounded-full ${colors[agent.name] ?? "bg-text-muted"} ${running ? "animate-pulse" : ""}`} />
                <h2 className="font-semibold text-text-primary">{agent.name}</h2>
              </div>
              <span className="rounded-full border border-border-green px-3 py-1 font-mono text-[11px] uppercase text-text-secondary">
                {done ? "Done" : running ? "Running" : agent.status === "failed" ? "Failed" : "Waiting"}
              </span>
            </div>
            <p className="mt-4 min-h-12 text-sm leading-6 text-text-secondary">{agent.log}</p>
            <div className="mt-5 h-2 overflow-hidden rounded-full bg-surface2">
              <div className={`h-full rounded-full ${done ? "w-full bg-accent" : running ? "w-2/3 animate-pulse bg-accent" : "w-2 bg-text-muted"}`} />
            </div>
            <p className="mt-3 font-mono text-xs text-text-muted">{done ? `${agent.duration}s` : done ? "Complete" : "Queued"}</p>
          </article>
        );
      })}
    </div>
  );
}

