import apiClient from './api';

export const sendMessage = async (message, context = {}) => {
    try {
        const sessionId = localStorage.getItem('session_id');

        if (!sessionId) {
            return {
                success: false,
                error: "session deactivated. login again."
            };
        }

        const requestData = {
            sessionId: sessionId,
            message: message,
            context: context,
        };

        const response = await apiClient.post('/api/chat', requestData);

        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.detail || error.message,
            status: error.response?.status,
        };
    }
};
export const formatChatResponse = (backendResponse = {}) => {
    const {
        answer,
        kbReferences,
        confidence,
        tier,
        severity,
        needsEscalation,
        guardrail,
        ticket_id,
    } = backendResponse;

    return {
        message: answer,
        kbReferences: Array.isArray(kbReferences)
            ? kbReferences.map(({ id, title, excerpt }) => ({
                  id,
                  title,
                  excerpt,
              }))
            : [],
        confidence,
        tier,
        severity,
        needsEscalation,
        guardrail,
        ticketId: ticket_id,
    };
};

export default {
    sendMessage,
    formatChatResponse,
};

