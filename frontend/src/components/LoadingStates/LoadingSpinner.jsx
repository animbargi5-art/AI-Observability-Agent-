import React from 'react';
import { ProgressSpinner } from 'primereact/progressspinner';
import { Card } from 'primereact/card';
import { Skeleton } from 'primereact/skeleton';

/**
 * Loading spinner component with different variants
 */
export const LoadingSpinner = ({ 
    size = 'normal', 
    message = 'Loading...', 
    overlay = false,
    variant = 'spinner',
    className = ''
}) => {
    const getSpinnerSize = () => {
        const sizes = {
            small: '2rem',
            normal: '3rem',
            large: '4rem'
        };
        return sizes[size] || sizes.normal;
    };

    const spinnerContent = (
        <div className={`loading-spinner ${className}`}>
            <div className="flex flex-column align-items-center gap-3">
                <ProgressSpinner 
                    style={{ width: getSpinnerSize(), height: getSpinnerSize() }}
                    strokeWidth="4"
                />
                {message && <span className="text-600">{message}</span>}
            </div>
        </div>
    );

    if (overlay) {
        return (
            <div className="loading-overlay">
                <div className="loading-overlay-content">
                    {spinnerContent}
                </div>
            </div>
        );
    }

    return spinnerContent;
};

/**
 * Card loading skeleton
 */
export const CardSkeleton = ({ 
    lines = 3, 
    hasHeader = true, 
    hasFooter = false,
    className = ''
}) => {
    return (
        <Card className={`card-skeleton ${className}`}>
            {hasHeader && (
                <div className="mb-3">
                    <Skeleton width="60%" height="1.5rem" className="mb-2" />
                    <Skeleton width="40%" height="1rem" />
                </div>
            )}
            
            <div className="flex flex-column gap-2">
                {[...Array(lines)].map((_, index) => (
                    <Skeleton 
                        key={index}
                        width={index === lines - 1 ? '70%' : '100%'}
                        height="1rem"
                    />
                ))}
            </div>

            {hasFooter && (
                <div className="mt-3 pt-3" style={{ borderTop: '1px solid var(--surface-border)' }}>
                    <Skeleton width="30%" height="2rem" />
                </div>
            )}
        </Card>
    );
};

/**
 * Table loading skeleton
 */
export const TableSkeleton = ({ 
    rows = 5, 
    columns = 4,
    hasHeader = true,
    className = ''
}) => {
    return (
        <div className={`table-skeleton ${className}`}>
            {hasHeader && (
                <div className="grid mb-3 p-3" style={{ borderBottom: '1px solid var(--surface-border)' }}>
                    {[...Array(columns)].map((_, index) => (
                        <div key={index} className="col">
                            <Skeleton width="80%" height="1rem" />
                        </div>
                    ))}
                </div>
            )}
            
            {[...Array(rows)].map((rowIndex) => (
                <div key={rowIndex} className="grid p-3" style={{ borderBottom: '1px solid var(--surface-border)' }}>
                    {[...Array(columns)].map((_, colIndex) => (
                        <div key={colIndex} className="col">
                            <Skeleton 
                                width={colIndex === 0 ? '60%' : '90%'} 
                                height="1rem" 
                            />
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

/**
 * Chart loading skeleton
 */
export const ChartSkeleton = ({ 
    type = 'bar', 
    height = '300px',
    className = ''
}) => {
    const renderChart = () => {
        switch (type) {
            case 'pie':
                return (
                    <div className="flex justify-content-center align-items-center" style={{ height }}>
                        <div className="border-circle" style={{ width: '200px', height: '200px' }}>
                            <Skeleton width="100%" height="100%" borderRadius="50%" />
                        </div>
                    </div>
                );
            
            case 'line':
                return (
                    <div className="flex flex-column" style={{ height }}>
                        <div className="flex align-items-end justify-content-between flex-1 gap-1 mb-2">
                            {[...Array(8)].map((_, index) => (
                                <Skeleton 
                                    key={index}
                                    width="100%"
                                    height={`${Math.random() * 70 + 30}%`}
                                />
                            ))}
                        </div>
                        <Skeleton width="100%" height="1rem" />
                    </div>
                );
            
            default: // bar
                return (
                    <div className="flex flex-column" style={{ height }}>
                        <div className="flex align-items-end justify-content-between flex-1 gap-1 mb-2">
                            {[...Array(6)].map((_, index) => (
                                <Skeleton 
                                    key={index}
                                    width="100%"
                                    height={`${Math.random() * 80 + 20}%`}
                                />
                            ))}
                        </div>
                        <Skeleton width="100%" height="1rem" />
                    </div>
                );
        }
    };

    return (
        <div className={`chart-skeleton ${className}`}>
            <div className="mb-3">
                <Skeleton width="40%" height="1.5rem" />
            </div>
            {renderChart()}
        </div>
    );
};

/**
 * Page loading component
 */
export const PageSkeleton = ({ 
    hasHeader = true,
    hasSidebar = false,
    sections = 3,
    className = ''
}) => {
    return (
        <div className={`page-skeleton ${className}`}>
            {hasHeader && (
                <div className="mb-4">
                    <Skeleton width="30%" height="2rem" className="mb-2" />
                    <Skeleton width="60%" height="1rem" />
                </div>
            )}

            <div className={hasSidebar ? 'grid' : ''}>
                {hasSidebar && (
                    <div className="col-3">
                        <Card>
                            <Skeleton width="100%" height="1.5rem" className="mb-3" />
                            {[...Array(5)].map((_, index) => (
                                <Skeleton 
                                    key={index}
                                    width="100%" 
                                    height="2rem" 
                                    className="mb-2" 
                                />
                            ))}
                        </Card>
                    </div>
                )}
                
                <div className={hasSidebar ? 'col-9' : 'col-12'}>
                    {[...Array(sections)].map((_, index) => (
                        <CardSkeleton 
                            key={index} 
                            lines={4} 
                            hasHeader 
                            className="mb-3"
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default LoadingSpinner;