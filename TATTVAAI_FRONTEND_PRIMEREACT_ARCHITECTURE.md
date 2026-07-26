# TattvaAI - Frontend PrimeReact Architecture

**AI-Powered Autonomous Incident Investigation Platform - Frontend Implementation**

**Version:** 1.0  
**Framework:** React 19.2.7 + Vite 8.1.1 + PrimeReact  
**Target Audience:** Frontend Developers, UI/UX Designers, Technical Judges

---

## 1. Executive Summary

TattvaAI's frontend is built using **PrimeReact**, a comprehensive React UI component library that provides enterprise-grade components, themes, and accessibility features. The frontend serves as the primary interface for Site Reliability Engineers (SREs) to interact with AI-powered incident investigations.

### Core Technology Stack

- **React 19.2.7** - Latest React with concurrent features
- **PrimeReact 10.x** - Enterprise UI component library
- **Vite 8.1.1** - Next-generation frontend tooling
- **React Router DOM 7.x** - Client-side routing
- **Axios** - HTTP client for API communication
- **ReactFlow 11.x** - Interactive node-based graphs
- **Recharts 3.x** - Data visualization charts

---

## 2. Why PrimeReact?

### Enterprise-Grade Components
PrimeReact provides production-ready components specifically designed for enterprise applications:

- **DataTable** - Advanced grid with filtering, sorting, pagination
- **Timeline** - Investigation step visualization
- **Tree** - Service dependency hierarchies
- **Chart.js Integration** - Statistical reporting
- **Dialog** - Modal investigation details
- **TabView** - Multi-panel evidence display

### Design System Benefits
- **Consistent Look & Feel** - Unified design language
- **Accessibility Compliant** - WCAG 2.1 AA standards
- **Responsive Design** - Mobile-first approach
- **Theme Customization** - Brand alignment capabilities
- **RTL Support** - International accessibility

### Developer Experience
- **TypeScript Support** - Type-safe development
- **Comprehensive Documentation** - Detailed API reference
- **Active Community** - Regular updates and support
- **Performance Optimized** - Lazy loading and virtualization

---

## 3. Application Architecture

### High-Level Structure
```
src/
├── components/          # Reusable PrimeReact-based components
├── pages/              # Route-level page components
├── layouts/            # Layout wrapper components
├── services/           # API communication layer
├── hooks/              # Custom React hooks
├── utils/              # Helper functions and utilities
├── styles/             # Global styles and PrimeReact themes
└── types/              # TypeScript type definitions
```

### Component Hierarchy
```
App (PrimeReact Provider)
├── MainLayout (Sidebar + Content)
│   ├── Sidebar (PrimeReact Menu)
│   └── Router Outlet
│       ├── Dashboard Page
│       ├── Investigation Page
│       ├── History Page
│       └── Reports Page
```
## 4. PrimeReact Component Mapping

### Dashboard Components

#### Investigation Status Card
**PrimeReact Components:** `Card`, `Tag`, `Button`
```jsx
<Card className="investigation-status-card">
    <div className="flex align-items-center justify-content-between">
        <div className="flex align-items-center">
            <i className="pi pi-circle-fill text-green-500 mr-2"></i>
            <span className="text-xl font-semibold">IDLE - Ready</span>
        </div>
        <Tag severity="success" value="Online"></Tag>
    </div>
</Card>
```

#### Statistics Cards
**PrimeReact Components:** `Card`, `Badge`, `Skeleton`
```jsx
<Card className="statistic-card">
    <div className="flex align-items-center justify-content-between">
        <div>
            <div className="text-2xl font-bold text-900">{value}</div>
            <div className="text-600">{label}</div>
        </div>
        <Badge value={badge} severity={severity} />
    </div>
</Card>
```

#### Investigation List
**PrimeReact Components:** `DataTable`, `Column`, `Tag`, `Button`
```jsx
<DataTable 
    value={investigations} 
    paginator 
    rows={10}
    loading={loading}
    className="investigation-table"
>
    <Column field="id" header="Investigation ID" />
    <Column field="severity" header="Severity" body={severityTemplate} />
    <Column field="confidence" header="Confidence" body={confidenceTemplate} />
    <Column field="status" header="Status" body={statusTemplate} />
    <Column body={actionTemplate} header="Actions" />
</DataTable>
```

