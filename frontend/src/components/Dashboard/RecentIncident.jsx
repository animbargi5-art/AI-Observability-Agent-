import { useNavigate } from "react-router-dom";

export default function RecentIncidents({ investigations }) {

    const navigate = useNavigate();

    const recent = [...investigations]
        .sort(
            (a, b) =>
                new Date(b.created_at) -
                new Date(a.created_at)
        )
        .slice(0, 5);

    return (

        <div className="recent-incidents">

            <h2>Recent Investigations</h2>

            {

                recent.length === 0 ?

                (

                    <p>No investigations found.</p>

                )

                :

                (

                    recent.map(item => (

                        <div
                            key={item.id}
                            className="recent-card"
                            onClick={() =>
                                navigate(`/investigation/${item.id}`)
                            }
                        >

                            <h3>{item.title}</h3>

                            <p>

                                <strong>Severity:</strong>

                                {" "}

                                {item.severity}

                            </p>

                            <p>

                                <strong>Status:</strong>

                                {" "}

                                {item.status}

                            </p>

                            <p>

                                <strong>Confidence:</strong>

                                {" "}

                                {item.confidence}%

                            </p>

                        </div>

                    ))

                )

            }

        </div>

    );

}