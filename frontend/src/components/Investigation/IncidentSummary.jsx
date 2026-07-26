import "../../styles/incident-summary.css";

export default function IncidentSummary({ investigation }) {

    if (!investigation) return null;

    const report = investigation.report || {};

    const summary = report.executive_summary || "No summary available.";

    return (

        <div className="incident-summary">

            <h2>Incident Summary</h2>

            <div className="summary-grid">

                <div className="summary-card">
                    <span>Incident</span>
                    <h3>{report.title || investigation.title}</h3>
                </div>

                <div className="summary-card">
                    <span>ID</span>
                    <h3>{report.incident_id || investigation.incident_id}</h3>
                </div>

                <div className="summary-card">
                    <span>Severity</span>
                    <h3>{report.severity || investigation.severity}</h3>
                </div>

                <div className="summary-card">
                    <span>Status</span>
                    <h3>{report.status || investigation.status}</h3>
                </div>

                <div className="summary-card">
                    <span>Confidence</span>
                    <h3>{report.confidence ?? investigation.confidence}%</h3>
                </div>

                <div className="summary-card">
                    <span>Evidence</span>
                    <h3>{report.evidence_count ?? report.evidence?.length ?? 0}</h3>
                </div>

                <div className="summary-card">
                    <span>Recommendations</span>
                    <h3>{report.recommendation_count ?? report.recommendations?.length ?? 0}</h3>
                </div>

                <div className="summary-card">
                    <span>Timeline Events</span>
                    <h3>{report.timeline?.length ?? 0}</h3>
                </div>

            </div>
            <p>{summary}</p>

        </div>

    );

}
