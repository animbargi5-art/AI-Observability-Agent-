import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Custom hook for debouncing values
 * Delays updating the debounced value until after the specified delay
 */
export const useDebounce = (value, delay = 300) => {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);

    return debouncedValue;
};

/**
 * Custom hook for debouncing callbacks
 * Returns a debounced version of the callback function
 */
export const useDebounceCallback = (callback, delay = 300, deps = []) => {
    const timeoutRef = useRef(null);
    const callbackRef = useRef(callback);

    // Update callback ref when dependencies change
    useEffect(() => {
        callbackRef.current = callback;
    }, [callback, ...deps]);

    const debouncedCallback = useCallback((...args) => {
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        timeoutRef.current = setTimeout(() => {
            callbackRef.current(...args);
        }, delay);
    }, [delay]);

    // Cleanup timeout on unmount
    useEffect(() => {
        return () => {
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }
        };
    }, []);

    // Cancel function to manually cancel pending debounced calls
    const cancel = useCallback(() => {
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
            timeoutRef.current = null;
        }
    }, []);

    // Flush function to immediately execute pending debounced call
    const flush = useCallback((...args) => {
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
            timeoutRef.current = null;
        }
        callbackRef.current(...args);
    }, []);

    return {
        debouncedCallback,
        cancel,
        flush,
        isPending: () => timeoutRef.current !== null
    };
};

/**
 * Hook for debounced search functionality
 * Commonly used pattern for search inputs
 */
export const useSearchDebounce = (initialValue = '', delay = 300) => {
    const [searchTerm, setSearchTerm] = useState(initialValue);
    const [isSearching, setIsSearching] = useState(false);
    const debouncedSearchTerm = useDebounce(searchTerm, delay);

    // Track when search is in progress
    useEffect(() => {
        if (searchTerm !== debouncedSearchTerm) {
            setIsSearching(true);
        } else {
            setIsSearching(false);
        }
    }, [searchTerm, debouncedSearchTerm]);

    const clearSearch = useCallback(() => {
        setSearchTerm('');
    }, []);

    const setSearch = useCallback((value) => {
        setSearchTerm(value);
    }, []);

    return {
        searchTerm,
        debouncedSearchTerm,
        isSearching,
        setSearch,
        clearSearch,
        hasSearch: debouncedSearchTerm.length > 0
    };
};

/**
 * Hook for debounced API calls
 * Prevents excessive API calls while user is typing
 */
export const useApiDebounce = (apiCall, delay = 500, deps = []) => {
    const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const { debouncedCallback, cancel } = useDebounceCallback(
        async (...args) => {
            if (!apiCall) return;

            setIsLoading(true);
            setError(null);

            try {
                const result = await apiCall(...args);
                setData(result);
            } catch (err) {
                setError(err);
                setData(null);
            } finally {
                setIsLoading(false);
            }
        },
        delay,
        deps
    );

    const execute = useCallback((...args) => {
        debouncedCallback(...args);
    }, [debouncedCallback]);

    const reset = useCallback(() => {
        cancel();
        setIsLoading(false);
        setData(null);
        setError(null);
    }, [cancel]);

    return {
        execute,
        reset,
        cancel,
        data,
        error,
        isLoading
    };
};

/**
 * Hook for debounced form validation
 * Delays validation until user stops typing
 */
export const useValidationDebounce = (validationFn, delay = 300) => {
    const [validationState, setValidationState] = useState({
        isValidating: false,
        isValid: null,
        errors: null
    });

    const { debouncedCallback } = useDebounceCallback(
        async (value) => {
            if (!validationFn) return;

            setValidationState(prev => ({ ...prev, isValidating: true }));

            try {
                const result = await validationFn(value);
                setValidationState({
                    isValidating: false,
                    isValid: result.isValid || !result.errors?.length,
                    errors: result.errors || null
                });
            } catch (error) {
                setValidationState({
                    isValidating: false,
                    isValid: false,
                    errors: [error.message || 'Validation error']
                });
            }
        },
        delay
    );

    const validate = useCallback((value) => {
        setValidationState(prev => ({ ...prev, isValidating: true }));
        debouncedCallback(value);
    }, [debouncedCallback]);

    const reset = useCallback(() => {
        setValidationState({
            isValidating: false,
            isValid: null,
            errors: null
        });
    }, []);

    return {
        validate,
        reset,
        ...validationState
    };
};

/**
 * Hook for auto-save functionality with debouncing
 * Automatically saves data after user stops making changes
 */
export const useAutoSave = (saveFunction, data, delay = 2000, options = {}) => {
    const { 
        enabled = true, 
        skipInitialSave = true,
        onSaveStart,
        onSaveSuccess,
        onSaveError 
    } = options;

    const [saveState, setSaveState] = useState({
        isSaving: false,
        lastSaved: null,
        error: null
    });

    const initialRenderRef = useRef(true);
    const lastSavedDataRef = useRef(null);

    const { debouncedCallback, cancel } = useDebounceCallback(
        async (dataToSave) => {
            if (!enabled || !saveFunction) return;

            // Skip if data hasn't changed
            if (JSON.stringify(dataToSave) === JSON.stringify(lastSavedDataRef.current)) {
                return;
            }

            setSaveState(prev => ({ ...prev, isSaving: true, error: null }));
            onSaveStart?.();

            try {
                await saveFunction(dataToSave);
                lastSavedDataRef.current = dataToSave;
                setSaveState(prev => ({
                    ...prev,
                    isSaving: false,
                    lastSaved: new Date(),
                    error: null
                }));
                onSaveSuccess?.();
            } catch (error) {
                setSaveState(prev => ({
                    ...prev,
                    isSaving: false,
                    error: error.message || 'Save failed'
                }));
                onSaveError?.(error);
            }
        },
        delay
    );

    // Auto-save when data changes
    useEffect(() => {
        if (skipInitialSave && initialRenderRef.current) {
            initialRenderRef.current = false;
            return;
        }

        if (enabled && data !== undefined && data !== null) {
            debouncedCallback(data);
        }

        return cancel;
    }, [data, enabled, debouncedCallback, cancel, skipInitialSave]);

    const saveNow = useCallback(async () => {
        cancel(); // Cancel any pending auto-save
        if (saveFunction && data !== undefined && data !== null) {
            try {
                setSaveState(prev => ({ ...prev, isSaving: true, error: null }));
                await saveFunction(data);
                lastSavedDataRef.current = data;
                setSaveState(prev => ({
                    ...prev,
                    isSaving: false,
                    lastSaved: new Date(),
                    error: null
                }));
                onSaveSuccess?.();
            } catch (error) {
                setSaveState(prev => ({
                    ...prev,
                    isSaving: false,
                    error: error.message || 'Save failed'
                }));
                onSaveError?.(error);
                throw error;
            }
        }
    }, [data, saveFunction, cancel, onSaveSuccess, onSaveError]);

    const hasUnsavedChanges = JSON.stringify(data) !== JSON.stringify(lastSavedDataRef.current);

    return {
        ...saveState,
        saveNow,
        cancel,
        hasUnsavedChanges
    };
};

export default useDebounce;