### Investigation Details Components

#### Investigation Progress
**PrimeReact Components:** `Steps`, `ProgressBar`, `Timeline`
```jsx
<Steps 
    model={progressSteps} 
    activeIndex={currentStep}
    className="investigation-progress"
/>

<Timeline 
    value={events} 
    content={timelineTemplate}
    className="investigation-timeline"
/>
```

#### Evidence Panel
**PrimeReact Components:** `TabView`, `TabPanel`, `Card`, `Chip`
```jsx
<TabView className="evidence-tabs">
    <TabPanel header="Traces">
        <Card className="evidence-card">
            <div className="flex flex-wrap gap-2 mb-3">
                <Chip label="Critical" className="bg-red-100 text-red-900" />
                <Chip label="Checkout Service" className="bg-blue-100 text-blue-900" />
            </div>
            <div className="evidence-content">{traceEvidence}</div>
        </Card>
    </TabPanel>
    <TabPanel header="Logs">{logEvidence}</TabPanel>
    <TabPanel header="Metrics">{metricEvidence}</TabPanel>
</TabView>
```
#### Root Cause Analysis
**PrimeReact Components:** `Panel`, `ProgressBar`, `Tag`, `Accordion`
```jsx
<Panel header="Root Cause Analysis" className="root-cause-panel">
    <div className="mb-4">
        <div className="flex align-items-center justify-content-between mb-2">
            <span className="font-semibold">Database Connection Pool Exhausted</span>
            <Tag severity="danger" value="96% Confidence" />
        </div>
        <ProgressBar value={96} className="confidence-bar" />
    </div>
    
    <Accordion multiple>
        <AccordionTab header="Supporting Evidence">
            <ul className="list-none p-0">
                <li className="flex align-items-center mb-2">
                    <i className="pi pi-check-circle text-green-500 mr-2"></i>
                    Trace Analysis
                </li>
                <li className="flex align-items-center mb-2">
                    <i className="pi pi-check-circle text-green-500 mr-2"></i>
                    Log Analysis
                </li>
            </ul>
        </AccordionTab>
    </Accordion>
</Panel>
```

#### Recommendations Panel
**PrimeReact Components:** `DataView`, `Button`, `Tag`, `Divider`
```jsx
<DataView 
    value={recommendations} 
    layout="list"
    itemTemplate={recommendationTemplate}
    header="Recommendations"
/>

const recommendationTemplate = (recommendation) => (
    <div className="col-12 surface-border border-bottom-1 pb-3 mb-3">
        <div className="flex align-items-start justify-content-between">
            <div className="flex flex-column">
                <span className="font-semibold text-900 mb-2">{recommendation.title}</span>
                <p className="text-600 mb-3">{recommendation.description}</p>
                <div className="flex gap-2">
                    <Tag severity={recommendation.priority} value={recommendation.urgency} />
                    <Tag severity="info" value={recommendation.category} />
                </div>
            </div>
            <Button 
                icon="pi pi-external-link" 
                className="p-button-text"
                onClick={() => openRecommendation(recommendation)}
            />
        </div>
    </div>
);
```

### History & Reports Components

