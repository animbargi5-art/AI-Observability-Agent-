import { useEffect, useState } from "react";

import ReportStatCard from "../components/Reports/ReportStatCard";
import SeverityChart from "../components/Reports/SeverityChart";
import StatusChart from "../components/Reports/StatusChart";

import { getAllInvestigations } from "../services/investigationService";

import "../styles/reports-page.css";

export default function ReportsPage() {

    const [investigations, setInvestigations] = useState([]);

    useEffect(() => {

        async function loadReports() {

            try {

                const data = await getAllInvestigations();

                setInvestigations(data);

            }

            catch (error) {

                console.error(error);

            }

        }

        loadReports();

    }, []);

    const total = investigations.length;

    const high = investigations.filter(

        investigation => investigation.severity === "HIGH"

    ).length;

    const medium = investigations.filter(

        investigation => investigation.severity === "MEDIUM"

    ).length;

    const low = investigations.filter(

        investigation => investigation.severity === "LOW"

    ).length;

    const noIssue = investigations.filter(

        investigation => investigation.severity === "NONE"

    ).length;

    const severityData = [

        {
            name: "HIGH",
            value: high
        },

        {
            name: "MEDIUM",
            value: medium
        },

        {
            name: "LOW",
            value: low
        },

        {
            name: "NONE",
            value: noIssue
        }

    ];

    const statusData = [

        {
            name: "INVESTIGATING",
            value: investigations.filter(
                item => item.status === "INVESTIGATING"
            ).length
        },

        {
            name: "RESOLVED",
            value: investigations.filter(
                item => item.status === "RESOLVED"
            ).length
        },

        {
            name: "NO_ISSUE",
            value: investigations.filter(
                item => item.status === "NO_ISSUE"
            ).length
        },

        {
            name: "FAILED",
            value: investigations.filter(
                item => item.status === "FAILED"
            ).length
        }

    ];

    return (

        <div className="reports-page">

            <h1>

                Reports Dashboard

            </h1>

            <div className="reports-stats">

                <ReportStatCard
                    title="Total"
                    value={total}
                />

                <ReportStatCard
                    title="High"
                    value={high}
                />

                <ReportStatCard
                    title="Medium"
                    value={medium}
                />

                <ReportStatCard
                    title="Low"
                    value={low}
                />

                <ReportStatCard
                    title="No Issue"
                    value={noIssue}
                />

            </div>

            <SeverityChart
                data={severityData}
            />

            <StatusChart
                data={statusData}
            />

        </div>

    );

}