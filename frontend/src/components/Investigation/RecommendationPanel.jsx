import "../../styles/recommendation-panel.css";

export default function RecommendationPanel({

    investigation

}) {

    const recommendations =
        investigation.report?.recommendations || [];

    return (

        <div className="recommendation-panel">

            <h2>Recommendations</h2>

            {

                recommendations.length === 0 ? (

                    <p>

                        No recommendations available.

                    </p>

                ) : (

                    <ul>

                        {

                            recommendations.map(

                                (item, index) => (

                                <div
                                    key={index}
                                    className="recommendation-item"
                                >
                                    <h4>{item.title}</h4>

                                    <p>{item.description}</p>
                                    
                                </div>
                                )

                            )

                        }

                    </ul>

                )

            }

        </div>

    );

}