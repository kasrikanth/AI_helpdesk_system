import React, { useEffect, useState } from "react";
import { fetchMetricsSummary, fetchMetricsTrends } from "../backend_connection/metrics";
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, Cell
} from "recharts";

// ── Color Palette ─────────────────────────────────────────────────────────────
const YELLOW       = "#FFD600";
const ORANGE       = "#FFA000";
const DEEP_ORANGE  = "#FF6F00";
const AMBER        = "#FFCA28";
const BG_PAGE      = "#111111";
const BG_CARD      = "#1A1A1A";
const BG_CARD_DARK = "#161616";
const BORDER       = "rgba(255,214,0,0.18)";
const PIE_COLORS   = [YELLOW, ORANGE, DEEP_ORANGE, AMBER, "#FFE57F", "#FF8F00"];

// ── Tooltip style ─────────────────────────────────────────────────────────────
const tooltipStyle = {
  contentStyle: { backgroundColor: "#1e1e1e", border: `1px solid ${YELLOW}`, borderRadius: 8 },
  labelStyle:   { color: YELLOW },
  itemStyle:    { color: "#fff" },
};

// ── KPI Card ──────────────────────────────────────────────────────────────────
const KpiCard = ({ title, value, accent }) => (
  <div style={{
    flex: "1 1 0",
    minWidth: 140,
    background: BG_CARD,
    border: `1px solid ${accent}44`,
    borderTop: `3px solid ${accent}`,
    borderRadius: 14,
    padding: "22px 16px",
    textAlign: "center",
    boxShadow: `0 4px 20px ${accent}18`,
    transition: "transform 0.2s, box-shadow 0.2s",
    cursor: "default",
  }}
  onMouseEnter={e => { e.currentTarget.style.transform = "translateY(-5px)"; e.currentTarget.style.boxShadow = `0 10px 30px ${accent}35`; }}
  onMouseLeave={e => { e.currentTarget.style.transform = "translateY(0)";   e.currentTarget.style.boxShadow = `0 4px 20px ${accent}18`; }}
  >
    <p style={{ margin: "0 0 10px", fontSize: 12, color: "#888", textTransform: "uppercase", letterSpacing: 1 }}>{title}</p>
    <p style={{ margin: 0, fontSize: 32, fontWeight: 800, color: accent }}>{value}</p>
  </div>
);

// ── Section / Chart Card ──────────────────────────────────────────────────────
const ChartCard = ({ title, children, accent = YELLOW }) => (
  <div style={{
    background: BG_CARD,
    border: `1px solid ${BORDER}`,
    borderRadius: 14,
    padding: "24px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.4)",
    transition: "box-shadow 0.3s",
  }}
  onMouseEnter={e => e.currentTarget.style.boxShadow = `0 8px 32px ${accent}28`}
  onMouseLeave={e => e.currentTarget.style.boxShadow = "0 4px 20px rgba(0,0,0,0.4)"}
  >
    <h3 style={{ margin: "0 0 20px", fontSize: 16, fontWeight: 700, color: accent, letterSpacing: 0.5 }}>
      {title}
    </h3>
    {children}
  </div>
);

