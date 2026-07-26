import { Routes, Route, Navigate } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import DashboardPage from "../pages/DashboardPage";
import HistoryPage from "../pages/HistoryPage";
import InvestigationPage from "../pages/InvestigationPage";
import SettingsPage from "../pages/SettingsPage";
import ReportsPage from "../pages/ReportPage";

export default function AppRouter() {
    return (
        <MainLayout>
            <Routes>
                {/* Root route redirects to dashboard */}
                <Route 
                    path="/" 
                    element={<Navigate to="/dashboard" replace />} 
                />
                
                {/* Main application routes */}
                <Route 
                    path="/dashboard" 
                    element={<DashboardPage />} 
                />
                
                <Route 
                    path="/history" 
                    element={<HistoryPage />} 
                />
                
                <Route 
                    path="/reports" 
                    element={<ReportsPage />} 
                />
                
                <Route 
                    path="/settings" 
                    element={<SettingsPage />} 
                />
                
                <Route 
                    path="/investigation/:id" 
                    element={<InvestigationPage />} 
                />
                
                {/* Future routes - placeholders for upcoming features */}
                <Route 
                    path="/notifications" 
                    element={<Navigate to="/dashboard" replace />} 
                />
                
                <Route 
                    path="/live-monitoring" 
                    element={<Navigate to="/dashboard" replace />} 
                />
                
                <Route 
                    path="/knowledge-graph" 
                    element={<Navigate to="/dashboard" replace />} 
                />
                
                <Route 
                    path="/ai-assistant" 
                    element={<Navigate to="/dashboard" replace />} 
                />
                
                {/* Catch all route - redirect to dashboard */}
                <Route 
                    path="*" 
                    element={<Navigate to="/dashboard" replace />} 
                />
            </Routes>
        </MainLayout>
    );
}