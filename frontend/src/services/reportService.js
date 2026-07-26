import api from "../api/interceptors.js";

class ReportService {
    constructor() {
        this.baseEndpoint = "/reports";
    }

    // Get overall statistics
    async getOverallStats(dateRange = {}) {
        const params = new URLSearchParams();
        if (dateRange.from) params.append('date_from', dateRange.from);
        if (dateRange.to) params.append('date_to', dateRange.to);

        const url = params.toString() ? `${this.baseEndpoint}/stats?${params}` : `${this.baseEndpoint}/stats`;
        const response = await api.get(url);
        return response.data;
    }

    // Get severity distribution data
    async getSeverityDistribution(dateRange = {}) {
        const params = new URLSearchParams();
        if (dateRange.from) params.append('date_from', dateRange.from);
        if (dateRange.to) params.append('date_to', dateRange.to);

        const url = params.toString() ? `${this.baseEndpoint}/severity?${params}` : `${this.baseEndpoint}/severity`;
        const response = await api.get(url);
        return response.data;
    }

    // Get status distribution data
    async getStatusDistribution(dateRange = {}) {
        const params = new URLSearchParams();
        if (dateRange.from) params.append('date_from', dateRange.from);
        if (dateRange.to) params.append('date_to', dateRange.to);

        const url = params.toString() ? `${this.baseEndpoint}/status?${params}` : `${this.baseEndpoint}/status`;
        const response = await api.get(url);
        return response.data;
    }

    // Get trend data
    async getTrendData(period = '7d', dateRange = {}) {
        const params = new URLSearchParams();
        params.append('period', period);
        if (dateRange.from) params.append('date_from', dateRange.from);
        if (dateRange.to) params.append('date_to', dateRange.to);

        const response = await api.get(`${this.baseEndpoint}/trends?${params}`);
        return response.data;
    }

    // Get performance metrics
    async getPerformanceMetrics(dateRange = {}) {
        const params = new URLSearchParams();
        if (dateRange.from) params.append('date_from', dateRange.from);
        if (dateRange.to) params.append('date_to', dateRange.to);

        const url = params.toString() ? `${this.baseEndpoint}/performance?${params}` : `${this.baseEndpoint}/performance`;
        const response = await api.get(url);
        return response.data;
    }

    // Get AI agent performance data
    async getAgentPerformance(dateRange = {}) {
        const params = new URLSearchParams();
        if (dateRange.from) params.append('date_from', dateRange.from);
        if (dateRange.to) params.append('date_to', dateRange.to);

        const url = params.toString() ? `${this.baseEndpoint}/agents?${params}` : `${this.baseEndpoint}/agents`;
        const response = await api.get(url);
        return response.data;
    }

    // Export reports
    async exportReport(reportType, format = 'pdf', params = {}) {
        const queryParams = new URLSearchParams(params);
        queryParams.append('format', format);

        const response = await api.get(`${this.baseEndpoint}/${reportType}/export?${queryParams}`, {
            responseType: 'blob'
        });
        return response.data;
    }

    // Generate custom report
    async generateCustomReport(reportConfig) {
        const response = await api.post(`${this.baseEndpoint}/custom`, reportConfig);
        return response.data;
    }
}

export default new ReportService();