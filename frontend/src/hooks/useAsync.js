import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Custom hook for managing async operations
 * Provides loading, error, and data states for async functions
 */
export const useAsync = (asyncFunction, dependencies = [], options = {}) => {
    const {
        immediate = true,
        onSuccess,
        onError,
        initialData = null
    } = options;

    const [state, setState] = useState({
        data: initialData,
        loading: false,
        error: null
    });

    const cancelRef = useRef(false);

    const execute = useCallback(async (...args) => {
        setState(prev => ({ ...prev, loading: true, error: null }));
        cancelRef.current = false;

        try {
            const result = await asyncFunction(...args);
            
            if (!cancelRef.current) {
                setState(prev => ({ ...prev, data: result, loading: false }));
                onSuccess?.(result);
            }
            
            return result;
        } catch (error) {
            if (!cancelRef.current) {
                setState(prev => ({ ...prev, error, loading: false }));
                onError?.(error);
            }
            throw error;
        }
    }, [asyncFunction, onSuccess, onError]);

    const reset = useCallback(() => {
        setState({
            data: initialData,
            loading: false,
            error: null
        });
    }, [initialData]);

    const cancel = useCallback(() => {
        cancelRef.current = true;
        setState(prev => ({ ...prev, loading: false }));
    }, []);

    // Execute on mount if immediate is true
    useEffect(() => {
        if (immediate && asyncFunction) {
            execute();
        }

        return () => {
            cancel();
        };
    }, dependencies); // eslint-disable-line react-hooks/exhaustive-deps

    return {
        ...state,
        execute,
        reset,
        cancel
    };
};

/**
 * Hook for handling async operations with retry logic
 */
export const useAsyncRetry = (asyncFunction, dependencies = [], options = {}) => {
    const {
        maxRetries = 3,
        retryDelay = 1000,
        backoffMultiplier = 2,
        ...asyncOptions
    } = options;

    const [retryCount, setRetryCount] = useState(0);
    const retryTimeoutRef = useRef(null);

    const executeWithRetry = useCallback(async (...args) => {
        try {
            const result = await asyncFunction(...args);
            setRetryCount(0); // Reset retry count on success
            return result;
        } catch (error) {
            if (retryCount < maxRetries) {
                const delay = retryDelay * Math.pow(backoffMultiplier, retryCount);
                
                return new Promise((resolve, reject) => {
                    retryTimeoutRef.current = setTimeout(async () => {
                        setRetryCount(prev => prev + 1);
                        try {
                            const result = await executeWithRetry(...args);
                            resolve(result);
                        } catch (retryError) {
                            reject(retryError);
                        }
                    }, delay);
                });
            }
            throw error;
        }
    }, [asyncFunction, retryCount, maxRetries, retryDelay, backoffMultiplier]);

    const { execute: originalExecute, ...asyncState } = useAsync(
        executeWithRetry,
        dependencies,
        asyncOptions
    );

    const cancel = useCallback(() => {
        if (retryTimeoutRef.current) {
            clearTimeout(retryTimeoutRef.current);
        }
        setRetryCount(0);
        asyncState.cancel();
    }, [asyncState]);

    const reset = useCallback(() => {
        setRetryCount(0);
        asyncState.reset();
    }, [asyncState]);

    useEffect(() => {
        return () => {
            if (retryTimeoutRef.current) {
                clearTimeout(retryTimeoutRef.current);
            }
        };
    }, []);

    return {
        ...asyncState,
        execute: originalExecute,
        cancel,
        reset,
        retryCount,
        isRetrying: retryCount > 0,
        maxRetries
    };
};

/**
 * Hook for managing multiple async operations
 */
