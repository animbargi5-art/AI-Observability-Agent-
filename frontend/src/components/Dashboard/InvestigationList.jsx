import "../../styles/investigation-card.css";

import InvestigationCard from "./InvestigationCard";

export default function InvestigationList({

    investigations

}) {

    if (investigations.length === 0) {

        return (

            <p>No investigations found.</p>

        );

    }

    return (

        <div>

            {

                investigations.map(

                    (investigation) => (

                        <InvestigationCard

                            key={investigation.id}

                            investigation={investigation}

                        />

                    )

                )

            }

        </div>

    );

}