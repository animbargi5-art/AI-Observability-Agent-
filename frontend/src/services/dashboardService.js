import api from "../api/interceptors.js";

class DashboardService {
    constructor() {
        this.baseEndpoint = "/dashboard";
    }

    // Get dashboard statistics
    async getDashboardStats() {
        const response = await api.get(`${this.baseEndpoint}/stats`);
        return response.data;
    }

    // Get investigation status
    async getInvestigationStatus() {
        const response = await api.get(`${this.baseEndpoint}/status`);
        return response.data;
    }

    // Get recent investigations
    async getRecentInvestigations(limit = 5) {
        const response = await api.get(`${this.baseEndpoint}/recent`, {
            params: { limit }
        });
        return response.data;
    }

    // Get system health
    async getSystemHealth() {
        const response = await api.get(`${this.baseEndpoint}/health`);
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