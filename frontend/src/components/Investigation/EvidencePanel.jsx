import { Card } from "primereact/card";
import { Tag } from "primereact/tag";
import { TabView, TabPanel } from "primereact/tabview";
import { DataView } from "primereact/dataview";
import { Badge } from "primereact/badge";
import { Chip } from "primereact/chip";
import { Message } from "primereact/message";
import { Accordion, AccordionTab } from "primereact/accordion";

export default function EvidencePanel({ investigation }) {
    const evidence = investigation?.report?.evidence || [];

    const getSeverityInfo = (severity) => {
        switch (severity?.toUpperCase()) {
            case 'CRITICAL':
                return { severity: 'danger', color: 'text-red-600' };
            case 'HIGH':
                return { severity: 'warning', color: 'text-orange-600' };
            case 'MEDIUM':
                return { severity: 'info', color: 'text-blue-600' };
            case 'LOW':
                return { severity: 'success', color: 'text-green-600' };
            default:
                return { severity: 'secondary', color: 'text-gray-600' };
        }
    };

    const getEvidenceIcon = (type) => {
        switch (type?.toLowerCase()) {
            case 'trace':
                return 'pi pi-search';
            case 'log':
                return 'pi pi-file-o';
            case 'metric':
                return 'pi pi-chart-line';
            case 'alert':
                return 'pi pi-bell';
            default:
                return 'pi pi-info-circle';
        }
    };

    // Group evidence by category
    const groupedEvidence = evidence.reduce((groups, item) => {
        const category = item.category || item.type || 'Other';
        if (!groups[category]) {
            groups[category] = [];
        }
        groups[category].push(item);
        return groups;
    }, {});

    const evidenceTemplate = (item, index) => {
        const severityInfo = getSeverityInfo(item.severity);
        
        return (
            <Card className="evidence-card mb-3" key={index}>
                <div className="flex align-items-start justify-content-between mb-3">
                    <div className="flex align-items-center gap-2">
                        <i className={`${getEvidenceIcon(item.type)} text-primary`} 
                           style={{ fontSize: '1.25rem' }}></i>
                        <h4 className="m-0">{item.type}</h4>
                    </div>
                    <div className="flex gap-2">
                        <Tag 
                            value={item.severity}
                            severity={severityInfo.severity}
                            className="font-semibold"
                        />
                        <Badge 
                            value={`${item.confidence || 0}%`}
                            severity="info"
                        />
                    </div>
                </div>

                <div className="mb-3">
                    <p className="text-700 line-height-3 m-0">
                        {item.summary || item.message}
                    </p>
                </div>

                <div className="grid">
                    <div className="col-12 md:col-6">
                        <div className="field">
                            <label className="text-600 font-medium text-sm">Service</label>
                            <div className="mt-1">
                                <Chip 
                                    label={item.service_name || 'Unknown'} 
                                    icon="pi pi-server"
                                />
                            </div>
                        </div>
                    </div>

                    {item.timestamp && (
                        <div className="col-12 md:col-6">
                            <div className="field">
                                <label className="text-600 font-medium text-sm">Timestamp</label>
                                <div className="mt-1 flex align-items-center gap-2">
                                    <i className="pi pi-clock text-500"></i>
                                    <span className="text-700 text-sm">
                                        {new Date(item.timestamp).toLocaleString()}
                                    </span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Trace Information */}
                {item.trace && (
                    <Accordion className="mt-3">
                        <AccordionTab header="Trace Details">
                            <div className="grid">
                                <div className="col-12 md:col-6">
                                    <div className="field">
                                        <label className="text-600 font-medium text-sm">Endpoint</label>
                                        <p className="m-0 mt-1 text-700">{item.trace.endpoint || 'N/A'}</p>
                                    </div>
                                </div>
                                
                                <div className="col-12 md:col-6">
                                    <div className="field">
                                        <label className="text-600 font-medium text-sm">HTTP Method</label>
                                        <p className="m-0 mt-1 text-700">{item.trace.method || 'N/A'}</p>
                                    </div>
                                </div>
                                
                                <div className="col-12 md:col-6">
                                    <div className="field">
                                        <label className="text-600 font-medium text-sm">Status</label>
                                        <p className="m-0 mt-1 text-700">{item.trace.status || 'N/A'}</p>
                                    </div>
                                </div>
                                
                                <div className="col-12 md:col-6">
                                    <div className="field">
                                        <label className="text-600 font-medium text-sm">Duration</label>
                                        <p className="m-0 mt-1 text-700">
                                            {item.trace.duration_ms ? `${item.trace.duration_ms} ms` : 'N/A'}
                                        </p>
                                    </div>
                                </div>
                                
                                {item.trace.trace_id && (
                                    <div className="col-12">
                                        <div className="field">
                                            <label className="text-600 font-medium text-sm">Trace ID</label>
                                            <p className="m-0 mt-1 text-700 font-mono text-sm">
                                                {item.trace.trace_id}
                                            </p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </AccordionTab>
                    </Accordion>
                )}
            </Card>
        );
    };

    const headerTemplate = () => (
        <div className="flex align-items-center justify-content-between">
            <div className="flex align-items-center gap-2">
                <i className="pi pi-list text-700"></i>
                <span className="font-semibold">Investigation Evidence</span>
            </div>
            <Badge value={evidence.length} severity="info" />
        </div>
    );

    if (evidence.length === 0) {
        return (
            <Card header={headerTemplate} className="evidence-panel">
                <Message 
                    severity="info" 
                    text="No evidence available for this investigation."
                    className="w-full"
                />
            </Card>
        );
    }

    return (
        <Card header={headerTemplate} className="evidence-panel">
            {Object.keys(groupedEvidence).length > 1 ? (
                <TabView>
                    {Object.entries(groupedEvidence).map(([category, categoryEvidence]) => (
                        <TabPanel 
                            key={category} 
                            header={`${category} (${categoryEvidence.length})`}
                        >
                            <DataView
                                value={categoryEvidence}
                                itemTemplate={evidenceTemplate}
                                layout="list"
                            />
                        </TabPanel>
                    ))}
                </TabView>
            ) : (
                <DataView
                    value={evidence}
                    itemTemplate={evidenceTemplate}
                    layout="list"
                />
            )}
        </Card>
    );
}