#### Search & Filtering
**PrimeReact Components:** `InputText`, `Dropdown`, `MultiSelect`, `Calendar`
```jsx
<div className="flex gap-3 mb-4 filter-bar">
    <span className="p-input-icon-left">
        <i className="pi pi-search" />
        <InputText 
            placeholder="Search investigations..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
        />
    </span>
    
    <Dropdown 
        value={severityFilter} 
        options={severityOptions}
        onChange={(e) => setSeverityFilter(e.value)}
        placeholder="Severity"
    />
    
    <MultiSelect 
        value={statusFilter} 
        options={statusOptions}
        onChange={(e) => setStatusFilter(e.value)}
        placeholder="Status"
        display="chip"
    />
    
    <Calendar 
        value={dateRange} 
        onChange={(e) => setDateRange(e.value)}
        selectionMode="range"
        placeholder="Date Range"
    />
</div>
```
#### Reports Dashboard
**PrimeReact Components:** `Chart`, `Card`, `DataTable`, `Knob`
```jsx
<div className="grid">
    <div className="col-12 md:col-6 lg:col-3">
        <Card className="text-center">
            <Knob 
                value={totalInvestigations} 
                max={1000}
                valueTemplate="{value}"
                className="knob-chart"
            />
            <div className="text-600 mt-2">Total Investigations</div>
        </Card>
    </div>
    
    <div className="col-12 md:col-6">
        <Card>
            <Chart 
                type="doughnut" 
                data={severityChartData}
                options={chartOptions}
                className="severity-chart"
            />
        </Card>
    </div>
    
    <div className="col-12">
        <Card>
            <Chart 
                type="line" 
                data={trendChartData}
                options={trendChartOptions}
                className="trend-chart"
            />
        </Card>
    </div>
</div>
```

## 5. Layout Architecture

### Main Layout Structure
**PrimeReact Components:** `Menubar`, `Sidebar`, `Toast`, `ConfirmDialog`
```jsx
const MainLayout = ({ children }) => (
    <div className="layout-wrapper">
        <Menubar 
            model={menuItems}
            start={brandTemplate}
            end={userTemplate}
            className="main-menubar"
        />
        
        <div className="layout-content">
            <Sidebar 
                visible={sidebarVisible}
                onHide={() => setSidebarVisible(false)}
                className="layout-sidebar"
            >
                <Menu model={navigationItems} />
            </Sidebar>
            
            <div className="main-content">
                {children}
            </div>
        </div>
        
        <Toast ref={toastRef} position="top-right" />
        <ConfirmDialog />
    </div>
);
```

### Responsive Navigation
**PrimeReact Components:** `Menu`, `Button`, `Avatar`
```jsx
const NavigationMenu = () => {
    const menuItems = [
        {
            label: 'Dashboard',
            icon: 'pi pi-home',
            command: () => navigate('/dashboard')
        },
        {
            label: 'Investigations',
            icon: 'pi pi-search',
            items: [
                {
                    label: 'Active',
                    icon: 'pi pi-play',
                    command: () => navigate('/investigations/active')
                },
                {
                    label: 'History',
                    icon: 'pi pi-history',
                    command: () => navigate('/investigations/history')
                }
            ]
        },
        {
            label: 'Reports',
            icon: 'pi pi-chart-bar',
            command: () => navigate('/reports')
        }
    ];

    return (
        <Menu 
            model={menuItems} 
            className="navigation-menu"
        />
    );
};
```
## 6. State Management & Data Flow

### Investigation State Management
**React Hooks + PrimeReact Integration**
```jsx
const useInvestigationState = () => {
    const [investigation, setInvestigation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const toast = useRef(null);

    const startInvestigation = async () => {
        setLoading(true);
        try {
            const response = await investigationService.start();
            setInvestigation(response.data);
            toast.current.show({
                severity: 'info',
                summary: 'Investigation Started',
                detail: 'AI agents are analyzing telemetry data'
            });
        } catch (error) {
            toast.current.show({
                severity: 'error',
                summary: 'Investigation Failed',
                detail: error.message
            });
        } finally {
            setLoading(false);
        }
    };

    return {
        investigation,
        loading,
        progress,
        startInvestigation,
        toast
    };
};
```

### Real-time Updates with WebSockets
**PrimeReact Toast + Progress Integration**
```jsx
const useRealtimeInvestigation = (investigationId) => {
    const [progress, setProgress] = useState(0);
    const [currentStep, setCurrentStep] = useState('');
    const toast = useRef(null);

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8000/investigations/${investigationId}/progress`);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            setProgress(data.progress);
            setCurrentStep(data.step);
            
            toast.current.show({
                severity: 'info',
                summary: data.step,
                detail: data.message,
                life: 3000
            });
        };

        return () => ws.close();
    }, [investigationId]);

    return { progress, currentStep };
};
```

### API Service Layer
**Axios + PrimeReact Error Handling**
```jsx
class InvestigationService {
    constructor() {
        this.api = axios.create({
            baseURL: process.env.VITE_API_BASE_URL,
            timeout: 30000
        });
        
        this.setupInterceptors();
    }

