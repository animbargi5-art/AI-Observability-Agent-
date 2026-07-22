import "../../styles/report-stat-card.css";

export default function ReportStatCard({

    title,

    value

}) {

    return (

        <div className="report-stat-card">

            <h3>

                {title}

            </h3>

            <h1>

                {value}

            </h1>

        </div>

    );

}