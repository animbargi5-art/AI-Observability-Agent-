import api from "../api/interceptors.js";

class DashboardService {
    constructor() {
        this.baseEndpoint = "/dashboard";
    }

    // Get dashboard statistics
    async getDashboardStats() {
        const response = await api.get(`${this.baseEndpoint}/statistics`);
        return response.data;
    }

    // Get investigation status
    async getInvestigationStatus() {
        // Investigations run synchronously today. Keep a stable UI contract
        // until the backend exposes a persisted progress endpoint.
        return { status: 'idle' };
    }

    // Get recent investigations
    async getRecentInvestigations(limit = 5) {
        const response = await api.get(`${this.baseEndpoint}/recent`, {
            params: { limit }
        });
        return response.data.investigations ?? [];
    }

    // Get system health
    async getSystemHealth() {
        const response = await api.get(`${this.baseEndpoint}/health-overview`);
        return response.data;
    }

    // Get backend connection status
    async getBackendStatus() {
        const response = await api.get("/health");
        return response.data;
    }

    // Get SigNoz connection status
    async getSigNozStatus() {
        const response = await api.get(`${this.baseEndpoint}/signoz-status`);
        return response.data;
    }
}

export default new DashboardService();
