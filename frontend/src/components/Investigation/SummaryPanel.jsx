import "../../styles/summary-panel.css";

export default function SummaryPanel({

    investigation

}) {

    return (

        <div className="summary-panel">

            <h2>

                {investigation.title}

            </h2>

            <div className="summary-grid">

                <div>

                    <strong>Incident ID</strong>

                    <p>{investigation.incident_id}</p>

                </div>

                <div>

                    <strong>Severity</strong>

                    <p>{investigation.severity}</p>

                </div>

                <div>

                    <strong>Status</strong>

                    <p>{investigation.status}</p>

                </div>

                <div>

                    <strong>Confidence</strong>

                    <p>{investigation.confidence}%</p>

                </div>

            </div>

        </div>

    );

}