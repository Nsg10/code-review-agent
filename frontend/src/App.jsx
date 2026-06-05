import { useReview } from "./hooks/useReview";
import { UrlInput } from "./components/UrlInput";
import { Dashboard } from "./components/Dashboard";
import { LoadingState } from "./components/LoadingState";
import "./App.css";

function App() {
  const { loading, results, error, reviewRepo } = useReview();

  return (
    <div className="app">
      <header className="header">
        <h1 className="title">Code Review Agent</h1>
        <p className="subtitle">
          Paste a GitHub repo URL and get instant reviews from 4 AI agents
        </p>
      </header>

      <main className="main">
        <UrlInput onSubmit={reviewRepo} loading={loading} />

        {error && <div className="error-box">{error}</div>}
        {loading && <LoadingState />}
        {results && !loading && <Dashboard results={results} />}
      </main>
    </div>
  );
}

export default App;