export function ScoreRing({ score }) {
  const isNumber = typeof score === "number";
  const pct = isNumber ? (score / 10) * 100 : null;

  const radius = 28;
  const circumference = 2 * Math.PI * radius;
  const offset = pct !== null ? circumference - (pct / 100) * circumference : 0;

  const color =
    !isNumber ? "#8b5cf6"
    : score >= 8 ? "#3fb950"
    : score >= 6 ? "#d29922"
    : "#f85149";

  const severityColor =
    typeof score === "string"
      ? score === "High" ? "#f85149"
      : score === "Medium" ? "#d29922"
      : "#3fb950"
      : color;

  if (!isNumber) {
    return (
      <div className="score-badge" style={{ background: `${severityColor}18`, border: `1px solid ${severityColor}40` }}>
        <span style={{ color: severityColor, fontSize: "12px", fontWeight: 600 }}>
          {score}
        </span>
      </div>
    );
  }

  return (
    <div className="score-ring-wrap">
      <svg width="72" height="72" viewBox="0 0 72 72">
        <circle
          cx="36" cy="36" r={radius}
          fill="none"
          stroke="#21262d"
          strokeWidth="5"
        />
        <circle
          cx="36" cy="36" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="5"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 36 36)"
          style={{ transition: "stroke-dashoffset 1s ease" }}
        />
      </svg>
      <div className="score-ring-label">
        <span className="score-number" style={{ color }}>{score}</span>
        <span className="score-denom">/10</span>
      </div>
    </div>
  );
}