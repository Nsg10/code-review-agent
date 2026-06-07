import { useState } from "react";

export function UrlInput({ onSubmit, loading }) {
  const [url, setUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) onSubmit(url.trim());
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-wrapper">
        <span className="input-prefix">github.com/</span>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="username/repository"
          className="url-input"
          disabled={loading}
        />
        <button
          type="submit"
          className="submit-btn"
          disabled={loading || !url.trim()}
        >
          {loading ? "Analysing..." : "Review Repo →"}
        </button>
      </div>
      <p className="input-hint">
        Try: facebook/react · vercel/next.js · golang/go
      </p>
    </form>
  );
}