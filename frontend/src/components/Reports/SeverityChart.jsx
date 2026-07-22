import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const COLORS = [
    "#ef4444", // HIGH
    "#f59e0b", // MEDIUM
    "#3b82f6", // LOW
    "#10b981"  // NONE
];

export default function SeverityChart({ data }) {

    return (

        <div className="report-card">

            <h2>Severity Distribution</h2>

            <ResponsiveContainer width="100%" height={320}>

                <PieChart>

                    <Pie
                        data={data}
                        dataKey="value"
                        nameKey="name"
                        outerRadius={110}
                        label
                    >

                        {data.map((entry, index) => (

                            <Cell
                                key={index}
                                fill={COLORS[index % COLORS.length]}
                            />

                        ))}

                    </Pie>

                    <Tooltip />

                </PieChart>

            </ResponsiveContainer>

        </div>

    );

}