import { useEffect, useState } from "react";

import {
    getAllInvestigations,
    startInvestigation
} from "../services/investigationService";

import DashboardHeader from "../components/Dashboard/DashboardHeader";
import InvestigationList from "../components/Dashboard/InvestigationList";
import StatisticsCards from "../components/Dashboard/StatisticsCards";
import RecentIncidents from "../components/Dashboard/RecentIncidents";
import InvestigationProgress from "../components/Dashboard/InvestigationProgress";

import InvestigationStatus from "../components/Dashboard/InvestigationStatus";

import "../styles/status-card.css";
import "../styles/progress-panel.css";

import "../styles/header.css";
import "../styles/dashboard.css";
import "../styles/statistics.css";

export default function DashboardPage() {

    const [investigations, setInvestigations] = useState([]);

    const [loading, setLoading] = useState(true);

    const [running, setRunning] = useState(false);

    useEffect(() => {

        async function load() {

            try {

                const data = await getAllInvestigations();

                console.log(data);

                setInvestigations(data);

            }

            catch (error) {

                console.error(error);

            }

            finally {

                setLoading(false);

            }

        }

        load();

    }, []);


        async function runInvestigation() {

            try {

                setRunning(true);

                await startInvestigation();

                const updated = await getAllInvestigations();

                setInvestigations(updated);

            }

            catch (error) {

                console.error(error);

            }

            finally {

                setRunning(false);

            }

        }

    return (

        <div className="dashboard-page">

            <DashboardHeader />

            <div style={{ margin: "20px 0" }}>

                <button
                    onClick={runInvestigation}
                    disabled={running}
                >

                   {
                        running
                            ? "Running Investigation..."
                            : "Start New Investigation"
                    }

                </button>

            </div>

            <InvestigationStatus

                running={running}

            />
            <InvestigationProgress

                running={running}

            />

            <StatisticsCards investigations={investigations} />

            <RecentIncidents

                investigations={investigations}

            />

        {

            loading ?

            (

                <p>Loading investigations...</p>

            )

            :

            (

                <InvestigationList

                    investigations={investigations}

                />

            )

        }

    </div>

    );

}