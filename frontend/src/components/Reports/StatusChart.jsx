import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const COLORS = [
    "#2563eb", // INVESTIGATING
    "#10b981", // RESOLVED
    "#f59e0b", // NO_ISSUE
    "#ef4444"  // FAILED
];

export default function StatusChart({ data }) {

    return (

        <div className="report-card">

            <h2>Status Distribution</h2>

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