    setupInterceptors() {
        this.api.interceptors.response.use(
            (response) => response,
            (error) => {
                // Global error handling with PrimeReact Toast
                const message = error.response?.data?.detail || 'An error occurred';
                
                // This will be caught by components and displayed via Toast
                return Promise.reject(new Error(message));
            }
        );
    }

    async startInvestigation() {
        const response = await this.api.post('/investigations/start');
        return response.data;
    }

    async getInvestigationDetails(id) {
        const response = await this.api.get(`/investigations/${id}`);
        return response.data;
    }

    async getInvestigationHistory(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await this.api.get(`/investigations/history?${params}`);
        return response.data;
    }
}
```
## 7. Styling & Theming

### PrimeReact Theme Configuration
```jsx
// main.jsx
import { PrimeReactProvider } from 'primereact/api';
import 'primereact/resources/themes/lara-light-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';

const primeConfig = {
    ripple: true,
    inputStyle: 'outlined',
    locale: 'en',
    appendTo: 'self'
};

ReactDOM.createRoot(document.getElementById('root')).render(
    <PrimeReactProvider value={primeConfig}>
        <App />
    </PrimeReactProvider>
);
```

### Custom TattvaAI Theme
**CSS Custom Properties + PrimeReact Variables**
```css
/* styles/tattvaai-theme.css */
:root {
    --primary-color: #1976d2;
    --primary-color-text: #ffffff;
    --surface-0: #ffffff;
    --surface-50: #fafafa;
    --surface-100: #f5f5f5;
    --surface-200: #eeeeee;
    --text-color: #212529;
    --text-color-secondary: #6c757d;
    
    /* Investigation Status Colors */
    --success-color: #4caf50;
    --warning-color: #ff9800;
    --danger-color: #f44336;
    --info-color: #2196f3;
    
    /* Severity Colors */
    --severity-critical: #d32f2f;
    --severity-high: #f57c00;
    --severity-medium: #fbc02d;
    --severity-low: #388e3c;
}

