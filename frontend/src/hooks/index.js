// Custom Hooks for TattvaAI Frontend

// Investigation-related hooks
export { useInvestigation, useInvestigations } from './useInvestigation';

// Dashboard hooks
export { useDashboard } from './useDashboard';

// UI and interaction hooks
export { useToast } from './useToast';
export { useConfirmDialog } from './useConfirmDialog';

// Real-time communication hooks
export { useWebSocket, useWebSocketSubscription } from './useWebSocket';

// Data persistence hooks
export { 
    useLocalStorage, 
    useUserPreferences, 
    useSessionData, 
    usePersistedForm 
} from './useLocalStorage';

// Performance and UX hooks
export { 
    useDebounce, 
    useDebounceCallback, 
    useSearchDebounce, 
    useApiDebounce, 
    useValidationDebounce, 
    useAutoSave 
} from './useDebounce';

// Async operation hooks
export {
    useAsync,
    useAsyncRetry,
    useAsyncQueue,
    useAsyncUpload
} from './useAsync';

// Error handling hooks
export { useErrorHandler } from './useErrorHandler';

// Loading state hooks
export { 
    useLoadingState, 
    useAsyncOperation, 
    useMultipleLoadingStates, 
    useSkeletonLoading 
} from './useLoadingState';

// Re-export default hooks for convenience
export { default as useInvestigation } from './useInvestigation';
export { default as useDashboard } from './useDashboard';
export { default as useToast } from './useToast';
export { default as useConfirmDialog } from './useConfirmDialog';
export { default as useWebSocket } from './useWebSocket';
export { default as useLocalStorage } from './useLocalStorage';
export { default as useDebounce } from './useDebounce';
export { default as useAsync } from './useAsync';
export { default as useErrorHandler } from './useErrorHandler';
export { default as useLoadingState } from './useLoadingState';