import { useRef, useCallback } from 'react';

/**
 * Custom hook for managing toast notifications
 * Provides a consistent interface for showing toast messages
 */
export const useToast = () => {
    const toastRef = useRef(null);

    const showToast = useCallback((message, severity = 'info', options = {}) => {
        if (!toastRef.current) {
            console.warn('Toast ref not available. Make sure Toast component is mounted.');
            return;
        }

        const defaultOptions = {
            life: severity === 'error' ? 6000 : 4000, // Error messages stay longer
            closable: true,
            ...options
        };

        toastRef.current.show({
            severity,
            summary: getSeverityLabel(severity),
            detail: message,
            ...defaultOptions
        });
    }, []);

    const showSuccess = useCallback((message, options = {}) => {
        showToast(message, 'success', options);
    }, [showToast]);

    const showError = useCallback((message, options = {}) => {
        showToast(message, 'error', options);
    }, [showToast]);

    const showWarning = useCallback((message, options = {}) => {
        showToast(message, 'warn', options);
    }, [showToast]);

    const showInfo = useCallback((message, options = {}) => {
        showToast(message, 'info', options);
    }, [showToast]);

    const clear = useCallback(() => {
        if (toastRef.current) {
            toastRef.current.clear();
        }
    }, []);

    const setToastRef = useCallback((ref) => {
        toastRef.current = ref;
    }, []);

    return {
        showToast,
        showSuccess,
        showError,
        showWarning,
        showInfo,
        clear,
        setToastRef,
        toastRef
    };
};

// Helper function to get severity labels
const getSeverityLabel = (severity) => {
    const labels = {
        success: 'Success',
        info: 'Information',
        warn: 'Warning',
        error: 'Error'
    };
    return labels[severity] || 'Notification';
};

export default useToast;