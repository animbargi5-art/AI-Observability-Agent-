import { Routes, Route } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import DashboardPage from "../pages/DashboardPage";
import HistoryPage from "../pages/HistoryPage";
import InvestigationPage from "../pages/InvestigationPage";
import SettingsPage from "../pages/SettingsPage";

export default function AppRouter() {

    return (

        <MainLayout>

            <Routes>

                <Route
                    path="/"
                    element={<DashboardPage />}
                />

                <Route
                    path="/history"
                    element={<HistoryPage />}
                />

                <Route
                    path="/settings"
                    element={<SettingsPage />}
                />

                <Route
                    path="/investigation/:id"
                    element={<InvestigationPage />}
                />

            </Routes>

        </MainLayout>

    );

}