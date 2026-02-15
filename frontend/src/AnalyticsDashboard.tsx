import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from './App'; // Import AuthContext

interface AnalyticsSummary {
    total_users: number;
    total_signups: number;
    active_subscriptions: number;
    mrr_estimate_usd: number;
}

const AnalyticsDashboard: React.FC = () => {
    const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const authContext = useContext(AuthContext);

    useEffect(() => {
        const fetchAnalytics = async () => {
            setLoading(true);
            setError(null);
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    throw new Error("No authentication token found.");
                }
                const response = await axios.get<AnalyticsSummary>('http://127.0.0.1:8000/analytics/summary', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setAnalytics(response.data);
            } catch (err: any) {
                console.error("Failed to fetch analytics:", err);
                setError(err.response?.data?.detail || err.message || "Failed to load analytics data.");
            } finally {
                setLoading(false);
            }
        };

        if (authContext?.isAuthenticated && authContext.user?.is_superuser) {
            fetchAnalytics();
        } else if (authContext?.isAuthenticated && !authContext.user?.is_superuser) {
            setError("You do not have permission to view this dashboard.");
            setLoading(false);
        } else {
            setError("Please log in to view analytics.");
            setLoading(false);
        }
    }, [authContext?.isAuthenticated, authContext?.user?.is_superuser]);

    if (loading) {
        return <div style={{ textAlign: 'center', padding: '20px' }}>Loading Analytics...</div>;
    }

    if (error) {
        return <div style={{ textAlign: 'center', padding: '20px', color: 'red' }}>Error: {error}</div>;
    }

    if (!analytics) {
        return <div style={{ textAlign: 'center', padding: '20px' }}>No analytics data available.</div>;
    }

    return (
        <div style={{ maxWidth: '900px', margin: 'auto', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h2 style={{ textAlign: 'center', color: '#333', marginBottom: '30px' }}>Platform Analytics Dashboard</h2>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
                <div style={cardStyle}>
                    <h3>Total Registered Users</h3>
                    <p style={metricStyle}>{analytics.total_users}</p>
                </div>
                <div style={cardStyle}>
                    <h3>Total Signups (Lifetime)</h3>
                    <p style={metricStyle}>{analytics.total_signups}</p>
                </div>
                <div style={cardStyle}>
                    <h3>Active Subscriptions</h3>
                    <p style={metricStyle}>{analytics.active_subscriptions}</p>
                </div>
                <div style={cardStyle}>
                    <h3>Estimated MRR (USD)</h3>
                    <p style={metricStyle}>${analytics.mrr_estimate_usd.toFixed(2)}</p>
                </div>
            </div>

            {/* Additional sections for more detailed analytics */}
            <div style={{ marginTop: '40px', borderTop: '1px solid #eee', paddingTop: '20px' }}>
                <h3 style={{ color: '#555' }}>Recent Activity (Future Implementation)</h3>
                <p>Chart for daily signups, subscription changes, etc. will go here.</p>
            </div>
        </div>
    );
};

const cardStyle: React.CSSProperties = {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
    textAlign: 'center',
};

const metricStyle: React.CSSProperties = {
    fontSize: '2.5em',
    fontWeight: 'bold',
    color: '#007bff',
    margin: '10px 0 0',
};

export default AnalyticsDashboard;