/* Component-specific styling */
.investigation-status-card {
    border-left: 4px solid var(--success-color);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.investigation-progress .p-steps .p-steps-item.p-highlight .p-steps-number {
    background: var(--primary-color);
    color: var(--primary-color-text);
}

.evidence-card {
    border-radius: 8px;
    margin-bottom: 1rem;
    transition: box-shadow 0.3s ease;
}

.evidence-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

### Responsive Design with PrimeFlex
```jsx
// Responsive grid layout using PrimeFlex classes
<div className="grid">
    <div className="col-12 md:col-6 lg:col-4">
        <Card>Statistics Card 1</Card>
    </div>
    <div className="col-12 md:col-6 lg:col-4">
        <Card>Statistics Card 2</Card>
    </div>
    <div className="col-12 lg:col-4">
        <Card>Statistics Card 3</Card>
    </div>
</div>

// Flexible layout with gap utilities
<div className="flex flex-wrap gap-3 align-items-center justify-content-between mb-4">
    <div className="flex gap-2">
        <Button label="Start Investigation" severity="success" />
        <Button label="Refresh" severity="secondary" outlined />
    </div>
    <div className="flex gap-2">
        <InputText placeholder="Search..." />
        <Dropdown options={filterOptions} />
    </div>
</div>
```
## 8. Performance Optimization

### Lazy Loading with React.lazy + PrimeReact
```jsx
// Lazy-loaded pages with loading fallback
const Dashboard = React.lazy(() => import('./pages/DashboardPage'));
const Investigation = React.lazy(() => import('./pages/InvestigationPage'));
const History = React.lazy(() => import('./pages/HistoryPage'));
const Reports = React.lazy(() => import('./pages/ReportsPage'));

const AppRouter = () => (
    <Router>
        <Suspense fallback={
            <div className="flex align-items-center justify-content-center" style={{height: '100vh'}}>
                <ProgressSpinner />
            </div>
        }>
            <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/investigation/:id" element={<Investigation />} />
                <Route path="/history" element={<History />} />
                <Route path="/reports" element={<Reports />} />
            </Routes>
        </Suspense>
    </Router>
);
```

### Virtual Scrolling for Large Datasets
**PrimeReact DataTable with VirtualScrolling**
```jsx
const InvestigationHistoryTable = () => {
    const [investigations, setInvestigations] = useState([]);
    const [loading, setLoading] = useState(false);

    return (
        <DataTable 
            value={investigations}
            virtualScrollerOptions={{
                itemSize: 60,
                numToleratedItems: 10,
                scrollHeight: '400px'
            }}
            loading={loading}
            lazy
            paginator
            rows={50}
            totalRecords={totalRecords}
            onPage={onPageChange}
            className="investigation-history-table"
        >
            <Column field="id" header="ID" />
            <Column field="timestamp" header="Date" body={dateTemplate} />
            <Column field="severity" header="Severity" body={severityTemplate} />
            <Column field="status" header="Status" body={statusTemplate} />
            <Column field="confidence" header="Confidence" body={confidenceTemplate} />
        </DataTable>
    );
};
```

### Memoization for Complex Components
```jsx
// Memoized evidence panel to prevent unnecessary re-renders
const EvidencePanel = React.memo(({ evidence, loading }) => {
    const evidenceCards = useMemo(() => {
        return evidence.map(item => ({
            ...item,
            severityColor: getSeverityColor(item.severity),
            timestamp: formatTimestamp(item.timestamp)
        }));
    }, [evidence]);

    if (loading) {
        return (
            <div className="grid">
                {Array.from({length: 6}).map((_, i) => (
                    <div key={i} className="col-12 md:col-6">
                        <Skeleton height="200px" className="mb-3" />
                    </div>
                ))}
            </div>
        );
    }

    return (
        <DataView 
            value={evidenceCards}
            layout="grid"
            itemTemplate={evidenceCardTemplate}
            paginator
            rows={12}
        />
    );
});
```

## 9. Accessibility & Internationalization

### WCAG 2.1 AA Compliance
**PrimeReact Accessibility Features**
```jsx
// Proper ARIA labels and keyboard navigation
<DataTable 
    value={investigations}
    selectionMode="single"
    selection={selectedInvestigation}
    onSelectionChange={(e) => setSelectedInvestigation(e.value)}
    dataKey="id"
    tableStyle={{ minWidth: '60rem' }}
    aria-label="Investigation history table"
>
    <Column 
        field="severity" 
        header="Severity"
        body={(rowData) => (
            <Tag 
                value={rowData.severity}
                severity={getSeverityLevel(rowData.severity)}
                aria-label={`Severity: ${rowData.severity}`}
            />
        )}
    />
</DataTable>

// Accessible form inputs
<div className="field">
    <label htmlFor="search-input" className="block text-900 font-medium mb-2">
        Search Investigations
    </label>
    <InputText 
        id="search-input"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Enter investigation ID or description"
        className="w-full"
        aria-describedby="search-help"
    />
    <small id="search-help" className="block text-600 mt-1">
        Search by investigation ID, service name, or error description
    </small>
</div>
```
### Internationalization Support
**PrimeReact i18n Integration**
```jsx
// i18n configuration
import { locale, addLocale } from 'primereact/api';

const i18nConfig = {
    en: {
        startsWith: 'Starts with',
        contains: 'Contains',
        notContains: 'Not contains',
        endsWith: 'Ends with',
        equals: 'Equals',
        notEquals: 'Not equals',
        noFilter: 'No Filter',
        lt: 'Less than',
        lte: 'Less than or equal to',
        gt: 'Greater than',
        gte: 'Greater than or equal to',
        dateIs: 'Date is',
        dateIsNot: 'Date is not',
        dateBefore: 'Date is before',
        dateAfter: 'Date is after',
        clear: 'Clear',
        apply: 'Apply',
        matchAll: 'Match All',
        matchAny: 'Match Any',
        addRule: 'Add Rule',
        removeRule: 'Remove Rule',
        accept: 'Yes',
        reject: 'No',
        choose: 'Choose',
        upload: 'Upload',
        cancel: 'Cancel',
        dayNames: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        dayNamesShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        dayNamesMin: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        monthNamesShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        today: 'Today',
        weekHeader: 'Wk',
        firstDayOfWeek: 0,
        dateFormat: 'mm/dd/yy',
        weak: 'Weak',
        medium: 'Medium',
        strong: 'Strong',
        passwordPrompt: 'Enter a password',
        emptyFilterMessage: 'No results found',
        emptyMessage: 'No available options'
    }
};

addLocale('en', i18nConfig.en);
locale('en');
```

## 10. Testing Strategy

### Component Testing with React Testing Library
```jsx
// __tests__/components/Dashboard/InvestigationCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { PrimeReactProvider } from 'primereact/api';
import InvestigationCard from '../InvestigationCard';

const TestWrapper = ({ children }) => (
    <PrimeReactProvider value={{ ripple: false }}>
        {children}
    </PrimeReactProvider>
);

describe('InvestigationCard', () => {
    const mockInvestigation = {
        id: 'inv-123',
        severity: 'HIGH',
        confidence: 96,
        status: 'COMPLETED',
        timestamp: '2024-01-15T10:30:00Z',
        summary: 'Database connection pool exhausted'
    };

    it('renders investigation details correctly', () => {
        render(
            <TestWrapper>
                <InvestigationCard investigation={mockInvestigation} />
            </TestWrapper>
        );

        expect(screen.getByText('inv-123')).toBeInTheDocument();
        expect(screen.getByText('HIGH')).toBeInTheDocument();
        expect(screen.getByText('96%')).toBeInTheDocument();
        expect(screen.getByText('Database connection pool exhausted')).toBeInTheDocument();
    });

    it('handles click events correctly', () => {
        const mockOnClick = jest.fn();
        
        render(
            <TestWrapper>
                <InvestigationCard 
                    investigation={mockInvestigation} 
                    onClick={mockOnClick}
                />
            </TestWrapper>
        );

        fireEvent.click(screen.getByRole('button'));
        expect(mockOnClick).toHaveBeenCalledWith(mockInvestigation);
    });
});
```

### E2E Testing with Cypress
```javascript
// cypress/e2e/investigation-workflow.cy.js
describe('Investigation Workflow', () => {
    beforeEach(() => {
        cy.visit('/dashboard');
        cy.intercept('POST', '/api/investigations/start', { fixture: 'investigation-start.json' });
        cy.intercept('GET', '/api/investigations/*/progress', { fixture: 'investigation-progress.json' });
    });

    it('completes full investigation workflow', () => {
        // Start investigation
        cy.get('[data-testid="start-investigation-btn"]').click();
        
        // Verify progress indicators
        cy.get('.p-steps').should('be.visible');
        cy.get('[data-testid="progress-bar"]').should('exist');
        
        // Wait for completion
        cy.get('[data-testid="investigation-completed"]', { timeout: 10000 }).should('be.visible');
        
        // Verify results panels
        cy.get('[data-testid="executive-summary"]').should('contain.text', 'Database connection pool');
        cy.get('[data-testid="confidence-score"]').should('contain.text', '96%');
        cy.get('[data-testid="recommendations"]').should('exist');
        
        // Test evidence expansion
        cy.get('[data-testid="evidence-tab-traces"]').click();
        cy.get('[data-testid="trace-evidence-card"]').should('be.visible');
    });
});
```
## 11. Build & Deployment

### Vite Configuration for PrimeReact
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            '@': resolve(__dirname, 'src'),
            '@components': resolve(__dirname, 'src/components'),
            '@pages': resolve(__dirname, 'src/pages'),
            '@services': resolve(__dirname, 'src/services'),
            '@utils': resolve(__dirname, 'src/utils'),
            '@styles': resolve(__dirname, 'src/styles')
        }
    },
    optimizeDeps: {
        include: ['primereact/**']
    },
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    'primereact': ['primereact'],
                    'react-vendor': ['react', 'react-dom', 'react-router-dom'],
                    'charts': ['recharts', 'reactflow']
                }
            }
        },
        chunkSizeWarningLimit: 1000
    },
    server: {
        port: 3000,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                secure: false
            },
            '/ws': {
                target: 'ws://localhost:8000',
                ws: true
            }
        }
    }
});
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Environment Configuration
```javascript
// src/config/environment.js
export const config = {
    API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    WS_BASE_URL: import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000/ws',
    ENVIRONMENT: import.meta.env.VITE_ENVIRONMENT || 'development',
    DEBUG: import.meta.env.VITE_DEBUG === 'true',
    
    // PrimeReact theme configuration
    THEME: import.meta.env.VITE_THEME || 'lara-light-blue',
    LOCALE: import.meta.env.VITE_LOCALE || 'en',
    
    // Feature flags
    FEATURES: {
        REAL_TIME_UPDATES: import.meta.env.VITE_FEATURE_REAL_TIME === 'true',
        ADVANCED_CHARTS: import.meta.env.VITE_FEATURE_CHARTS === 'true',
        EXPORT_FUNCTIONALITY: import.meta.env.VITE_FEATURE_EXPORT === 'true'
    }
};
```

