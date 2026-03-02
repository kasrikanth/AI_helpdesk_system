import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
} from '@mui/material';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';

import {
  fetchMetricsSummary,
  fetchMetricsTrends,
} from '../backend_connection/metrics';

const MetricsDashboard = () => {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  
  useEffect(() => {
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
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Grid container spacing={3}>
      
      {/* SUMMARY CARDS */}
      <Grid item xs={12} md={3}>
        <MetricCard title="Total Conversations" value={summary.total_conversations} />
      </Grid>

      <Grid item xs={12} md={3}>
        <MetricCard title="Total Tickets" value={summary.total_tickets} />
      </Grid>

      <Grid item xs={12} md={3}>
        <MetricCard title="Deflection Rate" value={`${summary.deflection_rate}%`} />
      </Grid>

      <Grid item xs={12} md={3}>
        <MetricCard title="Avg Confidence" value={summary.avg_confidence} />
      </Grid>

      {/* CONVERSATION TREND */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Conversation Volume Trend
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={trends.conversation_volume}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="start_date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#1976d2" />
          </LineChart>
        </ResponsiveContainer>
      </Grid>

      {/* TICKET TREND */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Ticket Volume Trend
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={trends.ticket_volume}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="start_date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#d32f2f" />
          </LineChart>
        </ResponsiveContainer>
      </Grid>

    </Grid>
  );
};

const MetricCard = ({ title, value }) => (
  <Card>
    <CardContent>
      <Typography variant="subtitle2" color="textSecondary">
        {title}
      </Typography>
      <Typography variant="h5">{value}</Typography>
    </CardContent>
  </Card>
);

export default MetricsDashboard;