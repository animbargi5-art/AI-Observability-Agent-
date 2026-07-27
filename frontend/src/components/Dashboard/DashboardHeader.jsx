export default function DashboardHeader({ onRefresh, refreshing = false }) {

    const now = new Date();

    const formattedTime = now.toLocaleString();

    return (

        <div className="dashboard-header">

            <div>

                <h1>Investigation workspace</h1>

                <p>
                    Live SigNoz evidence, clear incident decisions.
                </p>

                <p className="dashboard-time">

                    Updated {formattedTime}

                </p>

            </div>

            <div className="dashboard-actions">

                <button className="refresh-btn" onClick={onRefresh} disabled={refreshing}>
                    <i className={refreshing ? "pi pi-spin pi-spinner" : "pi pi-refresh"} />
                    {refreshing ? " Refreshing" : " Refresh"}
                </button>

            </div>

        </div>

    );

}
