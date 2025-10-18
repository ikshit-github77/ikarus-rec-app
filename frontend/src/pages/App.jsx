import React, { useState } from "react";

// --- small helpers for badges + currency ---
const Badge = ({ children, bg = "#f5f5f5", fg = "#444" }) => (
  <span
    style={{
      display: "inline-block",
      padding: "2px 8px",
      borderRadius: 999,
      fontSize: 12,
      background: bg,
      color: fg,
      lineHeight: "18px",
    }}
  >
    {children}
  </span>
);

const formatINR = (v) => {
  if (v === null || v === undefined || isNaN(Number(v))) return null;
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(v));
};

export default function App() {
  const [query, setQuery] = useState("");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function submit(e) {
    e.preventDefault();
    setErr("");
    setItems([]);
    const q = query.trim();
    if (!q) {
      setErr("Type what you’re looking for (e.g., chair under 150).");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, top_k: 5 }),
      });
      if (!res.ok) {
        const t = await res.text();
        throw new Error(t || `Request failed (${res.status})`);
      }
      const data = await res.json();
      setItems(Array.isArray(data.items) ? data.items : []);
    } catch (e) {
      setErr(e.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 20, maxWidth: 960, margin: "0 auto" }}>
      <h2 style={{ marginBottom: 10 }}>Furniture Recommender</h2>
      <p style={{ color: "#555", marginTop: 0, marginBottom: 16 }}>
        Describe what you need; we’ll find close matches and write a short blurb.
      </p>

      <form onSubmit={submit} style={{ display: "flex", gap: 10, marginBottom: 12 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. modern wooden chair under 150 • compact desk for small room • matte black bathroom faucet"
          style={{
            flex: 1,
            padding: "10px 12px",
            border: "1px solid #ddd",
            borderRadius: 8,
            outline: "none",
          }}
        />
        <button
          disabled={loading}
          style={{
            padding: "10px 14px",
            borderRadius: 8,
            border: "1px solid #0a66c2",
            background: loading ? "#9cc6f3" : "#0a66c2",
            color: "white",
            cursor: loading ? "not-allowed" : "pointer",
            minWidth: 110,
          }}
        >
          {loading ? "Finding..." : "Recommend"}
        </button>
      </form>

      {err && (
        <div
          style={{
            background: "#fff2f2",
            color: "#b42318",
            border: "1px solid #f3c5c5",
            borderRadius: 8,
            padding: "8px 10px",
            marginBottom: 12,
          }}
        >
          {err}
        </div>
      )}

      {/* results */}
      <div style={{ marginTop: 8 }}>
        {items.length === 0 && !loading && !err && (
          <div style={{ color: "#666", fontSize: 14 }}>
            Try: <em>“lightweight study table under 3000”</em> or{" "}
            <em>“oak finish dining chairs under 150”</em>.
          </div>
        )}

        {items.map((it, idx) => (
          <div
            key={idx}
            style={{
              border: "1px solid #eee",
              borderRadius: 12,
              padding: 14,
              marginBottom: 12,
              boxShadow: "0 1px 2px rgba(0,0,0,0.03)",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                gap: 10,
                alignItems: "start",
              }}
            >
              <div style={{ fontWeight: 600, fontSize: 16, lineHeight: "22px" }}>
                {it.title || "Untitled item"}
              </div>
              <div style={{ whiteSpace: "nowrap", fontWeight: 600 }}>
                {formatINR(it.price) || ""}
              </div>
            </div>

            {/* badges row */}
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", margin: "8px 0 6px" }}>
              {formatINR(it.price) && <Badge bg="#eef6ff" fg="#165fb3">{formatINR(it.price)}</Badge>}
              {it.categories && it.categories.trim() !== "" && (
                <Badge bg="#f5f5f5" fg="#444">{it.categories}</Badge>
              )}
              {it.brand && it.brand.trim() !== "" && (
                <Badge bg="#fff7ed" fg="#9a3412">{it.brand}</Badge>
              )}
            </div>

            {/* short GenAI blurb */}
            {it.gen_copy && (
              <p style={{ marginTop: 6, lineHeight: 1.5, color: "#333" }}>{it.gen_copy}</p>
            )}

            {/* optional: small meta row */}
            <div style={{ marginTop: 6, color: "#777", fontSize: 12 }}>
              {it.color ? `Color: ${it.color}` : null}
              {it.material ? ` • Material: ${it.material}` : null}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
