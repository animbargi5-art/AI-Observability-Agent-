import { useEffect, useState } from "react";

import InvestigationList from "../components/Dashboard/InvestigationList";
import SearchBar from "../components/History/SearchBar";
import SeverityFilter from "../components/History/SeverityFilter";

import StatusFilter from "../components/History/StatusFilter";
import SortFilter from "../components/History/SortFilter";

import {

    getAllInvestigations

} from "../services/investigationService";

export default function HistoryPage() {

    const [

        investigations,

        setInvestigations

    ] = useState([]);

    const [

        search,

        setSearch

    ] = useState("");

    const [

        severity,

        setSeverity

    ] = useState("ALL");

    const [

        status,

        setStatus

    ] = useState("ALL");

    const [

        sortBy,

        setSortBy

    ] = useState("NEWEST");

    const filteredInvestigations = investigations
        .filter((investigation) => {

            const matchesSearch =

                investigation.title
                    .toLowerCase()
                    .includes(search.toLowerCase()) ||

                investigation.incident_id
                    .toLowerCase()
                    .includes(search.toLowerCase());

            const matchesSeverity =

                severity === "ALL" ||

                investigation.severity === severity;

            const matchesStatus =

                status === "ALL" ||

                investigation.status === status;

            return (

                matchesSearch &&

                matchesSeverity &&

                matchesStatus

            );

        })

        .sort((a, b) => {

            switch (sortBy) {

                case "NEWEST":

                    return new Date(b.created_at) - new Date(a.created_at);

                case "OLDEST":

                    return new Date(a.created_at) - new Date(b.created_at);

                case "CONFIDENCE_HIGH":

                    return b.confidence - a.confidence;

                case "CONFIDENCE_LOW":

                    return a.confidence - b.confidence;

                default:

                    return 0;

            }

        });

    useEffect(() => {

        async function loadHistory() {

            try {

                const data = await getAllInvestigations();

                setInvestigations(data);

            }

            catch (error) {

                console.error(error);

            }

        }

        loadHistory();

    }, []);

    return (

        <div>

            <h1>

                Investigation History

            </h1>

            <SearchBar

                value={search}

                onChange={setSearch}

            />

            <SeverityFilter
               
                value={severity}

                onChange={setSeverity}

            />

            <StatusFilter

                value={status}

                onChange={setStatus}

            />

            <SortFilter

                value={sortBy}

                onChange={setSortBy}

            />

            <InvestigationList

                investigations={filteredInvestigations}

            />

        </div>

    );

}