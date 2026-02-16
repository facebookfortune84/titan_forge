import React, { useState } from 'react';

interface ROIData {
  current_annual_spend: number;
  titanforge_annual: number;
  titanforge_monthly: number;
  estimated_savings_annual: number;
  estimated_savings_monthly: number;
  net_monthly_savings: number;
  months_to_breakeven: number;
  roi_percentage: number;
}

interface ROICalculatorComponentProps {
  data?: ROIData;
  companyName?: string;
}

const ROICalculatorComponent: React.FC<ROICalculatorComponentProps> = ({ 
  data, 
  companyName = 'Your Company' 
}) => {
  if (!data) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
        <p>No ROI data available. Generate a PDF to see calculations.</p>
      </div>
    );
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(value);
  };

  return (
    <div style={{
      backgroundColor: '#f9f9f9',
      borderRadius: '8px',
      padding: '30px',
      maxWidth: '800px',
      margin: '20px auto',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
    }}>
      <h2 style={{ textAlign: 'center', color: '#333', marginTop: 0 }}>
        ROI Analysis for {companyName}
      </h2>

      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '20px',
        marginBottom: '30px'
      }}>
        <div style={{
          backgroundColor: 'white',
          padding: '15px',
          borderRadius: '6px',
          borderLeft: '4px solid #007bff'
        }}>
          <p style={{ margin: '0 0 5px 0', color: '#666', fontSize: '14px' }}>
            Current Annual Spend
          </p>
          <p style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#333' }}>
            {formatCurrency(data.current_annual_spend)}
          </p>
        </div>

        <div style={{
          backgroundColor: 'white',
          padding: '15px',
          borderRadius: '6px',
          borderLeft: '4px solid #28a745'
        }}>
          <p style={{ margin: '0 0 5px 0', color: '#666', fontSize: '14px' }}>
            Annual Savings with TitanForge
          </p>
          <p style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#28a745' }}>
            {formatCurrency(data.estimated_savings_annual)}
          </p>
        </div>

        <div style={{
          backgroundColor: 'white',
          padding: '15px',
          borderRadius: '6px',
          borderLeft: '4px solid #ffc107'
        }}>
          <p style={{ margin: '0 0 5px 0', color: '#666', fontSize: '14px' }}>
            TitanForge Annual Cost
          </p>
          <p style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#333' }}>
            {formatCurrency(data.titanforge_annual)}
          </p>
        </div>

        <div style={{
          backgroundColor: 'white',
          padding: '15px',
          borderRadius: '6px',
          borderLeft: '4px solid #17a2b8'
        }}>
          <p style={{ margin: '0 0 5px 0', color: '#666', fontSize: '14px' }}>
            Net Monthly Savings
          </p>
          <p style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#17a2b8' }}>
            {formatCurrency(data.net_monthly_savings)}
          </p>
        </div>
      </div>

      <div style={{
        backgroundColor: 'white',
        padding: '20px',
        borderRadius: '6px',
        marginBottom: '20px',
        textAlign: 'center'
      }}>
        <h3 style={{ margin: '0 0 15px 0', color: '#333' }}>Key Metrics</h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '20px'
        }}>
          <div>
            <p style={{ margin: '0 0 10px 0', color: '#666' }}>ROI Percentage</p>
            <p style={{ 
              margin: 0, 
              fontSize: '32px', 
              fontWeight: 'bold', 
              color: '#007bff'
            }}>
              {data.roi_percentage.toFixed(0)}%
            </p>
          </div>
          <div>
            <p style={{ margin: '0 0 10px 0', color: '#666' }}>Breakeven Period</p>
            <p style={{ 
              margin: 0, 
              fontSize: '32px', 
              fontWeight: 'bold', 
              color: '#28a745'
            }}>
              {Math.ceil(data.months_to_breakeven)} months
            </p>
          </div>
        </div>
      </div>

      <div style={{
        backgroundColor: '#e7f3ff',
        padding: '15px',
        borderRadius: '6px',
        borderLeft: '4px solid #007bff'
      }}>
        <p style={{ margin: 0, color: '#004085', fontSize: '14px' }}>
          <strong>💡 Insight:</strong> By switching to TitanForge, you could save{' '}
          <strong>{formatCurrency(data.estimated_savings_annual)}</strong> annually while reducing operational complexity.
        </p>
      </div>
    </div>
  );
};

export default ROICalculatorComponent;