## 12. Package.json Configuration

### Updated Dependencies for PrimeReact
```json
{
  "name": "tattvaai-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite --host",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:e2e": "cypress open",
    "lint": "eslint src --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint src --ext .js,.jsx,.ts,.tsx --fix",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^19.2.7",
    "react-dom": "^19.2.7",
    "react-router-dom": "^7.18.1",
    "primereact": "^10.8.2",
    "primeicons": "^7.0.0",
    "primeflex": "^3.3.1",
    "axios": "^1.18.1",
    "chart.js": "^4.4.0",
    "reactflow": "^11.11.4",
    "@tanstack/react-query": "^5.0.0",
    "date-fns": "^2.30.0",
    "uuid": "^9.0.1"
  },
  "devDependencies": {
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@types/uuid": "^9.0.7",
    "@vitejs/plugin-react": "^6.0.3",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "@testing-library/user-event": "^14.0.0",
    "cypress": "^13.0.0",
    "eslint": "^10.6.0",
    "eslint-plugin-react": "^7.33.0",
    "eslint-plugin-react-hooks": "^7.1.1",
    "typescript": "^5.0.0",
    "vite": "^8.1.1",
    "vitest": "^1.0.0"
  }
}
```
## 13. Migration Strategy from Current Implementation

### Phase 1: PrimeReact Integration (Week 1)
**Install and configure PrimeReact ecosystem**
```bash
npm install primereact primeicons primeflex
npm install chart.js @types/chart.js
npm uninstall recharts  # Replace with PrimeReact Chart
```

