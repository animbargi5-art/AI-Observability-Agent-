import { useEffect, useState } from "react";

import { getAllInvestigations } from "../services/investigationService";

import DashboardHeader from "../components/Dashboard/DashboardHeader";
import InvestigationList from "../components/Dashboard/InvestigationList";
import StatisticsCards from "../components/Dashboard/StatisticsCards";


import "../styles/header.css";
import "../styles/dashboard.css";
import "../styles/statistics.css";

export default function DashboardPage() {

    const [investigations, setInvestigations] = useState([]);

    const [loading, setLoading] = useState(true);

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

    return (

        <div className="dashboard-page">

            <DashboardHeader />

            <StatisticsCards investigations={investigations} />

            <InvestigationList investigations={investigations} />

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