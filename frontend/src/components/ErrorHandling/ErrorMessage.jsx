import React from 'react';
import { Message } from 'primereact/message';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';

/**
 * Generic error message component
 */
export const ErrorMessage = ({ 
    error, 
    title = 'Error',
    message,
    severity = 'error',
    showRetry = false,
    onRetry,
    showDetails = false,
    className = ''
}) => {
    const getErrorMessage = () => {
        if (message) return message;
        if (error?.message) return error.message;
        if (typeof error === 'string') return error;
        return 'An unexpected error occurred';
    };

    const getErrorDetails = () => {
        if (!error) return null;
        return error.stack || error.toString();
    };

    return (
        <div className={`error-message ${className}`}>
            <Message 
                severity={severity}
                content={
                    <div className="flex flex-column gap-2">
                        <div className="flex align-items-center gap-2">
                            <strong>{title}</strong>
                        </div>
                        <div>{getErrorMessage()}</div>
                        
                        {showRetry && onRetry && (
                            <div className="mt-2">
                                <Button 
                                    label="Try Again" 
                                    icon="pi pi-refresh"
                                    size="small"
                                    onClick={onRetry}
                                    className="p-button-outlined"
                                />
                            </div>
                        )}

                        {showDetails && getErrorDetails() && (
                            <details className="mt-2">
                                <summary className="cursor-pointer text-sm">Show Details</summary>
                                <pre className="mt-2 text-xs overflow-auto max-w-full">
                                    {getErrorDetails()}
                                </pre>
                            </details>
                        )}
                    </div>
                }
            />
        </div>
    );
};

/**
 * Network error component
 */
export const NetworkError = ({ 
    onRetry,
    isOffline = false,
    className = ''
}) => {
    const message = isOffline 
        ? 'You appear to be offline. Please check your internet connection.'
        : 'Unable to connect to the server. Please check your connection and try again.';

    return (
        <Card className={`network-error text-center p-4 ${className}`}>
            <i 
                className="pi pi-wifi text-orange-500 mb-3" 
                style={{ fontSize: '2rem' }}
            />
            <h3 className="text-lg font-semibold mb-2">Connection Problem</h3>
            <p className="text-600 mb-3 line-height-3">{message}</p>
            {onRetry && (
                <Button 
                    label="Retry"
                    icon="pi pi-refresh"
                    onClick={onRetry}
                />
            )}
        </Card>
    );
};

/**
 * Not found error component
 */
export const NotFoundError = ({ 
    resource = 'page',
    message,
    onGoBack,
    onGoHome,
    className = ''
}) => {
    const defaultMessage = `The ${resource} you're looking for could not be found.`;

    return (
        <Card className={`not-found-error text-center p-5 ${className}`}>
            <i 
                className="pi pi-search text-gray-400 mb-3" 
                style={{ fontSize: '3rem' }}
            />
            <h2 className="text-xl font-semibold mb-2">Not Found</h2>
            <p className="text-600 mb-4 line-height-3">
                {message || defaultMessage}
            </p>
            <div className="flex justify-content-center gap-2">
                {onGoBack && (
                    <Button 
                        label="Go Back"
                        icon="pi pi-arrow-left"
                        onClick={onGoBack}
                        className="p-button-outlined"
                    />
                )}
                {onGoHome && (
                    <Button 
                        label="Go Home"
                        icon="pi pi-home"
                        onClick={onGoHome}
                    />
                )}
            </div>
        </Card>
    );
};

/**
 * Permission denied error component
 */
export const PermissionError = ({ 
    message = 'You do not have permission to access this resource.',
    onLogin,
    onGoBack,
    className = ''
}) => {
    return (
        <Card className={`permission-error text-center p-5 ${className}`}>
            <i 
                className="pi pi-lock text-red-500 mb-3" 
                style={{ fontSize: '2.5rem' }}
            />
            <h2 className="text-xl font-semibold mb-2 text-red-600">Access Denied</h2>
            <p className="text-600 mb-4 line-height-3">{message}</p>
            <div className="flex justify-content-center gap-2">
                {onLogin && (
                    <Button 
                        label="Login"
                        icon="pi pi-sign-in"
                        onClick={onLogin}
                    />
                )}
                {onGoBack && (
                    <Button 
                        label="Go Back"
                        icon="pi pi-arrow-left"
                        onClick={onGoBack}
                        className="p-button-outlined"
                    />
                )}
            </div>
        </Card>
    );
};

/**
 * Inline error component for form fields
 */
export const InlineError = ({ 
    error, 
    show = true,
    className = ''
}) => {
    if (!show || !error) return null;

    return (
        <small className={`inline-error p-error block mt-1 ${className}`}>
            {typeof error === 'string' ? error : error.message}
        </small>
    );
};

export default ErrorMessage;