**Update main.jsx with PrimeReact provider**
```jsx
// Replace current setup with PrimeReact configuration
import { PrimeReactProvider } from 'primereact/api';
import 'primereact/resources/themes/lara-light-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';
```

### Phase 2: Component Migration (Week 2-3)
**Priority migration order:**
1. **Layout Components** - Sidebar, Navbar, MainLayout
2. **Dashboard Components** - Cards, Statistics, Progress
3. **Investigation Components** - Details, Evidence, Timeline
4. **History/Reports** - Tables, Charts, Filters

**Migration mapping:**
```jsx
// Current → PrimeReact
div className="card" → <Card>
div className="table" → <DataTable>
div className="chart" → <Chart>
button → <Button>
input → <InputText>
select → <Dropdown>
```

### Phase 3: Advanced Features (Week 4)
**Enhanced functionality with PrimeReact:**
- **Real-time updates** → Toast notifications + ProgressBar
- **Advanced filtering** → MultiSelect + Calendar + FilterMatchMode
- **Data export** → DataTable export functionality
- **Responsive design** → PrimeFlex grid system

### Phase 4: Testing & Optimization (Week 5)
**Comprehensive testing suite:**
- Unit tests for all PrimeReact components
- E2E tests for complete workflows
- Performance optimization and lazy loading
- Accessibility compliance validation

