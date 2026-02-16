import React, { useState } from 'react';
import { leadsAPI } from '@/services/api';

interface LeadCaptureFormProps {
  source?: string;
  onSuccess?: (message: string) => void;
  onError?: (error: string) => void;
  buttonText?: string;
  compact?: boolean;
}

const LeadCaptureForm: React.FC<LeadCaptureFormProps> = ({
  source = 'landing_page',
  onSuccess,
  onError,
  buttonText = 'Get Started',
  compact = false,
}) => {
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [company, setCompany] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);
    setLoading(true);

    try {
      if (!email) {
        throw new Error('Email is required');
      }

      await leadsAPI.submitLead(email, fullName || undefined, company || undefined, source);
      
      const successMsg = 'Thanks! We\'ll be in touch soon.';
      setMessage({ type: 'success', text: successMsg });
      
      // Reset form
      setEmail('');
      setFullName('');
      setCompany('');

      if (onSuccess) {
        onSuccess(successMsg);
      }

      // Clear message after 3 seconds
      setTimeout(() => setMessage(null), 3000);
    } catch (err: any) {
      const errorMsg = err.detail || err.message || 'Failed to submit. Please try again.';
      setMessage({ type: 'error', text: errorMsg });
      if (onError) {
        onError(errorMsg);
      }
    } finally {
      setLoading(false);
    }
  };

  const containerStyle = compact
    ? {
        padding: '15px',
        backgroundColor: '#f8f9fa',
        borderRadius: '6px',
      }
    : {
        padding: '30px',
        backgroundColor: '#f8f9fa',
        borderRadius: '8px',
        border: '1px solid #e9ecef',
      };

  const inputStyle = {
    width: '100%',
    padding: '10px 12px',
    marginBottom: '12px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '14px',
    boxSizing: 'border-box' as const,
  };

  const buttonStyle = {
    width: '100%',
    padding: '12px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    fontWeight: 'bold' as const,
    cursor: loading ? 'not-allowed' : 'pointer',
    opacity: loading ? 0.6 : 1,
    transition: 'opacity 0.2s',
  };

  const messageStyle = {
    padding: '12px',
    marginBottom: '12px',
    borderRadius: '4px',
    fontSize: '14px',
    textAlign: 'center' as const,
    ...(message?.type === 'success'
      ? {
          backgroundColor: '#d4edda',
          color: '#155724',
          border: '1px solid #c3e6cb',
        }
      : {
          backgroundColor: '#f8d7da',
          color: '#721c24',
          border: '1px solid #f5c6cb',
        }),
  };

  return (
    <div style={containerStyle}>
      <h3 style={{ marginTop: 0, marginBottom: '20px', textAlign: 'center' }}>
        {compact ? 'Join Our Waitlist' : 'Get Started Today'}
      </h3>

      {message && <div style={messageStyle}>{message.text}</div>}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column' }}>
        <input
          type="email"
          placeholder="Your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={loading}
          style={inputStyle}
        />

        {!compact && (
          <>
            <input
              type="text"
              placeholder="Full name (optional)"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              disabled={loading}
              style={inputStyle}
            />

            <input
              type="text"
              placeholder="Company (optional)"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              disabled={loading}
              style={inputStyle}
            />
          </>
        )}

        <button type="submit" disabled={loading} style={buttonStyle}>
          {loading ? 'Submitting...' : buttonText}
        </button>
      </form>

      <p style={{ fontSize: '12px', color: '#666', marginTop: '12px', textAlign: 'center' }}>
        We'll never spam you. Unsubscribe anytime.
      </p>
    </div>
  );
};

export default LeadCaptureForm;
