export function LoadingState() {
  const agents = [
    { name: "Code Quality", tag: "QUALITY", theme: "theme-quality", icon: "⚙️" },
    { name: "Bug Detector", tag: "BUGS", theme: "theme-bugs", icon: "🐛" },
    { name: "Optimizer", tag: "PERF", theme: "theme-optimizer", icon: "⚡" },
    { name: "System Design", tag: "ARCH", theme: "theme-design", icon: "🏗️" },
  ];

  return (
    <div className="loading-section">
      <div className="loading-header">
        <p className="loading-label">running 4 agents in parallel...</p>
        <div className="loading-bar-track">
          <div className="loading-bar-fill" />
        </div>
      </div>
      <div className="loading-grid">
        {agents.map((agent) => (
          <div key={agent.name} className={`loading-card agent-card ${agent.theme}`}>
            <div className="agent-card-header">
              <div className="agent-card-left">
                <div className="agent-icon-wrap">{agent.icon}</div>
                <span className="agent-name">{agent.name}</span>
              </div>
              <span className="agent-tag">{agent.tag}</span>
            </div>
            <div className="agent-card-body">
              <div className="skeleton skeleton-header" />
              <div className="skeleton skeleton-line" />
              <div className="skeleton skeleton-line medium" />
              <div className="skeleton skeleton-line short" />
              <div className="skeleton skeleton-line" />
              <div className="skeleton skeleton-line medium" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}