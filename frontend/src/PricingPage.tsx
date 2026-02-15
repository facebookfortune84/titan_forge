import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface PricingTier {
  id: string;
  name: string;
  price: number;
  description: string;
  features: string[];
}

const PricingPage: React.FC = () => {
  const [tiers, setTiers] = useState<PricingTier[]>([]);

  useEffect(() => {
    // In a real app, you might fetch this from an API
    const fetchPricing = async () => {
        try {
            const res = await axios.get('/pricing.json'); // It's in the public folder
            setTiers(res.data);
        } catch (e) {
            console.error("Could not load pricing.json", e);
        }
    };
    fetchPricing();
  }, []);

  return (
    <div style={{ display: 'flex', gap: '20px', justifyContent: 'center' }}>
      {tiers.map(tier => (
        <div key={tier.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', width: '30%', textAlign: 'center' }}>
          <h3 style={{ marginTop: 0 }}>{tier.name}</h3>
          <p style={{ fontSize: '2em', fontWeight: 'bold' }}>${tier.price}/mo</p>
          <p>{tier.description}</p>
          <ul style={{ listStyle: 'none', padding: 0, textAlign: 'left', margin: '20px 0' }}>
            {tier.features.map(feature => <li key={feature}>✔️ {feature}</li>)}
          </ul>
          <button disabled style={{ padding: '10px 20px', fontSize: '1em', cursor: 'not-allowed', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '5px' }}>
            Buy Now (Mock)
          </button>
        </div>
      ))}
    </div>
  );
};

export default PricingPage;
