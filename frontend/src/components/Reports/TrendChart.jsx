import React from 'react';
import { Chart } from 'primereact/chart';
import { Card } from 'primereact/card';

const TrendChart = ({ data = [] }) => {
    // Process cumulative data
    const processedData = data.reduce((result, item, index) => {
        const previous = result[index - 1]?.y || 0;
        result.push({
            x: item.date,
            y: previous + (item.investigations || item.value || 1)
        });
        return result;
    }, []);

    // Transform data for Chart.js
    const chartData = {
        labels: processedData.map(item => item.x),
        datasets: [
            {
                label: 'Cumulative Investigations',
                data: processedData.map(item => item.y),
                borderColor: '#2563EB',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#2563EB',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }
        ]
    };

    const options = {
        plugins: {
            title: {
                display: true,
                text: 'Investigation Trends Over Time',
                font: {
                    size: 16,
                    weight: 'bold'
                },
                color: '#1F2937'
            },
            legend: {
                display: false
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    title: function(context) {
                        return `Date: ${context[0].label}`;
                    },
                    label: function(context) {
                        return `Total Investigations: ${context.parsed.y}`;
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Date',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                },
                grid: {
                    display: false
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: 'Cumulative Count',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                },
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            }
        },
        elements: {
            point: {
                hoverBorderWidth: 3
            }
        }
    };

    const cardHeader = (
        <div className="flex align-items-center gap-2">
            <i className="pi pi-chart-line text-blue-500"></i>
            <span className="font-semibold">Investigation Trends</span>
        </div>
    );

    return (
        <Card header={cardHeader} className="trend-chart-card">
            <div style={{ height: '350px' }}>
                {data && data.length > 0 ? (
                    <Chart type="line" data={chartData} options={options} />
                ) : (
                    <div className="flex align-items-center justify-content-center h-full">
                        <div className="text-center text-500">
                            <i className="pi pi-chart-line text-4xl mb-3"></i>
                            <p>No trend data available</p>
                        </div>
                    </div>
                )}
            </div>
        </Card>
    );
};

export default TrendChart;