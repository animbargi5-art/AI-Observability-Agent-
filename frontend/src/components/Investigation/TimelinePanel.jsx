import "../../styles/timeline-panel.css";

export default function TimelinePanel({

    investigation

}) {

    const timeline = investigation.report?.timeline || [];

    return (

        <div className="timeline-panel">

            <h2>

                Timeline

            </h2>

            {

                timeline.length === 0 ?

                (

                    <p>

                        No timeline available.

                    </p>

                )

                :

                (

                    timeline.map((event, index) => (

                        <div

                            key={index}

                            className="timeline-item"

                        >

                            <h3>

                                {event.title}

                            </h3>

                            <p>

                                {event.description}

                            </p>

                            <small>

                                {event.time}

                            </small>

                        </div>

                    ))

                )

            }

        </div>

    );

}