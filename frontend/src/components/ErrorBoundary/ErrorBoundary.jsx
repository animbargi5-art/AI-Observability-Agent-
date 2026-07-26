import React from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import { Message } from 'primereact/message';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            hasError: false, 
            error: null, 
            errorInfo: null 
        };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        this.setState({
            error,
            errorInfo
        });

        // Log error to monitoring service if available
        if (window.logError) {
            window.logError(error, errorInfo);
        }
    }

    handleReload = () => {
        window.location.reload();
    };

    handleReset = () => {
        this.setState({ 
            hasError: false, 
            error: null, 
            errorInfo: null 
        });
    };

    render() {
        if (this.state.hasError) {
            const { fallback: CustomFallback, showDetails = false } = this.props;
            const { error, errorInfo } = this.state;

            if (CustomFallback) {
                return (
                    <CustomFallback 
                        error={error}
                        errorInfo={errorInfo}
                        onReset={this.handleReset}
                        onReload={this.handleReload}
                    />
                );
            }

            return (
                <div className="error-boundary-container p-4">
                    <Card className="error-boundary-card">
                        <div className="text-center">
                            <i 
                                className="pi pi-exclamation-triangle text-red-500 mb-3" 
                                style={{ fontSize: '3rem' }}
                            />
                            <h2 className="text-xl font-semibold mb-3 text-red-600">
                                Something went wrong
                            </h2>
                            <p className="text-600 mb-4 line-height-3">
                                An unexpected error occurred while rendering this component. 
                                Please try refreshing the page or contact support if the problem persists.
                            </p>

                            <div className="flex justify-content-center gap-2 mb-4">
                                <Button 
                                    label="Try Again" 
                                    icon="pi pi-refresh"
                                    onClick={this.handleReset}
                                    className="p-button-outlined"
                                />
                                <Button 
                                    label="Reload Page" 
                                    icon="pi pi-reload"
                                    onClick={this.handleReload}
                                    severity="secondary"
                                />
                            </div>

                            {showDetails && error && (
                                <Message 
                                    severity="error" 
                                    className="text-left"
                                    content={
                                        <div>
                                            <strong>Error Details:</strong>
                                            <pre className="mt-2 text-sm">
                                                {error.toString()}
                                                {errorInfo?.componentStack}
                                            </pre>
                                        </div>
                                    }
                                />
                            )}
                        </div>
                    </Card>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;