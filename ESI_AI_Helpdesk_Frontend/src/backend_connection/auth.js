// backend_connection/auth.js


// Auth

import apiClient from './api';
import { jwtDecode } from "jwt-decode";

/**
 * Login with email and password
 *
 * @param {string} email
 * @param {string} password
 * @returns {Promise<object>}
 */

export const login = async (email, password) => {
    try {
        const response = await apiClient.post('/auth/login', {
            email,
            password
        });

        const { access_token, session_id } = response.data;

        localStorage.setItem('access_token', access_token);
        localStorage.setItem('session_id', session_id);

        // Decode token to get role info
        const decoded = jwtDecode(access_token);

        const user = {
            id: decoded.sub,
            role: decoded.role,
            role_level: decoded.role_level
        };

        localStorage.setItem('user', JSON.stringify(user));

        return {
            success: true,
            user
        };

    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.detail || "Login failed"
        };
    }
};

export const getAccessToken = () => {
    return localStorage.getItem('access_token');
};

export const getSessionId = () => {
    return localStorage.getItem('session_id');
};

// Logout - clear stored tokens

export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('session_id');
};


//  * Check if user is authenticate
export const isAuthenticated = () => {
    return !!localStorage.getItem('access_token');
};

export const getStoredUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};

export default {
    login,
    logout,
    getAccessToken,
    getSessionId,
    isAuthenticated,
};
