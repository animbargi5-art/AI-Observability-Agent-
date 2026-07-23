import "../../styles/reasoning-panel.css";

export default function ReasoningPanel({ investigation }) {

    if (!investigation) {
        return null;
    }

    const reasoning = investigation.report?.reasoning || {};

    const conclusions = reasoning.conclusions || [];

    return (

        <div className="reasoning-panel">

            <h2>AI Reasoning</h2>

            <div className="reasoning-grid">

                <div className="reasoning-item">
                    <span>Highest Severity</span>
                    <strong>{reasoning.highest_severity}</strong>
                </div>

                <div className="reasoning-item">
                    <span>Evidence Collected</span>
                    <strong>{reasoning.evidence_count}</strong>
                </div>

                <div className="reasoning-item">
                    <span>Graph Nodes</span>
                    <strong>{reasoning.graph_nodes}</strong>
                </div>

                <div className="reasoning-item">
                    <span>Graph Edges</span>
                    <strong>{reasoning.graph_edges}</strong>
                </div>

                <div className="reasoning-item">
                    <span>Correlations</span>
                    <strong>{reasoning.correlation_count}</strong>
                </div>

            </div>

            <div className="reasoning-conclusions">

                <h3>AI Conclusions</h3>

                {

                    conclusions.length === 0 ?

                    (

                        <p>No reasoning available.</p>

                    )

                    :

                    (

                        <ul>

                            {

                                conclusions.map((item, index) => (

                                    <li key={index}>

                                        ✅ {item}

                                    </li>

                                ))

                            }

                        </ul>

                    )

                }

            </div>

        </div>

    );

}