import { useEffect, useState } from "react";

import { useParams, useNavigate } from "react-router-dom";

import {

    getInvestigationById,

    deleteInvestigation

} from "../services/investigationService";

import InvestigationHeader from "../components/Investigation/InvestigationHeader";

import RootCausePanel from "../components/Investigation/RootCausePanel";

import EvidencePanel from "../components/Investigation/EvidencePanel";

import TimelinePanel from "../components/Investigation/TimelinePanel";

import RecommendationPanel from "../components/Investigation/RecommendationPanel";

import ActionPanel from "../components/Investigation/ActionPanel";

import IncidentSummary from "../components/Investigation/IncidentSummary";

import CorrelationPanel from "../components/Investigation/CorrelationPanel";

import ReasoningPanel from "../components/Investigation/ReasoningPanel";

import InvestigationGraph from "../components/Investigation/InvestigationGraph";

import "../styles/investigation-page.css";

export default function InvestigationPage() {

    const { id } = useParams();

    const navigate = useNavigate();

    const [investigation, setInvestigation] = useState(null);

    const [loading, setLoading] = useState(true);

    async function loadInvestigation() {

        try {

            setLoading(true);

            const data = await getInvestigationById(id);

            console.log("FULL DATA");
            console.log(data);

            console.log("REPORT");
            console.log(data.report);

            console.log("ROOT CAUSE");
            console.log(data.report?.root_cause);

            console.log("CORRELATIONS");
            console.log(data.report?.correlations);

            console.log("REASONING");
            console.log(data.report?.reasoning);

            console.log("GRAPH");
            console.log(data.report?.graph);

            console.log("EVIDENCE");
            console.log(data.report?.evidence);

            console.log("TIMELINE");
            console.log(data.report?.timeline);

            console.log("RECOMMENDATIONS");
            console.log(data.report?.recommendations);

            setInvestigation(data);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    }

    async function handleDelete() {
         
        try {

            await deleteInvestigation(id);

            alert("Investigation deleted successfully.");

            navigate("/")

        }

        catch (error) {

            console.error(error);

            alert("Failed to delete investigation.");

        }
        
    }

    useEffect(() => {

        loadInvestigation();

    }, [id]);

    if (loading) {

        return (

            <h2>

                Loading Investigation...

            </h2>

        );

    }

    if (!investigation) {

        return (

            <h2>

                Investigation Not Found

            </h2>

        );

    }

    return (

        <div className="investigation-page">

            <InvestigationHeader

                investigation={investigation}

            />

            <IncidentSummary
    
                investigation={investigation}

            />

            <RootCausePanel

                investigation={investigation}

            />

            <CorrelationPanel

                investigation={investigation}

            />

            <ReasoningPanel

                investigation={investigation}

            />

            <InvestigationGraph

                investigation={investigation}

            />

            <EvidencePanel

                investigation={investigation}

            />

            <TimelinePanel

                investigation={investigation}

            />

            <RecommendationPanel

                investigation={investigation}

            />

            <ActionPanel

                onRefresh={loadInvestigation}

                onDelete={handleDelete}

            />

        </div>

    );

}