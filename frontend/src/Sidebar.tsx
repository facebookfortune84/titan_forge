import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from './App'; // Import AuthContext

interface SidebarProps {
  // currentView and onViewChange are removed as navigation is handled by react-router-dom
  isAuthenticated: boolean;
  handleLogout: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isAuthenticated, handleLogout }) => {
  const authContext = useContext(AuthContext);

  const navItems = [
    { id: 'home', label: 'Home', path: '/' },
    { id: 'pricing', label: 'Pricing', path: '/pricing' },
    // Only show dashboard, tasks, agents if authenticated
  ];

  const authNavItems = [
    { id: 'dashboard', label: 'Dashboard', path: '/dashboard' },
    { id: 'tasks', label: 'Task History', path: '/tasks' },
    { id: 'agents', label: 'Agent Command Center', path: '/agents' },
  ];

  const publicAuthItems = [
    { id: 'login', label: 'Login', path: '/login' },
    { id: 'register', label: 'Register', path: '/register' },
  ];

  return (
    <nav style={{
      width: '250px', // Slightly wider for more content
      backgroundColor: '#f8f9fa',
      padding: '20px',
      borderRight: '1px solid #dee2e6',
      display: 'flex',
      flexDirection: 'column',
      gap: '10px'
    }}>
      <h2 style={{ marginBottom: '20px', color: '#007bff' }}>TitanForge AI</h2>
      {navItems.map(item => (
        <Link 
          key={item.id}
          to={item.path}
          style={{
            padding: '10px 15px',
            textAlign: 'left',
            color: '#495057',
            textDecoration: 'none',
            fontSize: '1em',
            borderRadius: '4px',
          }}
          // Basic hover effect for demonstration
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#e2e6ea'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
        >
          {item.label}
        </Link>
      ))}

      {isAuthenticated && (
        <>
          <hr style={{ margin: '10px 0', borderColor: '#e2e6ea' }} />
          {authNavItems.map(item => (
            <Link 
              key={item.id}
              to={item.path}
              style={{
                padding: '10px 15px',
                textAlign: 'left',
                color: '#495057',
                textDecoration: 'none',
                fontSize: '1em',
                borderRadius: '4px',
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#e2e6ea'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
            >
              {item.label}
            </Link>
          ))}
          <button
            onClick={handleLogout}
            style={{
              padding: '10px 15px',
              textAlign: 'left',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '1em',
              marginTop: '10px'
            }}
          >
            Logout ({authContext?.user?.email})
          </button>
        </>
      )}

      {!isAuthenticated && (
        <>
          <hr style={{ margin: '10px 0', borderColor: '#e2e6ea' }} />
          {publicAuthItems.map(item => (
            <Link 
              key={item.id}
              to={item.path}
              style={{
                padding: '10px 15px',
                textAlign: 'left',
                color: '#495057',
                textDecoration: 'none',
                fontSize: '1em',
                borderRadius: '4px',
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#e2e6ea'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
            >
              {item.label}
            </Link>
          ))}
        </>
      )}
    </nav>
  );
};

export default Sidebar;

