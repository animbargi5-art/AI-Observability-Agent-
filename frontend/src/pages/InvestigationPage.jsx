import { useEffect, useState } from "react";

import { useParams, useNavigate } from "react-router-dom";

import {

    getInvestigationById,

    deleteInvestigation

} from "../services/investigationService";

import InvestigationHeader from "../components/Investigation/InvestigationHeader";

import SummaryPanel from "../components/Investigation/SummaryPanel";

import EvidencePanel from "../components/Investigation/EvidencePanel";

import TimelinePanel from "../components/Investigation/TimelinePanel";

import RecommendationPanel from "../components/Investigation/RecommendationPanel";

import ActionPanel from "../components/Investigation/ActionPanel";

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

            console.log("Investigation Data:", data);

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

            <SummaryPanel

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