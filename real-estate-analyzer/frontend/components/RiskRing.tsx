export default function RiskRing({ score }: { score: number }) {
  const color = score < 30 ? "#63B38A" : score <= 60 ? "#F2A623" : "#E8593C";
  const background = `conic-gradient(${color} ${score * 3.6}deg, #1A2235 0deg)`;
  return (
    <div className="grid place-items-center">
      <div className="grid h-28 w-28 place-items-center rounded-full" style={{ background }}>
        <div className="grid h-20 w-20 place-items-center rounded-full bg-surface">
          <span className="font-display text-3xl text-text-primary">{score}</span>
        </div>
      </div>
    </div>
  );
}

