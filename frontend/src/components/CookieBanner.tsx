import React, { useState, useEffect } from 'react';

interface CookieBannerProps {
  onAccept?: () => void;
  onDecline?: () => void;
}

const CookieBanner: React.FC<CookieBannerProps> = ({ onAccept, onDecline }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const cookieAccepted = localStorage.getItem('cookies_accepted');
    if (!cookieAccepted) {
      setIsVisible(true);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('cookies_accepted', 'true');
    setIsVisible(false);
    onAccept?.();
  };

  const handleDecline = () => {
    localStorage.setItem('cookies_accepted', 'false');
    setIsVisible(false);
    onDecline?.();
  };

  if (!isVisible) return null;

  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      backgroundColor: '#1a1a1a',
      color: 'white',
      padding: '20px',
      zIndex: 1000,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderTop: '1px solid #333'
    }}>
      <div>
        <p style={{ margin: 0, marginBottom: '10px' }}>
          <strong>Cookie Consent</strong>
        </p>
        <p style={{ margin: 0, fontSize: '14px', color: '#ccc' }}>
          We use cookies to improve your experience and analyze site usage.
        </p>
      </div>
      <div style={{ display: 'flex', gap: '10px', flexShrink: 0, marginLeft: '20px' }}>
        <button onClick={handleDecline} style={{
          padding: '10px 20px',
          backgroundColor: 'transparent',
          border: '1px solid white',
          color: 'white',
          cursor: 'pointer',
          borderRadius: '4px',
          fontSize: '14px',
          fontWeight: '500'
        }}>
          Decline
        </button>
        <button onClick={handleAccept} style={{
          padding: '10px 20px',
          backgroundColor: '#007bff',
          border: 'none',
          color: 'white',
          cursor: 'pointer',
          borderRadius: '4px',
          fontSize: '14px',
          fontWeight: '500'
        }}>
          Accept All
        </button>
      </div>
    </div>
  );
};

export default CookieBanner;
