export function AgentCard({ agent, result }) {
  const icons = {
    "Code Quality": "⚙️",
    "Bug Detector": "🐛",
    "Optimizer": "⚡",
    "System Design": "🏗️",
  };

  const colors = {
    "Code Quality": "#4f46e5",
    "Bug Detector": "#dc2626",
    "Optimizer": "#d97706",
    "System Design": "#059669",
  };

  return (
    <div className="agent-card" style={{ borderTopColor: colors[agent] }}>
      <div className="agent-header">
        <span className="agent-icon">{icons[agent]}</span>
        <h3 className="agent-title" style={{ color: colors[agent] }}>
          {agent}
        </h3>
      </div>
      <pre className="agent-result">{result}</pre>
    </div>
  );
}