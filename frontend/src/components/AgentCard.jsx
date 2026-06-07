import { useState } from "react";
import { ScoreRing } from "./ScoreRing";
import { parseAgentResult } from "../utils/parseResult";

const AGENT_CONFIG = {
  "Code Quality": { icon: "⚙️", theme: "theme-quality", tag: "QUALITY" },
  "Bug Detector": { icon: "🐛", theme: "theme-bugs", tag: "BUGS" },
  "Optimizer":    { icon: "⚡", theme: "theme-optimizer", tag: "PERF" },
  "System Design":{ icon: "🏗️", theme: "theme-design", tag: "ARCH" },
};

export function AgentCard({ agent, result, index }) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);
  const config = AGENT_CONFIG[agent] || { icon: "🤖", theme: "", tag: "AI" };
  const parsed = parseAgentResult(result);

  const handleCopy = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className={`agent-card ${config.theme}`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <div className="agent-card-header">
        <div className="agent-card-left">
          <div className="agent-icon-wrap">{config.icon}</div>
          <span className="agent-name">{agent}</span>
        </div>
        <div className="agent-card-right">
          <button className="copy-btn" onClick={handleCopy}>
            {copied ? "✓ Copied" : "Copy"}
          </button>
          <span className="agent-tag">{config.tag}</span>
        </div>
      </div>

      <div className="agent-card-body">
        {parsed.score !== null && (
          <div className="score-row">
            <ScoreRing score={parsed.score} />
            {parsed.summary && (
              <p className="summary-text">{parsed.summary}</p>
            )}
          </div>
        )}

        {!parsed.score && parsed.summary && (
          <p className="summary-text summary-only">{parsed.summary}</p>
        )}

        {parsed.sections.length > 0 && (
          <div className={`sections-wrap ${expanded ? "expanded" : ""}`}>
            {parsed.sections.map((section) => (
              <div key={section.title} className="section-block">
                <p className="section-title">{section.title}</p>
                <ul className="section-list">
                  {section.items.map((item, i) => (
                    <li key={i} className="section-item">{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        {parsed.sections.length > 0 && (
          <button
            className="expand-btn"
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? "Show less ↑" : "Show full review ↓"}
          </button>
        )}
      </div>
    </div>
  );
}
