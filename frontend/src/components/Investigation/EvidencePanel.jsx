import "../../styles/evidence-panel.css";

export default function EvidencePanel({

    investigation

}) {

    const evidence = investigation.report?.evidence || [];

    return (

        <div className="evidence-panel">

            <h2>

                Evidence

            </h2>

            {

                evidence.length === 0 ?

                (

                    <p>

                        No evidence available.

                    </p>

                )

                :

                (

                    evidence.map((item, index) => (

                        <div

                            key={index}

                            className="evidence-card"

                        >

                            <h3>

                                {item.type}

                            </h3>

                            <p>

                                Severity: {item.severity}

                            </p>

                        </div>

                    ))

                )

            }

        </div>

    );

}