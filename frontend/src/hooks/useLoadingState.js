import { useState, useCallback, useRef, useEffect } from 'react';

/**
 * Loading state management hook
 */
export const useLoadingState = (initialState = false) => {
    const [isLoading, setIsLoading] = useState(initialState);
    const [loadingStates, setLoadingStates] = useState({});
    const timeoutRef = useRef(null);

    // Set global loading state
    const setLoading = useCallback((loading, minDuration = 0) => {
        if (loading) {
            setIsLoading(true);
            // Clear any existing timeout
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }
        } else {
            if (minDuration > 0) {
                // Ensure loading shows for at least minDuration
                timeoutRef.current = setTimeout(() => {
                    setIsLoading(false);
                }, minDuration);
            } else {
                setIsLoading(false);
            }
        }
    }, []);

    // Set loading state for specific operations
    const setOperationLoading = useCallback((operation, loading) => {
        setLoadingStates(prev => ({
            ...prev,
            [operation]: loading
        }));
    }, []);

    // Check if specific operation is loading
    const isOperationLoading = useCallback((operation) => {
        return loadingStates[operation] || false;
    }, [loadingStates]);

    // Check if any operation is loading
    const hasAnyLoading = useCallback(() => {
        return Object.values(loadingStates).some(Boolean) || isLoading;
    }, [loadingStates, isLoading]);

    // Wrap async function with loading state
    const withLoading = useCallback((asyncFn, options = {}) => {
        const { 
            operation, 
            minDuration = 0,
            useGlobalLoading = false 
        } = options;

        return async (...args) => {
            try {
                if (operation) {
                    setOperationLoading(operation, true);
                }
                if (useGlobalLoading) {
                    setLoading(true, minDuration);
                }

                const result = await asyncFn(...args);
                return result;
            } finally {
                if (operation) {
                    setOperationLoading(operation, false);
                }
                if (useGlobalLoading) {
                    setLoading(false, minDuration);
                }
            }
        };
    }, [setLoading, setOperationLoading]);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }
        };
    }, []);

    return {
        isLoading,
        setLoading,
        loadingStates,
        setOperationLoading,
        isOperationLoading,
        hasAnyLoading,
        withLoading
    };
};

/**
 * Hook for managing async operations with loading and error states
 */
export const useAsyncOperation = (asyncFn, dependencies = []) => {
    const [state, setState] = useState({
        data: null,
        isLoading: false,
        error: null,
        isSuccess: false,
        isError: false
    });

    const execute = useCallback(async (...args) => {
        setState(prev => ({
            ...prev,
            isLoading: true,
            error: null,
            isSuccess: false,
            isError: false
        }));

        try {
            const result = await asyncFn(...args);
            setState({
                data: result,
                isLoading: false,
                error: null,
                isSuccess: true,
                isError: false
            });
            return result;
        } catch (error) {
            setState({
                data: null,
                isLoading: false,
                error,
                isSuccess: false,
                isError: true
            });
            throw error;
        }
    }, dependencies);

    const reset = useCallback(() => {
        setState({
            data: null,
            isLoading: false,
            error: null,
            isSuccess: false,
            isError: false
        });
    }, []);

    return {
        ...state,
        execute,
        reset
    };
};

/**
 * Hook for managing multiple loading states with priorities
 */
export const useMultipleLoadingStates = () => {
    const [states, setStates] = useState({});

    const setLoadingState = useCallback((key, loading, priority = 0) => {
        setStates(prev => ({
            ...prev,
            [key]: loading ? { loading: true, priority } : undefined
        }));
    }, []);

    const isLoading = useCallback((key) => {
        return states[key]?.loading || false;
    }, [states]);

    const hasAnyLoading = useCallback(() => {
        return Object.values(states).some(state => state?.loading);
    }, [states]);

    const getHighestPriorityLoading = useCallback(() => {
        const loadingStates = Object.entries(states)
            .filter(([_, state]) => state?.loading)
            .map(([key, state]) => ({ key, priority: state.priority }));

        if (loadingStates.length === 0) return null;

        return loadingStates.reduce((highest, current) => 
            current.priority > highest.priority ? current : highest
        ).key;
    }, [states]);

    const clearAll = useCallback(() => {
        setStates({});
    }, []);

    return {
        setLoadingState,
        isLoading,
        hasAnyLoading,
        getHighestPriorityLoading,
        clearAll,
        states
    };
};

/**
 * Hook for skeleton loading states
 */
export const useSkeletonLoading = (count = 5) => {
    const [isSkeletonLoading, setIsSkeletonLoading] = useState(true);
    const [skeletonCount, setSkeletonCount] = useState(count);

    const showSkeleton = useCallback(() => {
        setIsSkeletonLoading(true);
    }, []);

    const hideSkeleton = useCallback(() => {
        setIsSkeletonLoading(false);
    }, []);

    const updateSkeletonCount = useCallback((newCount) => {
        setSkeletonCount(newCount);
    }, []);

    return {
        isSkeletonLoading,
        skeletonCount,
        showSkeleton,
        hideSkeleton,
        updateSkeletonCount
    };
};

export default useLoadingState;