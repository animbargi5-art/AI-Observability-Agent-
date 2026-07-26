import { Card } from "primereact/card";
import { Tag } from "primereact/tag";
import { Skeleton } from "primereact/skeleton";
import { ProgressSpinner } from "primereact/progressspinner";

export default function InvestigationStatus({ status, loading, running }) {
    
    const getStatusInfo = () => {
        if (running || status?.status === 'running') {
            return {
                severity: 'success',
                icon: 'pi pi-play',
                label: 'RUNNING',
                description: 'AI agents are investigating incident...',
                color: 'text-green-500'
            };
        } else if (status?.status === 'completed') {
            return {
                severity: 'info',
                icon: 'pi pi-check',
                label: 'COMPLETED',
                description: 'Last investigation completed successfully',
                color: 'text-blue-500'
            };
        } else if (status?.status === 'failed') {
            return {
                severity: 'danger',
                icon: 'pi pi-times',
                label: 'FAILED',
                description: 'Last investigation encountered an error',
                color: 'text-red-500'
            };
        } else {
            return {
                severity: 'secondary',
                icon: 'pi pi-circle',
                label: 'IDLE',
                description: 'Ready to start a new investigation',
                color: 'text-500'
            };
        }
    };

    const statusInfo = getStatusInfo();

    const headerTemplate = () => (
        <div className="flex align-items-center gap-2">
            <i className="pi pi-info-circle text-700"></i>
            <span className="font-semibold">Investigation Status</span>
        </div>
    );

    if (loading) {
        return (
            <Card header={headerTemplate} className="status-card">
                <div className="flex flex-column gap-3">
                    <Skeleton height="2rem" width="8rem" />
                    <Skeleton height="1rem" />
                    <Skeleton height="1rem" width="70%" />
                </div>
            </Card>
        );
    }

    return (
        <Card header={headerTemplate} className="status-card">
            <div className="flex align-items-center gap-3 mb-3">
                {running ? (
                    <ProgressSpinner 
                        style={{ width: '24px', height: '24px' }} 
                        strokeWidth="4"
                    />
                ) : (
                    <i className={`${statusInfo.icon} ${statusInfo.color}`} 
                       style={{ fontSize: '1.5rem' }}></i>
                )}
                <Tag 
                    value={statusInfo.label} 
                    severity={statusInfo.severity}
                    className="font-bold"
                />
            </div>
            
            <p className="text-700 mb-2">
                {statusInfo.description}
            </p>
            
            {status?.last_updated && (
                <small className="text-600">
                    Last updated: {new Date(status.last_updated).toLocaleTimeString()}
                </small>
            )}
            
            {status?.investigation_id && (
                <div className="mt-2">
                    <small className="text-600">
                        Investigation ID: <span className="font-mono">{status.investigation_id}</span>
                    </small>
                </div>
            )}
        </Card>
    );
}