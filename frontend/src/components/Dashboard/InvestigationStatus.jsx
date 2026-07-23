export default function InvestigationStatus({

    running

}) {

    return (

        <div className="status-card">

            <h2>Investigation Status</h2>

            {

                running ?

                (

                    <>

                        <p>

                            🟢 Running

                        </p>

                        <p>

                            AI agents are investigating...

                        </p>

                    </>

                )

                :

                (

                    <>

                        <p>

                            ⚪ Idle

                        </p>

                        <p>

                            Ready to start a new investigation.

                        </p>

                    </>

                )

            }

        </div>

    );

}