import "../../styles/investigation-header.css";

export default function InvestigationHeader({

    investigation

}) {

    return (

        <div className="investigation-header">

            <h1>

                {investigation.title}

            </h1>

            <div className="investigation-meta">

                <span>

                    <strong>Incident:</strong>

                    {" "}

                    {investigation.incident_id}

                </span>

                <span>

                    <strong>Severity:</strong>

                    {" "}

                    {investigation.severity}

                </span>

                <span>

                    <strong>Status:</strong>

                    {" "}

                    {investigation.status}

                </span>

                <span>

                    <strong>Confidence:</strong>

                    {" "}

                    {investigation.confidence}%

                </span>

            </div>

        </div>

    );

}