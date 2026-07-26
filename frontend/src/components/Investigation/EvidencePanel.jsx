import "../../styles/evidence-panel.css";

export default function EvidencePanel({

    investigation

}) {

    const evidence = investigation.report?.evidence || [];

    return (

        <div className="evidence-panel">

            <h2>

                Investigation Evidence

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

                            <div className="evidence-header">

                                <h3>

                                    {item.type}

                                </h3>

                                <span
                                    className={`severity-badge ${item.severity?.toLowerCase()}`}
                                >
                                    {item.severity}
                                </span>

                            </div>

                            <div className="evidence-content">

                                <p>

                                    <strong>Category:</strong>

                                    {" "}

                                    {item.category}

                                </p>

                                <p>

                                    <strong>Confidence:</strong>

                                    {" "}

                                    {item.confidence}%

                                </p>

                                <p>

                                    <strong>Message:</strong>

                                    {" "}

                                    {item.summary}

                                </p>

                                <p>

                                    <strong>Service:</strong>

                                    {" "}

                                    {item.service_name || "Unknown"}

                                </p>

                                {

                                    item.trace && (

                                        <>

                                            <hr />

                                            <h4>

                                                Trace Information

                                            </h4>

                                            <p>

                                                <strong>Endpoint:</strong>

                                                {" "}

                                                {item.trace.endpoint || "N/A"}

                                            </p>

                                            <p>

                                                <strong>HTTP Method:</strong>

                                                {" "}

                                                {item.trace.method || "N/A"}

                                            </p>

                                            <p>

                                                <strong>Status:</strong>

                                                {" "}

                                                {item.trace.status || "N/A"}

                                            </p>

                                            <p>

                                                <strong>Duration:</strong>

                                                {" "}

                                                {item.trace.duration_ms ?? "N/A"} ms

                                            </p>

                                            <p>

                                                <strong>Trace ID:</strong>

                                                {" "}

                                                {item.trace.trace_id || "N/A"}

                                            </p>

                                        </>

                                    )

                                }

                            </div>

                        </div>

                    ))

                )

            }

        </div>

    );

}
