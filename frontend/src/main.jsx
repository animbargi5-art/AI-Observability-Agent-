import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { PrimeReactProvider } from "primereact/api";

// Import organized stylesheet
import "./styles/index.css";

// Import interceptors to initialize global error handling
import "./api/interceptors.js";

import App from "./App.jsx";

// Create QueryClient instance for TanStack Query
const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: 2,
            retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
            staleTime: 5 * 60 * 1000, // 5 minutes
            gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
            refetchOnWindowFocus: false,
        },
        mutations: {
            retry: 1,
        },
    },
});

// PrimeReact configuration
const primeConfig = {
    ripple: true,
    inputStyle: 'outlined',
    locale: 'en',
    appendTo: 'self',
    autoZIndex: true,
    hideOverlaysOnDocumentScrolling: false,
    nonce: undefined,
    nullSortOrder: 1,
    zIndex: {
        modal: 1100,
        overlay: 1000,
        menu: 1000,
        tooltip: 1100,
        toast: 1200
    }
};

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <QueryClientProvider client={queryClient}>
            <PrimeReactProvider value={primeConfig}>
                <BrowserRouter>
                    <App />
                </BrowserRouter>
            </PrimeReactProvider>
        </QueryClientProvider>
    </StrictMode>
);