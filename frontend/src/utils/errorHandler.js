/**
 * Global error handling utilities
 */

// Error types
export const ErrorTypes = {
    NETWORK: 'network',
    VALIDATION: 'validation',
    PERMISSION: 'permission',
    NOT_FOUND: 'not_found',
    SERVER: 'server',
    CLIENT: 'client',
    UNKNOWN: 'unknown'
};

// Error severity levels
export const ErrorSeverity = {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high',
    CRITICAL: 'critical'
};

/**
 * Normalize error object
 */
export const normalizeError = (error) => {
    if (!error) {
        return {
            type: ErrorTypes.UNKNOWN,
            message: 'An unknown error occurred',
            severity: ErrorSeverity.LOW,
            code: 'UNKNOWN_ERROR'
        };
    }

    // Handle axios errors
    if (error.response) {
        const { status, data } = error.response;
        return {
            type: getErrorTypeFromStatus(status),
            message: data?.message || data?.error || getDefaultMessage(status),
            severity: getSeverityFromStatus(status),
            code: data?.code || `HTTP_${status}`,
            status,
            data: data?.details
        };
    }

    // Handle network errors
    if (error.request) {
        return {
            type: ErrorTypes.NETWORK,
            message: 'Network error: Unable to connect to server',
            severity: ErrorSeverity.HIGH,
            code: 'NETWORK_ERROR',
            isNetworkError: true
        };
    }

    // Handle validation errors
    if (error.name === 'ValidationError' || error.type === 'validation') {
        return {
            type: ErrorTypes.VALIDATION,
            message: error.message || 'Validation failed',
            severity: ErrorSeverity.MEDIUM,
            code: 'VALIDATION_ERROR',
            fields: error.fields || {}
        };
    }

    // Handle JavaScript errors
    if (error instanceof Error) {
        return {
            type: ErrorTypes.CLIENT,
            message: error.message,
            severity: ErrorSeverity.MEDIUM,
            code: error.name || 'CLIENT_ERROR',
            stack: error.stack
        };
    }

    // Handle string errors
    if (typeof error === 'string') {
        return {
            type: ErrorTypes.UNKNOWN,
            message: error,
            severity: ErrorSeverity.LOW,
            code: 'STRING_ERROR'
        };
    }

    // Handle custom error objects
    return {
        type: error.type || ErrorTypes.UNKNOWN,
        message: error.message || 'An error occurred',
        severity: error.severity || ErrorSeverity.MEDIUM,
        code: error.code || 'CUSTOM_ERROR',
        ...error
    };
};

/**
 * Get error type from HTTP status
 */
const getErrorTypeFromStatus = (status) => {
    if (status >= 400 && status < 500) {
        if (status === 401 || status === 403) return ErrorTypes.PERMISSION;
        if (status === 404) return ErrorTypes.NOT_FOUND;
        if (status === 422) return ErrorTypes.VALIDATION;
        return ErrorTypes.CLIENT;
    }
    if (status >= 500) return ErrorTypes.SERVER;
    return ErrorTypes.UNKNOWN;
};

/**
 * Get severity from HTTP status
 */
const getSeverityFromStatus = (status) => {
    if (status >= 500) return ErrorSeverity.HIGH;
    if (status === 401 || status === 403) return ErrorSeverity.MEDIUM;
    if (status === 404) return ErrorSeverity.LOW;
    return ErrorSeverity.MEDIUM;
};

/**
 * Get default message from HTTP status
 */
const getDefaultMessage = (status) => {
    const messages = {
        400: 'Bad request',
        401: 'Authentication required',
        403: 'Access denied',
        404: 'Resource not found',
        422: 'Validation failed',
        429: 'Too many requests',
        500: 'Internal server error',
        502: 'Bad gateway',
        503: 'Service unavailable',
        504: 'Gateway timeout'
    };
    return messages[status] || `HTTP error ${status}`;
};

/**
 * Check if error is retryable
 */
export const isRetryableError = (error) => {
    const normalizedError = normalizeError(error);
    
    // Network errors are retryable
    if (normalizedError.isNetworkError) return true;
    
    // Server errors (5xx) are retryable
    if (normalizedError.status >= 500) return true;
    
    // Rate limiting is retryable
    if (normalizedError.status === 429) return true;
    
    // Timeout errors are retryable
    if (normalizedError.code === 'TIMEOUT' || normalizedError.code === 'ECONNABORTED') return true;
    
    return false;
};

/**
 * Check if user is offline
 */
export const isOfflineError = (error) => {
    const normalizedError = normalizeError(error);
    return normalizedError.isNetworkError && !navigator.onLine;
};

/**
 * Global error logger
 */
export const logError = (error, context = {}) => {
    const normalizedError = normalizeError(error);
    
    const errorLog = {
        ...normalizedError,
        timestamp: new Date().toISOString(),
        url: window.location.href,
        userAgent: navigator.userAgent,
        context
    };

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
        console.error('Error logged:', errorLog);
    }

    // Send to error tracking service (implement as needed)
    if (window.errorTracker) {
        window.errorTracker.captureError(errorLog);
    }

    // Log to analytics (implement as needed)
    if (window.analytics) {
        window.analytics.track('Error Occurred', {
            error_type: normalizedError.type,
            error_code: normalizedError.code,
            error_severity: normalizedError.severity,
            error_message: normalizedError.message
        });
    }

    return errorLog;
};

/**
 * Create retry function with exponential backoff
 */
export const createRetryHandler = (fn, maxRetries = 3, baseDelay = 1000) => {
    return async (...args) => {
        let lastError;
        
        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return await fn(...args);
            } catch (error) {
                lastError = error;
                
                // Don't retry if it's not a retryable error
                if (!isRetryableError(error)) {
                    throw error;
                }
                
                // Don't retry on the last attempt
                if (attempt === maxRetries) {
                    break;
                }
                
                // Calculate delay with exponential backoff and jitter
                const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000;
                await new Promise(resolve => setTimeout(resolve, delay));
                
                logError(error, { 
                    attempt: attempt + 1, 
                    maxRetries, 
                    nextRetryIn: delay 
                });
            }
        }
        
        throw lastError;
    };
};

/**
 * Error boundary error handler
 */
export const handleErrorBoundaryError = (error, errorInfo, componentName) => {
    logError(error, {
        type: 'error_boundary',
        componentName,
        componentStack: errorInfo?.componentStack
    });
};

/**
 * Async error handler wrapper
 */
export const withErrorHandling = (asyncFn, options = {}) => {
    const { 
        onError, 
        retries = 0, 
        retryDelay = 1000,
        context = {} 
    } = options;

    return async (...args) => {
        const retryHandler = retries > 0 
            ? createRetryHandler(asyncFn, retries, retryDelay)
            : asyncFn;

        try {
            return await retryHandler(...args);
        } catch (error) {
            const errorLog = logError(error, context);
            
            if (onError) {
                onError(errorLog);
            }
            
            throw error;
        }
    };
};

export default {
    ErrorTypes,
    ErrorSeverity,
    normalizeError,
    isRetryableError,
    isOfflineError,
    logError,
    createRetryHandler,
    handleErrorBoundaryError,
    withErrorHandling
};