import { useState } from "react";

export function UrlInput({ onSubmit, loading }) {
  const [url, setUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) onSubmit(url.trim());
  };

  return (
    <div className="url-input-container">
      <form onSubmit={handleSubmit} className="url-form">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://github.com/username/repo"
          className="url-input"
          disabled={loading}
        />
        <button type="submit" className="submit-btn" disabled={loading || !url.trim()}>
          {loading ? "Analysing..." : "Review Repo"}
        </button>
      </form>
    </div>
  );
}