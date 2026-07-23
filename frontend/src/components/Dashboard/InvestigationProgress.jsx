import { useEffect, useState } from "react";

const steps = [

    "Starting Investigation...",

    "Trace Agent Completed",

    "Logs Agent Completed",

    "Metrics Agent Completed",

    "Alert Agent Completed",

    "Dependency Agent Completed",

    "Historical Agent Completed",

    "Correlation Engine Completed",

    "Root Cause Analysis Completed",

    "Recommendation Engine Completed",

    "Generating Final Report..."

];

export default function InvestigationProgress({ running }) {

    const [visibleSteps, setVisibleSteps] = useState([]);

    useEffect(() => {

        if (!running) {

            setVisibleSteps([]);

            return;

        }

        let current = 0;

        const timer = setInterval(() => {

            current++;

            setVisibleSteps(steps.slice(0, current));

            if (current === steps.length) {

                clearInterval(timer);

            }

        }, 500);

        return () => clearInterval(timer);

    }, [running]);

    if (!running) return null;

    return (

        <div className="progress-panel">

            <h2>AI Investigation Running</h2>

            {

                visibleSteps.map((step, index) => (

                    <p key={index}>

                        ✅ {step}

                    </p>

                ))

            }

        </div>

    );

}