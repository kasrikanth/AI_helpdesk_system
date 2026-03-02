import apiClient from './api';


// Fetch Metrics Summary
export const fetchMetricsSummary = async () => {
  try {
    const response = await apiClient.get('/metrics/summary');
    return response.data;
  } catch (error) {
    console.error('Error fetching metrics summary:', error);
    throw error;
  }
};

// Fetch Metrics Trends
export const fetchMetricsTrends = async () => {
  try {
    const response = await apiClient.get('/metrics/trends');
    return response.data;
  } catch (error) {
    console.error('Error fetching metrics trends:', error);
    throw error;
  }
};