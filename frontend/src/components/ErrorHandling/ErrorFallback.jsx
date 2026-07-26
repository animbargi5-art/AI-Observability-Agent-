import React from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import { Divider } from 'primereact/divider';

/**
 * Generic error fallback component for error boundaries
 */
export const ErrorFallback = ({ 
    error, 
    onReset, 
    onReload,
    title = 'Something went wrong',
    showError = false 
}) => {
    return (
        <div className="error-fallback-container flex justify-content-center align-items-center min-h-screen p-4">
            <Card className="error-fallback-card max-w-30rem w-full">
                <div className="text-center">
                    <i 
                        className="pi pi-exclamation-triangle text-red-500 mb-3" 
                        style={{ fontSize: '3rem' }}
                    />
                    
                    <h1 className="text-2xl font-bold mb-3 text-red-600">
                        {title}
                    </h1>
                    
                    <p className="text-600 mb-4 line-height-3">
                        We apologize for the inconvenience. An unexpected error has occurred. 
                        Please try refreshing the page or contact support if the problem persists.
                    </p>

                    <div className="flex flex-column gap-2 mb-4">
                        <Button 
                            label="Try Again" 
                            icon="pi pi-refresh"
                            onClick={onReset}
                            className="w-full"
                        />
                        <Button 
                            label="Reload Page" 
                            icon="pi pi-reload"
                            onClick={onReload}
                            severity="secondary"
                            className="w-full"
                        />
                    </div>

                    {showError && error && (
                        <>
                            <Divider />
                            <details className="text-left">
                                <summary className="cursor-pointer text-sm font-semibold mb-2">
                                    Technical Details
                                </summary>
                                <div className="bg-gray-50 p-3 border-round text-xs">
                                    <pre className="overflow-auto">
                                        {error.toString()}
                                        {error.stack && '\n' + error.stack}
                                    </pre>
                                </div>
                            </details>
                        </>
                    )}
                </div>
            </Card>
        </div>
    );
};

/**
 * Page-level error fallback
 */
export const PageErrorFallback = ({ 
    error, 
    onRetry, 
    onGoHome,
    title = 'Page Error',
    message = 'This page encountered an error and could not be displayed.'
}) => {
    return (
        <div className="page-error-fallback flex justify-content-center align-items-center p-6">
            <Card className="text-center max-w-28rem">
                <i 
                    className="pi pi-times-circle text-red-400 mb-3" 
                    style={{ fontSize: '4rem' }}
                />
                
                <h2 className="text-xl font-semibold mb-3">{title}</h2>
                
                <p className="text-600 mb-4 line-height-3">{message}</p>

                <div className="flex justify-content-center gap-2">
                    {onRetry && (
                        <Button 
                            label="Try Again" 
                            icon="pi pi-refresh"
                            onClick={onRetry}
                            className="p-button-outlined"
                        />
                    )}
                    {onGoHome && (
                        <Button 
                            label="Go to Dashboard" 
                            icon="pi pi-home"
                            onClick={onGoHome}
                        />
                    )}
                </div>
            </Card>
        </div>
    );
};

/**
 * Component-level error fallback
 */
export const ComponentErrorFallback = ({ 
    error, 
    onRetry,
    componentName = 'Component',
    minimal = false 
}) => {
    if (minimal) {
        return (
            <div className="component-error-fallback-minimal p-3 border-1 border-red-300 bg-red-50 border-round">
                <div className="flex align-items-center justify-content-between">
                    <div className="flex align-items-center gap-2">
                        <i className="pi pi-exclamation-triangle text-red-600" />
                        <span className="text-red-600 text-sm">
                            {componentName} failed to load
                        </span>
                    </div>
                    {onRetry && (
                        <Button 
                            icon="pi pi-refresh"
                            size="small"
                            onClick={onRetry}
                            className="p-button-text p-button-sm"
                            tooltip="Retry loading"
                        />
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="component-error-fallback p-4 border-1 border-red-200 bg-red-50 border-round text-center">
            <i className="pi pi-exclamation-triangle text-red-500 mb-2 block" />
            <div className="text-sm text-red-600 mb-2">
                {componentName} Error
            </div>
            <div className="text-xs text-600 mb-3">
                This component encountered an error and could not be rendered.
            </div>
            {onRetry && (
                <Button 
                    label="Retry" 
                    icon="pi pi-refresh"
                    size="small"
                    onClick={onRetry}
                    className="p-button-outlined p-button-sm"
                />
            )}
        </div>
    );
};

export default ErrorFallback;