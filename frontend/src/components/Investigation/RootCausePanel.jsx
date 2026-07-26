import "../../styles/root-cause-panel.css";

export default function RootCausePanel({ investigation }) {

    if (!investigation) {
        return null;
    }

    const rootCause = investigation.report?.root_causes?.[0];

    if (!rootCause) {
        return (
            <div className="root-cause-panel">
                <h2>Root Cause Analysis</h2>
                <p>No root cause available.</p>
            </div>
        );
    }

    return (

        <div className="root-cause-panel">

            <h2>Root Cause Analysis</h2>

            <div className="root-cause-card">

                <div className="root-cause-item">
                    <span>Service</span>
                    <strong>{rootCause.service_name}</strong>
                </div>

                <div className="root-cause-item">
                    <span>Confidence</span>
                    <strong>{rootCause.confidence}%</strong>
                </div>

                <div className="root-cause-item full">
                    <span>Most Probable Cause</span>
                    <strong>{rootCause.probable_cause}</strong>
                </div>

            </div>

        </div>

    );
}
