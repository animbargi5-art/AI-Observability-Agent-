export default function StatisticsCards({ investigations }) {
    // The dashboard API wraps recent rows in { investigations, total } while
    // the query cache may contain either shape during a hot refresh.
    const safeInvestigations = Array.isArray(investigations)
        ? investigations
        : Array.isArray(investigations?.investigations)
            ? investigations.investigations
            : [];

    // Additional safety check to ensure it's always an array
    const validInvestigations = Array.isArray(safeInvestigations) ? safeInvestigations : [];

    const total = validInvestigations.length;

    const critical = validInvestigations.filter(
        item => item?.severity === "CRITICAL"
    ).length;

    const high = validInvestigations.filter(
        item => item?.severity === "HIGH"
    ).length;

    const medium = validInvestigations.filter(
        item => item?.severity === "MEDIUM"
    ).length;

    const low = validInvestigations.filter(
        item => item?.severity === "LOW"
    ).length;

    const noIssue = validInvestigations.filter(
        item => item?.severity === "NONE"
    ).length;

    const avgConfidence =
        total === 0
            ? 0
            : Math.round(
                validInvestigations.reduce(
                    (sum, item) => sum + (item?.confidence || 0),
                    0
                ) / total
            );

    const investigating = validInvestigations.filter(
        item => item?.status === "INVESTIGATING"
    ).length;

    return (

        <div className="statistics-container">

            <div className="stat-card">
                <h3>Total Investigations</h3>
                <p>{total}</p>
            </div>

            <div className="stat-card critical">
                <h3>Critical</h3>
                <p>{critical}</p>
            </div>

            <div className="stat-card high">
                <h3>High</h3>
                <p>{high}</p>
            </div>

            <div className="stat-card medium">
                <h3>Medium</h3>
                <p>{medium}</p>
            </div>

            <div className="stat-card low">
                <h3>Low</h3>
                <p>{low}</p>
            </div>

            <div className="stat-card">
                <h3>No Issue</h3>
                <p>{noIssue}</p>
            </div>

            <div className="stat-card">
                <h3>Investigating</h3>
                <p>{investigating}</p>
            </div>

            <div className="stat-card">
                <h3>Average Confidence</h3>
                <p>{avgConfidence}%</p>
            </div>

        </div>

    );

}
