import { useEffect, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { ProgressSpinner } from "primereact/progressspinner";
import { Skeleton } from "primereact/skeleton";
import { Message } from "primereact/message";

import investigationService from "../services/investigationService";
import dashboardService from "../services/dashboardService";

import DashboardHeader from "../components/Dashboard/DashboardHeader";
import InvestigationList from "../components/Dashboard/InvestigationList";
import StatisticsCards from "../components/Dashboard/StatisticsCards";
import RecentIncidents from "../components/Dashboard/RecentIncident";
import InvestigationProgress from "../components/Dashboard/InvestigationProgress";
import InvestigationStatus from "../components/Dashboard/InvestigationStatus";

export default function DashboardPage() {
    const queryClient = useQueryClient();
    const [isInvestigationRunning, setIsInvestigationRunning] = useState(false);

    // Fetch dashboard statistics
    const { 
        data: dashboardStats, 
        isLoading: statsLoading, 
        error: statsError 
    } = useQuery({
        queryKey: ['dashboard-stats'],
        queryFn: dashboardService.getDashboardStats,
        refetchInterval: 30000 // Refresh every 30 seconds
    });

    // Fetch recent investigations
    const { 
        data: investigations, 
        isLoading: investigationsLoading, 
        error: investigationsError 
    } = useQuery({
        queryKey: ['recent-investigations'],
        queryFn: () => dashboardService.getRecentInvestigations(10),
        refetchInterval: 10000 // Refresh every 10 seconds
    });

    // Fetch investigation status
    const { 
        data: investigationStatus, 
        isLoading: statusLoading 
    } = useQuery({
        queryKey: ['investigation-status'],
        queryFn: dashboardService.getInvestigationStatus,
        refetchInterval: 5000 // Refresh every 5 seconds
    });

    // Start investigation mutation
    const startInvestigationMutation = useMutation({
        mutationFn: investigationService.startInvestigation,
        onMutate: () => {
            setIsInvestigationRunning(true);
        },
        onSuccess: (data) => {
            // Refresh related queries
            queryClient.invalidateQueries(['recent-investigations']);
            queryClient.invalidateQueries(['investigation-status']);
            queryClient.invalidateQueries(['dashboard-stats']);
            
            // Navigate to investigation page if ID is returned
            if (data?.investigation_id) {
                window.location.href = `/investigation/${data.investigation_id}`;
            }
        },
        onError: (error) => {
            console.error('Failed to start investigation:', error);
        },
        onSettled: () => {
            setIsInvestigationRunning(false);
        }
    });

    const handleStartInvestigation = () => {
        startInvestigationMutation.mutate();
    };

    // Loading skeleton component
    const LoadingSkeleton = () => (
        <div className="grid">
            <div className="col-12">
                <Skeleton height="3rem" className="mb-3" />
            </div>
            {[...Array(4)].map((_, i) => (
                <div key={i} className="col-12 md:col-6 lg:col-3">
                    <Skeleton height="8rem" />
                </div>
            ))}
            <div className="col-12">
                <Skeleton height="12rem" />
            </div>
        </div>
    );

    // Error component
    const ErrorMessage = ({ error, onRetry }) => (
        <Message 
            severity="error" 
            text={`Failed to load dashboard data: ${error.message}`}
            className="mb-3"
        />
    );

    if (statsLoading && investigationsLoading && statusLoading) {
        return (
            <div className="dashboard-page">
                <LoadingSkeleton />
            </div>
        );
    }

    return (
        <div className="dashboard-page">
            <DashboardHeader />

            {/* Start Investigation Section */}
            <Card className="mb-4 start-investigation-card">
                <div className="flex align-items-center justify-content-between">
                    <div>
                        <h3 className="m-0 mb-2">Investigation Control</h3>
                        <p className="m-0 text-600">
                            Launch AI-powered autonomous incident investigation
                        </p>
                    </div>
                    <Button
                        label={isInvestigationRunning ? "Running Investigation..." : "Start New Investigation"}
                        icon={isInvestigationRunning ? "pi pi-spin pi-spinner" : "pi pi-play"}
                        onClick={handleStartInvestigation}
                        disabled={isInvestigationRunning || investigationStatus?.status === 'running'}
                        loading={startInvestigationMutation.isPending}
                        severity="success"
                        size="large"
                        className="investigation-start-btn"
                    />
                </div>
            </Card>

            {/* Investigation Status */}
            <div className="grid mb-4">
                <div className="col-12 md:col-6">
                    <InvestigationStatus 
                        status={investigationStatus}
                        loading={statusLoading}
                        running={isInvestigationRunning || investigationStatus?.status === 'running'}
                    />
                </div>
                <div className="col-12 md:col-6">
                    <InvestigationProgress 
                        status={investigationStatus}
                        running={isInvestigationRunning || investigationStatus?.status === 'running'}
                    />
                </div>
            </div>

            {/* Statistics Cards */}
            {statsError ? (
                <ErrorMessage error={statsError} />
            ) : (
                <StatisticsCards 
                    stats={dashboardStats} 
                    investigations={investigations} 
                    loading={statsLoading}
                />
            )}

            {/* Recent Investigations */}
            <div className="grid">
                <div className="col-12">
                    <Card className="recent-investigations-card">
                        <div className="card-header mb-3">
                            <h4 className="m-0">Recent Investigations</h4>
                            <Button 
                                label="View All" 
                                icon="pi pi-external-link"
                                className="p-button-text"
                                onClick={() => window.location.href = '/history'}
                            />
                        </div>

                        {investigationsError ? (
                            <ErrorMessage error={investigationsError} />
                        ) : investigationsLoading ? (
                            <div className="grid">
                                {[...Array(3)].map((_, i) => (
                                    <div key={i} className="col-12 md:col-6 lg:col-4">
                                        <Skeleton height="6rem" />
                                    </div>
                                ))}
                            </div>
                        ) : investigations && investigations.length > 0 ? (
                            <InvestigationList investigations={investigations} />
                        ) : (
                            <Message 
                                severity="info" 
                                text="No investigations found. Start your first investigation above."
                                className="w-full"
                            />
                        )}
                    </Card>
                </div>
            </div>
        </div>
    );
}