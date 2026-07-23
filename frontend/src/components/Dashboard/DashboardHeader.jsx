export default function DashboardHeader() {

    const now = new Date();

    const formattedTime = now.toLocaleString();

    return (

        <div className="dashboard-header">

            <div>

                <h1>TattvaAI Dashboard</h1>

                <p>
                    AI Powered Incident Intelligence Platform
                </p>

                <p className="dashboard-time">

                    Last Updated: {formattedTime}

                </p>

            </div>

            <div className="dashboard-actions">

                <button className="refresh-btn">

                    Refresh Dashboard

                </button>

            </div>

        </div>

    );

}