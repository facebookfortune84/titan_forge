import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from './App';
import { authAPI } from '@/services/api';

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const authContext = useContext(AuthContext);

    if (!authContext) {
      throw new Error('LoginPage must be used within an AuthProvider');
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            const tokens = await authAPI.login(email, password);
            localStorage.setItem('access_token', tokens.access_token);
            const user = await authAPI.getCurrentUser();
            authContext.setIsAuthenticated(true);
            authContext.setUser(user);
            navigate('/dashboard');
        } catch (err: any) {
            // Check if it's a FastAPI validation array [{msg: ...}] or a simple string
            const rawDetail = err.detail;
            let displayMessage = 'Login failed';

            if (Array.isArray(rawDetail)) {
                // Extracts the specific message like "field required" or "invalid email"
                displayMessage = rawDetail.map(d => `${d.loc[1]}: ${d.msg}`).join(', ');
            } else if (typeof rawDetail === 'string') {
                displayMessage = rawDetail;
            } else if (err.message) {
                displayMessage = err.message;
            }

            setError(displayMessage);
            console.error('Login error:', err);
        } finally {
          setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Login</h2>
            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div>
                    <label htmlFor="email" style={{ marginBottom: '5px', display: 'block' }}>Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                    />
                </div>
                <div>
                    <label htmlFor="password" style={{ marginBottom: '5px', display: 'block' }}>Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
                    />
                </div>
                <button
                    type="submit"
                    disabled={loading}
                    style={{ padding: '10px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', opacity: loading ? 0.6 : 1 }}
                >
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>
            <p style={{ textAlign: 'center', marginTop: '20px' }}>
                Don't have an account? <Link to="/register">Register here</Link>
            </p>
        </div>
    );
};

export default LoginPage;