## 14. Development Guidelines

### Component Structure Standards
```jsx
// Standard PrimeReact component structure
import React, { useState, useEffect, useRef } from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { ProgressBar } from 'primereact/progressbar';

const InvestigationComponent = ({ 
    investigation, 
    onUpdate, 
    loading = false 
}) => {
    // State management
    const [localState, setLocalState] = useState(null);
    const toast = useRef(null);

    // Effects
    useEffect(() => {
        // Component logic
    }, [investigation]);

    // Event handlers
    const handleAction = (event) => {
        try {
            // Action logic
            toast.current.show({
                severity: 'success',
                summary: 'Success',
                detail: 'Action completed'
            });
        } catch (error) {
            toast.current.show({
                severity: 'error',
                summary: 'Error',
                detail: error.message
            });
        }
    };

    // Render helpers
    const renderHeader = () => (
        <div className="flex align-items-center justify-content-between">
            <h3 className="m-0">Investigation {investigation?.id}</h3>
            <Button 
                icon="pi pi-refresh" 
                onClick={handleRefresh}
                loading={loading}
            />
        </div>
    );

    return (
        <div className="investigation-component">
            <Card header={renderHeader}>
                {loading ? (
                    <ProgressBar mode="indeterminate" />
                ) : (
                    <div className="content">
                        {/* Component content */}
                    </div>
                )}
            </Card>
            <Toast ref={toast} />
        </div>
    );
};

export default InvestigationComponent;
```

### Styling Conventions
```css
/* Use PrimeReact CSS classes + custom BEM methodology */
.investigation-component {
    /* Container styles */
}

.investigation-component__header {
    /* Header specific styles */
}

.investigation-component__content {
    /* Content specific styles */
}

.investigation-component--loading {
    /* Loading state modifier */
}

/* Leverage PrimeFlex utilities */
.flex.align-items-center.justify-content-between.gap-3.mb-4
```

## 15. Future Enhancements

### Advanced PrimeReact Features
**Coming in v2.0:**
- **Drag & Drop** - Reorderable investigation panels
- **Virtual Scrolling** - Handle thousands of investigations
- **Advanced Charts** - Interactive investigation analytics
- **Data Export** - PDF/Excel report generation
- **Theme Builder** - Custom TattvaAI branding
- **Mobile App** - React Native with PrimeReact Native

### Integration Roadmap
- **PrimeReact Editor** - Rich text incident descriptions
- **PrimeReact FileUpload** - Evidence attachment support
- **PrimeReact Scheduler** - Investigation scheduling
- **PrimeReact Captcha** - Security enhancements
- **PrimeReact SpeedDial** - Quick action menu

---

## 16. Conclusion

TattvaAI's frontend architecture leverages PrimeReact's enterprise-grade components to create a sophisticated, accessible, and performant user interface for AI-powered incident investigation. The combination of React 19, PrimeReact 10, and modern development practices ensures:

**✅ Enterprise Readiness** - Production-grade components with comprehensive features  
**✅ Developer Experience** - Consistent API, excellent documentation, TypeScript support  
**✅ User Experience** - Accessible, responsive, and intuitive interface design  
**✅ Maintainability** - Modular architecture with clear separation of concerns  
**✅ Scalability** - Performance optimizations for large-scale deployments  
**✅ Future-Proof** - Active ecosystem with regular updates and new features  

This architecture positions TattvaAI as a modern, professional platform that can compete with enterprise observability solutions while providing the specialized AI-powered investigation capabilities that differentiate it in the market.

---

*This frontend architecture document serves as the definitive guide for implementing TattvaAI's user interface using PrimeReact, ensuring consistent development practices and optimal user experience across all components and features.*