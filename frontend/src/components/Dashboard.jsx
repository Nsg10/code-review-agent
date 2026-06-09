import { useEffect, useRef } from "react";
import { AgentCard } from "./AgentCard";

export function Dashboard({ results, onReset }) {
  const ref = useRef(null);

  useEffect(() => {
    ref.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [results]);

  return (
    <div className="results-section" ref={ref}>
      <div className="results-header">
        <span className="results-title">review complete — 4 agents</span>
        <div className="results-header-right">
          <a href={results.repo_url} target="_blank" rel="noopener noreferrer" className="results-repo-link">
            {results.repo_url.replace("https://github.com/", "")}
          </a>
          <button className="new-review-btn" onClick={onReset}>New Review</button>
        </div>
      </div>
      <div className="agents-grid">
        {results.agents.map((item, i) => (
          <AgentCard key={item.agent} agent={item.agent} result={item.result} index={i} repoUrl={results.repo_url} />
        ))}
      </div>
    </div>
  );
}
