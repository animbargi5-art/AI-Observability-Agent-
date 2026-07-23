import "../../styles/incident-summary.css";

export default function IncidentSummary({ investigation }) {

    if (!investigation) return null;

    const report = investigation.report || {};

    const summary = report.executive_summary || {};

    const incident = report.incident || {};

    const statistics = report.statistics || {};

    return (

        <div className="incident-summary">

            <h2>Incident Summary</h2>

            <div className="summary-grid">

                <div className="summary-card">
                    <span>Incident</span>
                    <h3>{incident.title}</h3>
                </div>

                <div className="summary-card">
                    <span>ID</span>
                    <h3>{incident.id}</h3>
                </div>

                <div className="summary-card">
                    <span>Severity</span>
                    <h3>{summary.severity}</h3>
                </div>

                <div className="summary-card">
                    <span>Status</span>
                    <h3>{summary.status}</h3>
                </div>

                <div className="summary-card">
                    <span>Confidence</span>
                    <h3>{summary.confidence}%</h3>
                </div>

                <div className="summary-card">
                    <span>Evidence</span>
                    <h3>{statistics.evidence_count}</h3>
                </div>

                <div className="summary-card">
                    <span>Recommendations</span>
                    <h3>{statistics.recommendation_count}</h3>
                </div>

                <div className="summary-card">
                    <span>Timeline Events</span>
                    <h3>{statistics.timeline_events}</h3>
                </div>

            </div>

        </div>

    );

}