export const useAsyncQueue = (options = {}) => {
    const { 
        concurrency = 1, // Number of concurrent operations
        onComplete,
        onProgress 
    } = options;

    const [queue, setQueue] = useState([]);
    const [running, setRunning] = useState([]);
    const [completed, setCompleted] = useState([]);
    const [errors, setErrors] = useState([]);

    const addToQueue = useCallback((asyncFunction, id = Date.now()) => {
        const operation = {
            id,
            function: asyncFunction,
            status: 'pending',
            result: null,
            error: null
        };

        setQueue(prev => [...prev, operation]);
        return id;
    }, []);

    const removeFromQueue = useCallback((id) => {
        setQueue(prev => prev.filter(op => op.id !== id));
    }, []);

    const clearQueue = useCallback(() => {
        setQueue([]);
        setRunning([]);
        setCompleted([]);
        setErrors([]);
    }, []);

    const processQueue = useCallback(async () => {
        if (running.length >= concurrency || queue.length === 0) {
            return;
        }

        const nextOperation = queue[0];
        setQueue(prev => prev.slice(1));
        setRunning(prev => [...prev, nextOperation]);

        try {
            const result = await nextOperation.function();
            
            setRunning(prev => prev.filter(op => op.id !== nextOperation.id));
            setCompleted(prev => [...prev, { ...nextOperation, result, status: 'completed' }]);
            
            onProgress?.({
                completed: completed.length + 1,
                total: completed.length + errors.length + running.length + queue.length + 1,
                current: nextOperation
            });
        } catch (error) {
            setRunning(prev => prev.filter(op => op.id !== nextOperation.id));
            setErrors(prev => [...prev, { ...nextOperation, error, status: 'error' }]);
            
            onProgress?.({
                completed: completed.length,
                total: completed.length + errors.length + 1 + running.length + queue.length,
                current: nextOperation,
                error
            });
        }

        // Process next item in queue
        setTimeout(processQueue, 0);
    }, [queue, running, completed, errors, concurrency, onProgress]);

    // Auto-process queue when items are added
    useEffect(() => {
        processQueue();
    }, [processQueue]);

    // Notify when all operations complete
    useEffect(() => {
        const totalOperations = completed.length + errors.length;
        const allCompleted = queue.length === 0 && running.length === 0 && totalOperations > 0;
        
        if (allCompleted) {
            onComplete?.({
                completed: completed.length,
                errors: errors.length,
                results: completed,
                errorResults: errors
            });
        }
    }, [queue.length, running.length, completed, errors, onComplete]);

    const isActive = queue.length > 0 || running.length > 0;
    const progress = {
        total: queue.length + running.length + completed.length + errors.length,
        completed: completed.length,
        errors: errors.length,
        pending: queue.length,
        running: running.length
    };

    return {
        addToQueue,
        removeFromQueue,
        clearQueue,
        isActive,
        progress,
        queue,
        running,
        completed,
        errors
    };
};

/**
 * Hook for handling file uploads with progress tracking
 */
export const useAsyncUpload = (uploadFunction, options = {}) => {
    const {
        onProgress,
        onComplete,
        onError,
        allowMultiple = false
    } = options;

    const [uploads, setUploads] = useState([]);

    const upload = useCallback(async (file, uploadId = Date.now()) => {
        const uploadState = {
            id: uploadId,
            file,
            progress: 0,
            status: 'uploading',
            result: null,
            error: null
        };

        setUploads(prev => {
            if (!allowMultiple) {
                return [uploadState];
            }
            return [...prev, uploadState];
        });

        try {
            const result = await uploadFunction(file, (progress) => {
                setUploads(prev => prev.map(upload => 
                    upload.id === uploadId 
                        ? { ...upload, progress }
                        : upload
                ));
                onProgress?.(progress, file, uploadId);
            });

            setUploads(prev => prev.map(upload => 
                upload.id === uploadId 
                    ? { ...upload, status: 'completed', result, progress: 100 }
                    : upload
            ));

            onComplete?.(result, file, uploadId);
            return result;
        } catch (error) {
            setUploads(prev => prev.map(upload => 
                upload.id === uploadId 
                    ? { ...upload, status: 'error', error }
                    : upload
            ));

            onError?.(error, file, uploadId);
            throw error;
        }
    }, [uploadFunction, allowMultiple, onProgress, onComplete, onError]);

    const removeUpload = useCallback((uploadId) => {
        setUploads(prev => prev.filter(upload => upload.id !== uploadId));
    }, []);

    const clearUploads = useCallback(() => {
        setUploads([]);
    }, []);

    const getUploadById = useCallback((uploadId) => {
        return uploads.find(upload => upload.id === uploadId);
    }, [uploads]);

    const totalProgress = uploads.length > 0 
        ? uploads.reduce((sum, upload) => sum + upload.progress, 0) / uploads.length 
        : 0;

    return {
        upload,
        uploads,
        removeUpload,
        clearUploads,
        getUploadById,
        totalProgress,
        isUploading: uploads.some(upload => upload.status === 'uploading'),
        hasErrors: uploads.some(upload => upload.status === 'error'),
        allCompleted: uploads.length > 0 && uploads.every(upload => upload.status === 'completed')
    };
};

export default useAsync;