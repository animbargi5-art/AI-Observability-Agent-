import { useNavigate, useLocation } from "react-router-dom";
import { Menu } from "primereact/menu";
import { Badge } from "primereact/badge";
import { useState, useEffect } from "react";

import "../../styles/layouts/sidebar.css";

export default function Sidebar() {
    const navigate = useNavigate();
    const location = useLocation();
    const [activeRoute, setActiveRoute] = useState(location.pathname);

    // Update active route when location changes
    useEffect(() => {
        setActiveRoute(location.pathname);
    }, [location.pathname]);

    const menuItems = [
        {
            label: 'Main',
            items: [
                {
                    label: 'Dashboard',
                    icon: 'pi pi-home',
                    command: () => navigate('/dashboard'),
                    className: activeRoute === '/dashboard' ? 'active-menu-item' : ''
                },
                {
                    label: 'Investigations',
                    icon: 'pi pi-search',
                    items: [
                        {
                            label: 'Active Investigation',
                            icon: 'pi pi-play',
                            command: () => navigate('/investigation/active'),
                            disabled: true // Enable when there's an active investigation
                        },
                        {
                            label: 'Start New',
                            icon: 'pi pi-plus',
                            command: () => navigate('/dashboard') // Redirect to dashboard to start
                        }
                    ]
                },
                {
                    label: 'History',
                    icon: 'pi pi-history',
                    command: () => navigate('/history'),
                    className: activeRoute === '/history' ? 'active-menu-item' : ''
                },
                {
                    label: 'Reports',
                    icon: 'pi pi-chart-bar',
                    command: () => navigate('/reports'),
                    className: activeRoute === '/reports' ? 'active-menu-item' : ''
                }
            ]
        },
        {
            separator: true
        },
        {
            label: 'Management',
            items: [
                {
                    label: 'Settings',
                    icon: 'pi pi-cog',
                    command: () => navigate('/settings'),
                    className: activeRoute === '/settings' ? 'active-menu-item' : ''
                }
            ]
        },
        {
            separator: true
        },
        {
            label: 'Future Features',
            items: [
                {
                    label: 'Notifications',
                    icon: 'pi pi-bell',
                    badge: '3', // Example notification count
                    command: () => navigate('/notifications'),
                    disabled: true,
                    template: (item, options) => (
                        <div className={options.className} onClick={options.onClick}>
                            <span className={options.iconClassName}></span>
                            <span className={options.labelClassName}>{item.label}</span>
                            {item.badge && (
                                <Badge 
                                    value={item.badge} 
                                    severity="danger" 
                                    className="ml-auto"
                                />
                            )}
                        </div>
                    )
                },
                {
                    label: 'Live Monitoring',
                    icon: 'pi pi-eye',
                    command: () => navigate('/live-monitoring'),
                    disabled: true
                },
                {
                    label: 'Knowledge Graph',
                    icon: 'pi pi-sitemap',
                    command: () => navigate('/knowledge-graph'),
                    disabled: true
                },
                {
                    label: 'AI Assistant',
                    icon: 'pi pi-comments',
                    command: () => navigate('/ai-assistant'),
                    disabled: true
                }
            ]
        }
    ];

    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="logo-section">
                    <i className="pi pi-bolt logo-icon"></i>
                    <h2 className="logo-text">TattvaAI</h2>
                </div>
                <p className="tagline">AI Investigation Platform</p>
            </div>

            <div className="sidebar-menu">
                <Menu 
                    model={menuItems} 
                    className="navigation-menu"
                />
            </div>

            <div className="sidebar-footer">
                <div className="status-section">
                    <div className="status-item">
                        <i className="pi pi-circle-fill text-green-500"></i>
                        <span>Backend Online</span>
                    </div>
                    <div className="status-item">
                        <i className="pi pi-circle-fill text-blue-500"></i>
                        <span>SigNoz Connected</span>
                    </div>
                </div>
            </div>
        </aside>
    );
}