import React from 'react';
import { Card } from 'primereact/card';
import { Badge } from 'primereact/badge';

const ReportStatCard = ({ title, value, icon, color = 'blue', trend, trendValue }) => {
    const getColorClass = (colorName) => {
        const colors = {
            blue: 'text-blue-500',
            red: 'text-red-500',
            orange: 'text-orange-500',
            yellow: 'text-yellow-500',
            green: 'text-green-500',
            purple: 'text-purple-500'
        };
        return colors[colorName] || colors.blue;
    };

    const getBgColorClass = (colorName) => {
        const colors = {
            blue: 'bg-blue-50',
            red: 'bg-red-50',
            orange: 'bg-orange-50',
            yellow: 'bg-yellow-50',
            green: 'bg-green-50',
            purple: 'bg-purple-50'
        };
        return colors[colorName] || colors.blue;
    };

    const cardContent = (
        <div className="flex align-items-center">
            <div className={`flex align-items-center justify-content-center border-round-md w-3rem h-3rem ${getBgColorClass(color)} mr-3`}>
                <i className={`${icon || 'pi pi-chart-bar'} text-xl ${getColorClass(color)}`}></i>
            </div>
            <div className="flex-1">
                <div className="text-sm text-600 mb-1">{title}</div>
                <div className="flex align-items-center gap-2">
                    <span className="text-2xl font-bold text-900">{value}</span>
                    {trend && (
                        <Badge 
                            value={trendValue || '0%'} 
                            severity={trend === 'up' ? 'success' : trend === 'down' ? 'danger' : 'info'}
                            size="small"
                        />
                    )}
                </div>
            </div>
        </div>
    );

    return (
        <Card className="report-stat-card">
            {cardContent}
        </Card>
    );
};

export default ReportStatCard;