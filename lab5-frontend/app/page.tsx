"use client";

import { useState } from "react";
import { useCompletion } from "@ai-sdk/react";

export default function Page() {
  const [error, setError] = useState<string | null>(null);

  const {
    completion,
    complete,
    isLoading,
    error: completionError,
    input,
    handleInputChange,
  } = useCompletion({
    api: "/api/summarize",
    streamProtocol: "text",
    onError: (err) => {
      setError(err.message);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const trimmed = input.trim();
    if (!trimmed) {
      setError("Please enter some text to summarize.");
      return;
    }

    complete(trimmed);
  };

  const displayError = error ?? completionError?.message ?? null;

  return (
    <main style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "1rem" }}>Summarization</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="input-text" style={{ display: "block", marginBottom: "0.5rem" }}>
            Input text
          </label>
          <textarea
            id="input-text"
            value={input}
            onChange={handleInputChange}
            rows={6}
            disabled={isLoading}
            style={{
              width: "100%",
              padding: "0.5rem",
              fontFamily: "inherit",
            }}
            placeholder="Enter text to summarize..."
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          style={{
            padding: "0.5rem 1rem",
            cursor: isLoading ? "not-allowed" : "pointer",
            opacity: isLoading ? 0.7 : 1,
          }}
        >
          {isLoading ? "Generating…" : "Generate Summary"}
        </button>
      </form>

      {displayError && (
        <div
          role="alert"
          style={{
            marginTop: "1rem",
            padding: "0.75rem",
            backgroundColor: "#fee",
            color: "#c00",
            borderRadius: "4px",
          }}
        >
          {displayError}
        </div>
      )}

      <div style={{ marginTop: "1rem" }}>
        <h2 style={{ marginBottom: "0.5rem", fontSize: "1.1rem" }}>Summary</h2>
        <div
          style={{
            padding: "1rem",
            backgroundColor: "#f5f5f5",
            borderRadius: "4px",
            whiteSpace: "pre-wrap",
            minHeight: "4rem",
          }}
        >
          {completion || "(Summary will appear here)"}
        </div>
      </div>
    </main>
  );
}
