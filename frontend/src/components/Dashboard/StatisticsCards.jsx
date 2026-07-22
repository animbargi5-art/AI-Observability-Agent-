export default function StatisticsCards({ investigations }) {

    const total = investigations.length;

    const high = investigations.filter(
        item => item.severity === "HIGH"
    ).length;

    const low = investigations.filter(
        item => item.severity === "LOW"
    ).length;

    const none = investigations.filter(
        item => item.severity === "NONE"
    ).length;

    return (

        <div className="statistics-container">

            <div className="stat-card">

                <h3>Total</h3>

                <p>{total}</p>

            </div>

            <div className="stat-card">

                <h3>High</h3>

                <p>{high}</p>

            </div>

            <div className="stat-card">

                <h3>Low</h3>

                <p>{low}</p>

            </div>

            <div className="stat-card">

                <h3>No Issue</h3>

                <p>{none}</p>

            </div>

        </div>

    );

}