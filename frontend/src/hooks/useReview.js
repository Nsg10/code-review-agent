import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export function useReview() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [totalReviews, setTotalReviews] = useState(null);

  useEffect(() => {
    axios.get(`${API_URL}/stats`)
      .then((res) => setTotalReviews(res.data.total_reviews))
      .catch(() => {});
  }, []);

  const reviewRepo = async (repoUrl) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post(`${API_URL}/review`, {
        repo_url: repoUrl,
      });
      setResults(response.data);
      setTotalReviews(response.data.total_reviews);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResults(null);
    setError(null);
    setLoading(false);
  };

  return { loading, results, error, reviewRepo, reset, totalReviews };
}