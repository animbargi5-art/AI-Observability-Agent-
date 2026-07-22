import { useEffect, useState } from "react";

import InvestigationList from "../components/Dashboard/InvestigationList";
import SearchBar from "../components/History/SearchBar";

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

    const filteredInvestigations = investigations.filter(

        (investigation) =>

            investigation.title

                .toLowerCase()

                .includes(

                    search.toLowerCase()

                ) ||

            investigation.incident_id

                .toLowerCase()

                .includes(

                    search.toLowerCase()

                )

        );

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

            <InvestigationList

                investigations={filteredInvestigations}

            />

        </div>

    );

}