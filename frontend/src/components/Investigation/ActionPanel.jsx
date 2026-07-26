import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { Divider } from "primereact/divider";

export default function ActionPanel({ 
    onRefresh, 
    onDelete, 
    refreshLoading = false, 
    deleteLoading = false 
}) {
    
    const headerTemplate = () => (
        <div className="flex align-items-center gap-2">
            <i className="pi pi-cog text-700"></i>
            <span className="font-semibold">Investigation Actions</span>
        </div>
    );

    return (
        <Card header={headerTemplate} className="action-panel-card">
            <div className="flex flex-column gap-3">
                <p className="text-600 m-0">
                    Manage this investigation with the available actions below.
                </p>

                <Divider />

                <div className="flex flex-wrap gap-3 justify-content-between">
                    {/* Primary Actions */}
                    <div className="flex flex-wrap gap-2">
                        <Button
                            label="Refresh Investigation"
                            icon="pi pi-refresh"
                            onClick={onRefresh}
                            loading={refreshLoading}
                            severity="info"
                            tooltip="Re-run the investigation analysis"
                            tooltipOptions={{ position: 'top' }}
                        />
                        
                        <Button
                            label="Export Report"
                            icon="pi pi-download"
                            severity="secondary"
                            outlined
                            tooltip="Download investigation report (Coming Soon)"
                            tooltipOptions={{ position: 'top' }}
                            disabled
                        />
                        
                        <Button
                            label="Share"
                            icon="pi pi-share-alt"
                            severity="secondary"
                            outlined
                            tooltip="Share investigation with team (Coming Soon)"
                            tooltipOptions={{ position: 'top' }}
                            disabled
                        />
                    </div>

                    {/* Destructive Actions */}
                    <div className="flex gap-2">
                        <Button
                            label="Archive"
                            icon="pi pi-archive"
                            severity="secondary"
                            outlined
                            tooltip="Archive this investigation (Coming Soon)"
                            tooltipOptions={{ position: 'top' }}
                            disabled
                        />
                        
                        <Button
                            label="Delete Investigation"
                            icon="pi pi-trash"
                            onClick={onDelete}
                            loading={deleteLoading}
                            severity="danger"
                            outlined
                            tooltip="Permanently delete this investigation"
                            tooltipOptions={{ position: 'top' }}
                        />
                    </div>
                </div>

                {/* Help Text */}
                <div className="mt-2 p-3 bg-blue-50 border-round">
                    <div className="flex gap-2">
                        <i className="pi pi-info-circle text-blue-600"></i>
                        <div className="text-sm text-blue-900">
                            <strong>Refresh:</strong> Re-runs the AI investigation with current data. 
                            This may produce different results if the underlying telemetry has changed.
                        </div>
                    </div>
                </div>
            </div>
        </Card>
    );
}