// ChatbotPerformanceMetrics.jsx

import { fetchMetricsSummary } from '../backend_connection/metrics';

const ChatbotPerformanceMetrics = () => {
  const [summary, setSummary] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    const loadMetrics = async () => {
      try {
        const summaryData = await fetchMetricsSummary();
        setSummary(summaryData);
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
      <h1>Chatbot Performance Metrics</h1>
      <div>Guardrail Activations: {summary.guardrail_activations}</div>
      {/* Render other metrics dynamically */}
    </div>
  );
};