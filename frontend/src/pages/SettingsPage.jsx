import "../styles/settings-page.css";

export default function SettingsPage() {

    return (

        <div className="settings-page">

            <h1>
                Settings
            </h1>

            <div className="settings-card">

                <h2>
                    Application
                </h2>

                <div className="setting-row">

                    <span>Application Name</span>

                    <strong>TattvaAI</strong>

                </div>

                <div className="setting-row">

                    <span>Version</span>

                    <strong>1.0.0</strong>

                </div>

                <div className="setting-row">

                    <span>Environment</span>

                    <strong>Development</strong>

                </div>

            </div>

            <div className="settings-card">

                <h2>
                    Backend
                </h2>

                <div className="setting-row">

                    <span>API URL</span>

                    <strong>http://localhost:8000</strong>

                </div>

                <div className="setting-row">

                    <span>Status</span>

                    <strong>Connected</strong>

                </div>

            </div>

            <div className="settings-card">

                <h2>
                    About
                </h2>

                <p>

                    TattvaAI is an AI-powered incident investigation platform
                    that analyzes production incidents and provides evidence,
                    recommendations, and observability using SigNoz.

                </p>

            </div>

        </div>

    );

}