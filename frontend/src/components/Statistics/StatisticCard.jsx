import StatisticCard from "./StatisticCard";

export default function StatisticCard({

    title,

    value

}){

    return(

        <div className="stat-card">

            <h3>{title}</h3>

            <p>{value}</p>

            <StatisticCard
                title="Total"
                value={total}
            />

            <StatisticCard
                title="High"
                value={high}
            />

            <StatisticCard
                title="Low"
                value={low}
            />

            <StatisticCard
                title="No Issue"
                value={none}
            />

        </div>

    );

}