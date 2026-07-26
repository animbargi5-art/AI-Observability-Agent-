import { useCallback } from 'react';
import { useToast } from './useToast';
import { normalizeError, logError, isRetryableError, isOfflineError } from '../utils/errorHandler';

/**
 * Error handling hook with toast notifications and retry logic
 */
export const useErrorHandler = (options = {}) => {
    const { showToast } = useToast();
    const {
        showToastOnError = true,
        logErrors = true,
        context = {}
    } = options;

    const handleError = useCallback((error, customOptions = {}) => {
        const {
            title,
            message,
            showRetryOption = false,
            onRetry,
            severity = 'error',
            life = 5000,
            suppressToast = false,
            customContext = {}
        } = customOptions;

        // Normalize the error
        const normalizedError = normalizeError(error);
        
        // Log the error if enabled
        if (logErrors) {
            logError(error, { ...context, ...customContext });
        }

        // Show toast notification if enabled and not suppressed
        if (showToastOnError && !suppressToast) {
            const toastMessage = message || normalizedError.message;
            const toastTitle = title || getErrorTitle(normalizedError);

            // Create toast content
            let toastContent = toastMessage;
            if (showRetryOption && onRetry && isRetryableError(error)) {
                toastContent = (
                    <div className="flex flex-column gap-2">
                        <span>{toastMessage}</span>
                        <button 
                            className="p-button p-button-sm p-button-outlined"
                            onClick={onRetry}
                        >
                            <i className="pi pi-refresh mr-2" />
                            Try Again
                        </button>
                    </div>
                );
            }

            showToast({
                severity,
                summary: toastTitle,
                detail: toastContent,
                life,
                sticky: normalizedError.severity === 'critical'
            });
        }

        return normalizedError;
    }, [showToast, showToastOnError, logErrors, context]);

    const handleAsyncError = useCallback(async (asyncFn, errorOptions = {}) => {
        try {
            return await asyncFn();
        } catch (error) {
            handleError(error, errorOptions);
            throw error; // Re-throw to allow caller to handle if needed
        }
    }, [handleError]);

    const createErrorHandler = useCallback((errorOptions = {}) => {
        return (error) => handleError(error, errorOptions);
    }, [handleError]);

    const clearErrors = useCallback(() => {
        // Clear any persistent error states if needed
        // This can be extended based on application needs
    }, []);

    return {
        handleError,
        handleAsyncError,
        createErrorHandler,
        clearErrors,
        // Utility functions
        isRetryable: isRetryableError,
        isOffline: isOfflineError,
        normalize: normalizeError
    };
};

/**
 * Get error title based on error type
 */
const getErrorTitle = (normalizedError) => {
    switch (normalizedError.type) {
        case 'network':
            return 'Connection Error';
        case 'validation':
            return 'Validation Error';
        case 'permission':
            return 'Access Denied';
        case 'not_found':
            return 'Not Found';
        case 'server':
            return 'Server Error';
        default:
            return 'Error';
    }
};

export default useErrorHandler;