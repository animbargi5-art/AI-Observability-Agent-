import React from 'react';
import { Chart } from 'primereact/chart';
import { Card } from 'primereact/card';

const StatusChart = ({ data = [] }) => {
    // Transform data for Chart.js
    const chartData = {
        labels: data.map(item => item.name || item.label),
        datasets: [
            {
                data: data.map(item => item.value),
                backgroundColor: [
                    '#2563EB', // IN_PROGRESS - Blue
                    '#10B981', // COMPLETED - Green  
                    '#F59E0B', // PENDING - Orange
                    '#EF4444', // FAILED - Red
                    '#6B7280'  // OTHER - Gray
                ],
                borderColor: [
                    '#1D4ED8',
                    '#059669',
                    '#D97706',
                    '#DC2626',
                    '#4B5563'
                ],
                borderWidth: 2,
                hoverBorderWidth: 3
            }
        ]
    };

    const options = {
        plugins: {
            title: {
                display: true,
                text: 'Status Distribution',
                font: {
                    size: 16,
                    weight: 'bold'
                },
                color: '#1F2937'
            },
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.parsed || 0;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                        return `${label}: ${value} (${percentage}%)`;
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        elements: {
            arc: {
                borderRadius: 4
            }
        }
    };

    const cardHeader = (
        <div className="flex align-items-center gap-2">
            <i className="pi pi-chart-bar text-green-500"></i>
            <span className="font-semibold">Status Distribution</span>
        </div>
    );

    return (
        <Card header={cardHeader} className="status-chart-card">
            <div style={{ height: '300px' }}>
                {data && data.length > 0 ? (
                    <Chart type="doughnut" data={chartData} options={options} />
                ) : (
                    <div className="flex align-items-center justify-content-center h-full">
                        <div className="text-center text-500">
                            <i className="pi pi-chart-bar text-4xl mb-3"></i>
                            <p>No status data available</p>
                        </div>
                    </div>
                )}
            </div>
        </Card>
    );
};

export default StatusChart;