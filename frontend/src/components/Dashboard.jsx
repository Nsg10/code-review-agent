import { AgentCard } from "./AgentCard";

export function Dashboard({ results }) {
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <p className="repo-label">Results for:</p>
        <a href={results.repo_url} target="_blank" rel="noopener noreferrer" className="repo-url">
          {results.repo_url}
        </a>
      </div>
      <div className="agents-grid">
        {results.agents.map((item) => (
          <AgentCard key={item.agent} agent={item.agent} result={item.result} />
        ))}
      </div>
    </div>
  );
}
