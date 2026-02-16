import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useSwarm } from '@/contexts/SwarmContext';

const RealmForgeLandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { swarmStatus, agents, loading } = useSwarm();
  const [stats, setStats] = useState({ total_agents: 0, departments: 0, active: 0 });

  useEffect(() => {
    if (swarmStatus) {
      setStats({
        total_agents: swarmStatus.total_agents,
        departments: swarmStatus.departments.length,
        active: swarmStatus.active_agents,
      });
    }
  }, [swarmStatus]);

  const departments = [
    { name: 'Software Engineering', icon: '⚙️', description: 'Code generation & architecture' },
    { name: 'Cyber Security', icon: '🔒', description: 'Security audits & penetration testing' },
    { name: 'Data Intelligence', icon: '📊', description: 'Analytics & insights' },
    { name: 'DevOps Infrastructure', icon: '☁️', description: 'Deployment & infrastructure' },
    { name: 'Financial Operations', icon: '💰', description: 'Billing & revenue optimization' },
    { name: 'Marketing & PR', icon: '📢', description: 'Content & campaigns' },
  ];

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0f172a', color: '#e2e8f0', paddingBottom: '40px' }}>
      {/* Navigation */}
      <nav style={{ padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1e293b' }}>
        <h1 style={{ margin: 0, fontSize: '1.5em', fontWeight: 'bold' }}>🔥 TitanForge</h1>
        <div style={{ display: 'flex', gap: '20px' }}>
          <Link to="/login" style={{ color: '#60a5fa', textDecoration: 'none', cursor: 'pointer' }}>Login</Link>
          <Link to="/register" style={{ color: '#34d399', textDecoration: 'none', cursor: 'pointer' }}>Register</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section style={{ padding: '80px 40px', textAlign: 'center' }}>
        <h2 style={{ fontSize: '3.5em', fontWeight: 'bold', marginBottom: '20px', background: 'linear-gradient(to right, #60a5fa, #34d399)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Autonomous Software Development at Scale
        </h2>
        <p style={{ fontSize: '1.2em', color: '#cbd5e1', marginBottom: '30px', maxWidth: '600px', margin: '0 auto 30px' }}>
          Meet TitanForge: The AI-powered swarm that codes, deploys, secures, and optimizes your entire software development lifecycle.
        </p>
        <div style={{ display: 'flex', gap: '15px', justifyContent: 'center' }}>
          <button
            onClick={() => navigate('/register')}
            style={{
              padding: '15px 40px',
              fontSize: '1.1em',
              backgroundColor: '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 'bold',
              transition: 'background-color 0.3s',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#2563eb')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#3b82f6')}
          >
            Get Started Free
          </button>
          <Link
            to="/pricing"
            style={{
              padding: '15px 40px',
              fontSize: '1.1em',
              backgroundColor: 'transparent',
              color: '#60a5fa',
              border: '2px solid #60a5fa',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 'bold',
              textDecoration: 'none',
              display: 'inline-block',
            }}
          >
            View Pricing
          </Link>
        </div>
      </section>

      {/* Swarm Stats */}
      <section style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '60px' }}>
          <div style={{ backgroundColor: '#1e293b', padding: '30px', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: '#60a5fa', marginBottom: '10px' }}>
              {loading ? '...' : stats.total_agents}
            </div>
            <div style={{ color: '#94a3b8' }}>Autonomous Agents</div>
            <div style={{ fontSize: '0.9em', color: '#64748b', marginTop: '10px' }}>{loading ? 'Loading...' : `${stats.active} currently active`}</div>
          </div>

          <div style={{ backgroundColor: '#1e293b', padding: '30px', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: '#34d399', marginBottom: '10px' }}>
              {loading ? '...' : stats.departments}
            </div>
            <div style={{ color: '#94a3b8' }}>Specialized Departments</div>
            <div style={{ fontSize: '0.9em', color: '#64748b', marginTop: '10px' }}>Each with unique expertise</div>
          </div>

          <div style={{ backgroundColor: '#1e293b', padding: '30px', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: '#fbbf24', marginBottom: '10px' }}>24/7</div>
            <div style={{ color: '#94a3b8' }}>Always Available</div>
            <div style={{ fontSize: '0.9em', color: '#64748b', marginTop: '10px' }}>No downtime, full automation</div>
          </div>
        </div>
      </section>

      {/* Departments Showcase */}
      <section style={{ padding: '60px 40px', backgroundColor: '#1e293b', borderRadius: '8px', margin: '0 40px', marginBottom: '60px' }}>
        <h3 style={{ fontSize: '2.2em', fontWeight: 'bold', marginBottom: '50px', textAlign: 'center' }}>Meet Our Specialized Departments</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px' }}>
          {departments.map((dept, idx) => (
            <div key={idx} style={{ backgroundColor: '#0f172a', padding: '30px', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ fontSize: '2.5em', marginBottom: '15px' }}>{dept.icon}</div>
              <h4 style={{ fontSize: '1.3em', fontWeight: 'bold', marginBottom: '10px' }}>{dept.name}</h4>
              <p style={{ color: '#94a3b8' }}>{dept.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: '60px 40px', maxWidth: '1200px', margin: '0 auto' }}>
        <h3 style={{ fontSize: '2.2em', fontWeight: 'bold', marginBottom: '50px', textAlign: 'center' }}>Powerful Capabilities</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '40px' }}>
          <div>
            <div style={{ fontSize: '2em', marginBottom: '15px' }}>⚡</div>
            <h4 style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>Lightning Fast</h4>
            <p style={{ color: '#cbd5e1' }}>Process thousands of tasks simultaneously with our distributed swarm architecture</p>
          </div>
          <div>
            <div style={{ fontSize: '2em', marginBottom: '15px' }}>🎯</div>
            <h4 style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>Precision Focused</h4>
            <p style={{ color: '#cbd5e1' }}>Specialized agents with deep expertise in their domains deliver quality results</p>
          </div>
          <div>
            <div style={{ fontSize: '2em', marginBottom: '15px' }}>🔄</div>
            <h4 style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>Fully Autonomous</h4>
            <p style={{ color: '#cbd5e1' }}>Your agents work independently, collaborate seamlessly, and self-optimize</p>
          </div>
          <div>
            <div style={{ fontSize: '2em', marginBottom: '15px' }}>📊</div>
            <h4 style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>Real-time Analytics</h4>
            <p style={{ color: '#cbd5e1' }}>Monitor agent performance, system health, and project metrics in real-time</p>
          </div>
          <div>
            <div style={{ fontSize: '2em', marginBottom: '15px' }}>🔐</div>
            <h4 style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>Enterprise Security</h4>
            <p style={{ color: '#cbd5e1' }}>End-to-end encryption, audit logs, and compliance with industry standards</p>
          </div>
          <div>
            <div style={{ fontSize: '2em', marginBottom: '15px' }}>🚀</div>
            <h4 style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>Easy Integration</h4>
            <p style={{ color: '#cbd5e1' }}>Works with your existing tools and platforms through simple APIs</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{ padding: '60px 40px', textAlign: 'center', backgroundColor: '#1e293b', margin: '60px 40px 0', borderRadius: '8px' }}>
        <h3 style={{ fontSize: '2.2em', fontWeight: 'bold', marginBottom: '20px' }}>Ready to Automate Your Development?</h3>
        <p style={{ fontSize: '1.1em', color: '#cbd5e1', marginBottom: '30px' }}>Join hundreds of companies accelerating their software development with TitanForge</p>
        <button
          onClick={() => navigate('/register')}
          style={{
            padding: '15px 50px',
            fontSize: '1.1em',
            backgroundColor: '#10b981',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            transition: 'background-color 0.3s',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#059669')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#10b981')}
        >
          Start Free Trial
        </button>
      </section>

      {/* Footer */}
      <footer style={{ padding: '40px', textAlign: 'center', borderTop: '1px solid #1e293b', marginTop: '60px', color: '#64748b' }}>
        <p>&copy; 2025 TitanForge. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default RealmForgeLandingPage;
