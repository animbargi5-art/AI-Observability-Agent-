import {
    CartesianGrid,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from "recharts";

import "../../styles/trend-chart.css";

export default function TrendChart({ data }) {
    const cumulativeData = data.reduce((result, item) => {
        const previous = result.at(-1)?.investigations ?? 0;

        result.push({
            ...item,
            investigations: previous + item.investigations
        });

        return result;
    }, []);

    return (
        <section className="trend-chart">
            <h2>Investigation trend</h2>
            {cumulativeData.length === 0 ? (
                <p>No investigation data is available yet.</p>
            ) : (
                <ResponsiveContainer width="100%" height={280}>
                    <LineChart data={cumulativeData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        <Line
                            type="monotone"
                            dataKey="investigations"
                            stroke="#2563eb"
                            strokeWidth={2}
                        />
                    </LineChart>
                </ResponsiveContainer>
            )}
        </section>
    );
}
