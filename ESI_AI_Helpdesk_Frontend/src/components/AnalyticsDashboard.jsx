// AnalyticsDashboard.jsx

import { fetchMetricsSummary, fetchMetricsTrends } from '../backend_connection/metrics';

const AnalyticsDashboard = () => {
  const [summary, setSummary] = React.useState(null);
  const [trends, setTrends] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    const loadMetrics = async () => {
      try {
        const [summaryData, trendsData] = await Promise.all([
          fetchMetricsSummary(),
          fetchMetricsTrends(),
        ]);
        setSummary(summaryData);
        setTrends(trendsData);
      } catch (err) {
        setError('Failed to load metrics');
      } finally {
        setLoading(false);
      }
    };

    loadMetrics();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>Analytics Dashboard</h1>
      <div>Total Conversations: {summary.total_conversations}</div>
      <div>Total Tickets: {summary.total_tickets}</div>
      {/* Render charts dynamically using trends */}
    </div>
  );
};

export default AnalyticsDashboard;