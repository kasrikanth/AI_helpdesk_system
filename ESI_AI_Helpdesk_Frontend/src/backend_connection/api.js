// api.js


// API Client - HTTP backend communication

import axios from 'axios';
import { getAccessToken } from './auth';

const API_BASE_URL = import.meta.env.BACKEND_API_BASE_URL || 'https://ai-helpdesk-system-vas2.onrender.com';
const API_TIMEOUT = parseInt(import.meta.env.BACKEND_API_TIMEOUT || '20000');

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: API_TIMEOUT,
    headers: {
        'ngrok-skip-browser-warning': 'true',
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

// Request interceptor for logging and auth
apiClient.interceptors.request.use(
    (config) => {
        console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data);
        return config;
    },
    (error) => {
        console.error('[API Request Error]', error);
        return Promise.reject(error);
    }
);

// Response interceptor for logging and error handling
apiClient.interceptors.response.use(
    (response) => {
        console.log(`[API Response] ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data);
        return response;
    },
    (error) => {
        console.error('[API Response Error]', {
            url: error.config?.url,
            status: error.response?.status,
            data: error.response?.data,
            message: error.message,
        });

        if (error.response) {
            const { status, data } = error.response;

            if (status === 500) {
                console.error('Server error:', data);
            } else if (status === 404) {
                console.error('Resource not found:', error.config?.url);
            } else if (status === 400) {
                console.error('Bad request:', data);
            }
        } else if (error.request) {
            console.error('No response from server. Is the backend running?');
        } else {
            console.error('Request setup error:', error.message);
        }

        return Promise.reject(error);
    }
);

export default apiClient;
export { API_BASE_URL };
