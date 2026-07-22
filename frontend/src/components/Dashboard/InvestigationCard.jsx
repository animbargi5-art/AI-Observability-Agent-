import { useNavigate } from "react-router-dom";

import "../../styles/investigation-card.css";

export default function InvestigationCard({ investigation }) {

    const navigate = useNavigate();

    function openInvestigation() {

        navigate(`/investigation/${investigation.id}`);

    }

    return (

        <div
            className="investigation-card"
            onClick={openInvestigation}
            style={{ cursor: "pointer" }}
        >

            <h2>{investigation.title}</h2>

            <p>

                <strong>Incident ID:</strong>

                {" "}

                {investigation.incident_id}

            </p>

            <p>

                <strong>Severity:</strong>

                {" "}

                {investigation.severity}

            </p>

            <p>

                <strong>Status:</strong>

                {" "}

                {investigation.status}

            </p>

            <p>

                <strong>Confidence:</strong>

                {" "}

                {investigation.confidence}%

            </p>

        </div>

    );

}