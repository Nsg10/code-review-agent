export function LoadingState() {
  const agents = ["Code Quality", "Bug Detector", "Optimizer", "System Design"];

  return (
    <div className="loading-container">
      <p className="loading-text">Running 4 agents in parallel...</p>
      <div className="loading-grid">
        {agents.map((agent) => (
          <div key={agent} className="loading-card">
            <div className="skeleton skeleton-title" />
            <div className="skeleton skeleton-line" />
            <div className="skeleton skeleton-line" />
            <div className="skeleton skeleton-line short" />
          </div>
        ))}
      </div>
    </div>
  );
}