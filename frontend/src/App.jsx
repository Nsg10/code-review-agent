import { useReview } from "./hooks/useReview";
import { UrlInput } from "./components/UrlInput";
import { Dashboard } from "./components/Dashboard";
import { LoadingState } from "./components/LoadingState";
import "./App.css";

function App() {
  const { loading, results, error, reviewRepo, reset, totalReviews } = useReview();

  return (
    <div className="app">
      <section className="hero">
        <div className="badge">
          <span className="badge-dot" />
          4 AI Agents Running in Parallel
        </div>
        <h1 className="hero-title">
          <span className="word-code">Code</span>
          <span className="word-lens">Lens</span>
        </h1>
        <p className="hero-subtitle">
          Paste any public GitHub repository URL and get an instant
          multi-perspective AI code review in seconds.
        </p>
        <div className="agent-pills">
          <span className="pill"><span className="pill-icon">⚙️</span> Code Quality</span>
          <span className="pill"><span className="pill-icon">🐛</span> Bug Detector</span>
          <span className="pill"><span className="pill-icon">⚡</span> Optimizer</span>
          <span className="pill"><span className="pill-icon">🏗️</span> System Design</span>
        </div>
        {totalReviews !== null && (
          <div className="counter-badge">
            <span className="counter-number">{totalReviews.toLocaleString()}</span>
            <span className="counter-label">repositories reviewed</span>
          </div>
        )}
      </section>

      <div className="input-section">
        <UrlInput onSubmit={reviewRepo} loading={loading} />
      </div>

      {error && (
        <div className="error-box">
          <div className="error-inner">{error}</div>
        </div>
      )}

      {loading && <LoadingState />}
      {results && !loading && (
        <Dashboard results={results} onReset={reset} />
      )}

      <footer className="footer">
        Built with LangChain · Groq · FastAPI · React — 4 agents, 0 dollars
      </footer>
    </div>
  );
}

export default App;