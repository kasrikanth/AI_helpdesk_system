// Ticket Service - API integration for ticket management

import apiClient from './api';

//  Get tickets with filters (optional filter)
export const getTickets = async (filters = {}) => {
    try {
        const { data } = await apiClient.get('/tickets/', {
            params: {
                status: filters.status,
                tier: filters.tier,
                severity: filters.severity,
                limit: 50,
            },
        });

        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
};


// Get single ticket
export const getTicketById = async (ticketId) => {
    try {
        const { data } = await apiClient.get(`/tickets/${ticketId}`);
        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
};


// Update ticket
export const updateTicket = async (ticketId, updateData) => {
    try {
        const { data } = await apiClient.patch(
            `/tickets/update/${ticketId}`,
            updateData
        );

        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
};


export default {
    getTickets,
    getTicketById,
    updateTicket,
};