// ── Main Page ─────────────────────────────────────────────────────────────────
const AnalyticsPage = () => {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends]   = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      const [s, t] = await Promise.all([fetchMetricsSummary(), fetchMetricsTrends()]);
      setSummary(s);
      setTrends(t);
      setLoading(false);
    };
    load();
  }, []);

  if (loading) return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", background: BG_PAGE }}>
      <div style={{ width: 48, height: 48, border: `4px solid ${YELLOW}`, borderTopColor: "transparent", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );

  // ── Data transforms ───────────────────────────────────────────────────────
  const tierData = Object.entries(summary.tickets_by_tier || {}).map(([k, v]) => ({ name: k, value: v }));
  const severityData = Object.entries(summary.tickets_by_severity || {}).map(([k, v]) => ({ name: k, value: v }));
  const conversationTrend = trends.conversation_volume.map(i => ({ date: new Date(i.start_date).toLocaleDateString(), value: i.value }));
  const ticketTrend       = trends.ticket_volume.map(i => ({ date: new Date(i.start_date).toLocaleDateString(), value: i.value }));
  const guardrailTrend    = trends.guardrail_activations.map(i => ({ date: new Date(i.start_date).toLocaleDateString(), value: i.value }));

  // ── KPIs ──────────────────────────────────────────────────────────────────
  const kpis = [
    { title: "Total Conversations", value: summary.total_conversations,                       accent: YELLOW },
    { title: "Total Tickets",       value: summary.total_tickets,                              accent: ORANGE },
    { title: "Deflection Rate",     value: `${summary.deflection_rate}%`,                     accent: "#4FC3F7" },
    { title: "Avg Confidence",      value: `${(summary.avg_confidence * 100).toFixed(1)}%`,   accent: "#81C784" },
    { title: "Guardrails",          value: summary.guardrail_activations,                      accent: "#CE93D8" },
  ];

  // ── Shared axis/grid props ────────────────────────────────────────────────
  const axisStyle  = { fontSize: 11, fill: "#888" };
  const gridStyle  = { strokeDasharray: "3 3", stroke: "#2a2a2a" };

  return (
    <div style={{ background: BG_PAGE, minHeight: "100vh", padding: "32px 40px", fontFamily: "'Segoe UI', Arial, sans-serif", boxSizing: "border-box" }}>

      {/* ── Title ── */}
      <h1 style={{ margin: "0 0 32px", fontSize: 28, fontWeight: 800, color: YELLOW, letterSpacing: 0.5 }}>
        📊 Analytics Dashboard
      </h1>

      {/* ── KPI Row ── */}
      <div style={{ display: "flex", gap: 20, marginBottom: 40, flexWrap: "wrap" }}>
        {kpis.map(k => <KpiCard key={k.title} {...k} />)}
      </div>

      {/* ── Row 1: Line + Bar ── */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 24 }}>
        <ChartCard title="📈 Conversation Trend" accent={YELLOW}>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={conversationTrend}>
              <CartesianGrid {...gridStyle} />
              <XAxis dataKey="date" tick={axisStyle} stroke="#444" />
              <YAxis tick={axisStyle} stroke="#444" />
              <Tooltip {...tooltipStyle} />
              <Legend wrapperStyle={{ color: "#aaa", fontSize: 12 }} />
              <Line type="monotone" dataKey="value" stroke={YELLOW} strokeWidth={3} dot={{ r: 5, fill: YELLOW, strokeWidth: 0 }} activeDot={{ r: 7 }} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="🎫 Ticket Trend" accent={ORANGE}>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={ticketTrend}>
              <CartesianGrid {...gridStyle} />
              <XAxis dataKey="date" tick={axisStyle} stroke="#444" />
              <YAxis tick={axisStyle} stroke="#444" />
              <Tooltip {...tooltipStyle} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {ticketTrend.map((_, i) => (
                  <Cell key={i} fill={i % 2 === 0 ? ORANGE : YELLOW} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* ── Row 2: Guardrail + Pie row ── */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 24 }}>
        <ChartCard title="🛡 Guardrail Activations" accent="#CE93D8">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={guardrailTrend}>
              <CartesianGrid {...gridStyle} />
              <XAxis dataKey="date" tick={axisStyle} stroke="#444" />
              <YAxis tick={axisStyle} stroke="#444" />
              <Tooltip {...tooltipStyle} />
              <Line type="monotone" dataKey="value" stroke="#CE93D8" strokeWidth={3} dot={{ r: 5, fill: "#CE93D8", strokeWidth: 0 }} activeDot={{ r: 7 }} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* ── Pie Row inside right column ── */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <ChartCard title="🎫 Tickets by Tier" accent={AMBER}>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={tierData} dataKey="value" nameKey="name" outerRadius={90} cx="50%" cy="50%"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  labelLine={{ stroke: "#555" }}
                >
                  {tierData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                </Pie>
                <Tooltip {...tooltipStyle} />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="⚠ Tickets by Severity" accent="#FF8A65">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={severityData} dataKey="value" nameKey="name" outerRadius={90} cx="50%" cy="50%"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  labelLine={{ stroke: "#555" }}
                >
                  {severityData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                </Pie>
                <Tooltip {...tooltipStyle} />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>
      </div>

    </div>
  );
};

export default AnalyticsPage;