import "../../styles/root-cause-panel.css";

export default function RootCausePanel({ investigation }) {

    if (!investigation) {
        return null;
    }

    const rootCause = investigation.report?.root_cause;

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
                    <strong>{rootCause.service}</strong>
                </div>

                <div className="root-cause-item">
                    <span>Confidence</span>
                    <strong>{rootCause.confidence}%</strong>
                </div>

                <div className="root-cause-item full">
                    <span>Most Probable Cause</span>
                    <strong>{rootCause.cause}</strong>
                </div>

            </div>

        </div>

    );
}