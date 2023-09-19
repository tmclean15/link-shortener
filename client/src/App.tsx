import React, { useState } from "react";
import "./App.css";

const apiUrl = process.env.REACT_APP_API_URL;

const App: React.FC = () => {
  const [url, setUrl] = useState<string>("");
  const [shortenedUrl, setShortenedUrl] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch(`${apiUrl}/shorten`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `url=${encodeURIComponent(url)}`,
      });

      if (response.ok) {
        const data = await response.json();
        setShortenedUrl(data.short_url);
      } else {
        alert("Error shortening the URL!");
      }
    } catch (error) {
      console.error("There was an error:", error);
    }
  };

  return (
    <div className="App">
      <h1>Link Shortener</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter your URL:
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
        </label>
        <button type="submit">Shorten</button>
      </form>
      {shortenedUrl && (
        <div>
          <p>
            Shortened URL: <a href={shortenedUrl}>{shortenedUrl}</a>
          </p>
        </div>
      )}
    </div>
  );
};

export default App;
