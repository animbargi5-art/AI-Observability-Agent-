import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for managing localStorage with React state synchronization
 * Provides type-safe localStorage operations with automatic JSON serialization
 */
export const useLocalStorage = (key, defaultValue = null, options = {}) => {
    const {
        serialize = JSON.stringify,
        deserialize = JSON.parse,
        syncAcrossTabs = true
    } = options;

    // Initialize state with localStorage value or default
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? deserialize(item) : defaultValue;
        } catch (error) {
            console.warn(`Error reading localStorage key "${key}":`, error);
            return defaultValue;
        }
    });

    // Update localStorage when state changes
    const setValue = useCallback((value) => {
        try {
            // Allow value to be a function so we have the same API as useState
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            
            setStoredValue(valueToStore);
            
            if (valueToStore === null || valueToStore === undefined) {
                window.localStorage.removeItem(key);
            } else {
                window.localStorage.setItem(key, serialize(valueToStore));
            }
        } catch (error) {
            console.error(`Error setting localStorage key "${key}":`, error);
        }
    }, [key, serialize, storedValue]);

    // Remove item from localStorage
    const removeValue = useCallback(() => {
        try {
            setStoredValue(null);
            window.localStorage.removeItem(key);
        } catch (error) {
            console.error(`Error removing localStorage key "${key}":`, error);
        }
    }, [key]);

    // Listen for changes in other tabs/windows
    useEffect(() => {
        if (!syncAcrossTabs) return;

        const handleStorageChange = (e) => {
            if (e.key === key && e.storageArea === window.localStorage) {
                try {
                    const newValue = e.newValue ? deserialize(e.newValue) : null;
                    setStoredValue(newValue);
                } catch (error) {
                    console.warn(`Error parsing localStorage change for key "${key}":`, error);
                }
            }
        };

        window.addEventListener('storage', handleStorageChange);
        return () => window.removeEventListener('storage', handleStorageChange);
    }, [key, deserialize, syncAcrossTabs]);

    return [storedValue, setValue, removeValue];
};

/**
 * Hook for managing user preferences in localStorage
 */
export const useUserPreferences = () => {
    const [preferences, setPreferences, removePreferences] = useLocalStorage('tattvaai-user-preferences', {
        theme: 'light',
        sidebarCollapsed: false,
        dashboardRefreshInterval: 30000,
        investigationAutoRefresh: true,
        notificationsEnabled: true,
        soundEnabled: false,
        language: 'en',
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        dateFormat: 'YYYY-MM-DD',
        timeFormat: '24h'
    });

    const updatePreference = useCallback((key, value) => {
        setPreferences(prev => ({
            ...prev,
            [key]: value
        }));
    }, [setPreferences]);

    const resetPreferences = useCallback(() => {
        removePreferences();
    }, [removePreferences]);

    const getPreference = useCallback((key, defaultValue = null) => {
        return preferences?.[key] ?? defaultValue;
    }, [preferences]);

    return {
        preferences,
        updatePreference,
        resetPreferences,
        getPreference,
        
        // Convenience getters for common preferences
        theme: getPreference('theme', 'light'),
        sidebarCollapsed: getPreference('sidebarCollapsed', false),
        dashboardRefreshInterval: getPreference('dashboardRefreshInterval', 30000),
        investigationAutoRefresh: getPreference('investigationAutoRefresh', true),
        notificationsEnabled: getPreference('notificationsEnabled', true),
        soundEnabled: getPreference('soundEnabled', false),
        language: getPreference('language', 'en'),
        timezone: getPreference('timezone', Intl.DateTimeFormat().resolvedOptions().timeZone),
        dateFormat: getPreference('dateFormat', 'YYYY-MM-DD'),
        timeFormat: getPreference('timeFormat', '24h')
    };
};

/**
 * Hook for managing session data in localStorage
 */
export const useSessionData = () => {
    const [sessionData, setSessionData, removeSession] = useLocalStorage('tattvaai-session', {
        lastVisitedPage: '/dashboard',
        recentSearches: [],
        openTabs: [],
        filters: {},
        selectedItems: []
    }, { syncAcrossTabs: false }); // Don't sync session data across tabs

    const updateSessionData = useCallback((key, value) => {
        setSessionData(prev => ({
            ...prev,
            [key]: value
        }));
    }, [setSessionData]);

    const addRecentSearch = useCallback((search) => {
        setSessionData(prev => {
            const searches = prev.recentSearches || [];
            const newSearches = [search, ...searches.filter(s => s !== search)].slice(0, 10);
            return {
                ...prev,
                recentSearches: newSearches
            };
        });
    }, [setSessionData]);

    const clearRecentSearches = useCallback(() => {
        updateSessionData('recentSearches', []);
    }, [updateSessionData]);

    const setLastVisitedPage = useCallback((page) => {
        updateSessionData('lastVisitedPage', page);
    }, [updateSessionData]);

    const updateFilters = useCallback((filterType, filters) => {
        setSessionData(prev => ({
            ...prev,
            filters: {
                ...prev.filters,
                [filterType]: filters
            }
        }));
    }, [setSessionData]);

    const clearFilters = useCallback((filterType = null) => {
        if (filterType) {
            setSessionData(prev => ({
                ...prev,
                filters: {
                    ...prev.filters,
                    [filterType]: {}
                }
            }));
        } else {
            updateSessionData('filters', {});
        }
    }, [setSessionData, updateSessionData]);

    return {
        sessionData,
        updateSessionData,
        removeSession,
        
        // Specific actions
        addRecentSearch,
        clearRecentSearches,
        setLastVisitedPage,
        updateFilters,
        clearFilters,
        
        // Getters
        lastVisitedPage: sessionData?.lastVisitedPage || '/dashboard',
        recentSearches: sessionData?.recentSearches || [],
        filters: sessionData?.filters || {},
        selectedItems: sessionData?.selectedItems || []
    };
};

/**
 * Hook for managing form data persistence
 */
export const usePersistedForm = (formId, initialValues = {}) => {
    const storageKey = `tattvaai-form-${formId}`;
    const [formData, setFormData] = useLocalStorage(storageKey, initialValues, {
        syncAcrossTabs: false
    });

    const updateField = useCallback((fieldName, value) => {
        setFormData(prev => ({
            ...prev,
            [fieldName]: value
        }));
    }, [setFormData]);

    const updateFields = useCallback((fields) => {
        setFormData(prev => ({
            ...prev,
            ...fields
        }));
    }, [setFormData]);

    const resetForm = useCallback(() => {
        setFormData(initialValues);
    }, [setFormData, initialValues]);

    const clearForm = useCallback(() => {
        setFormData(null);
    }, [setFormData]);

    return {
        formData: formData || initialValues,
        updateField,
        updateFields,
        resetForm,
        clearForm,
        
        // Validation helpers
        isDirty: JSON.stringify(formData) !== JSON.stringify(initialValues),
        hasData: formData && Object.keys(formData).length > 0
    };
};

export default useLocalStorage;