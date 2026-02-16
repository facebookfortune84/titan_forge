import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from "@/App";
import { productAPI } from '@/services/api';
import type { Product } from '@/types/index';

interface PricingTier extends Product {
  price: number; // Price in dollars for display
}

const PricingPage: React.FC = () => {
  const [tiers, setTiers] = useState<PricingTier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const auth = useContext(AuthContext);
  if (!auth) { return <div>Loading...</div>; }
  const { isAuthenticated } = auth;

  useEffect(() => {
    const fetchPricing = async () => {
      setLoading(true);
      setError(null);
      try {
        if (!isAuthenticated) {
          setTiers([]);
          return;
        }
        const products = await productAPI.getProducts();
        const formattedTiers: PricingTier[] = products.map((product) => ({
          ...product,
          price: product.price / 100, // Convert cents to dollars
        }));
        setTiers(formattedTiers);
      } catch (err: any) {
        console.error("Could not load pricing from backend", err);
        setError(err.detail || "Failed to load pricing");
      } finally {
        setLoading(false);
      }
    };
    fetchPricing();
  }, [isAuthenticated]);

  const handleSubscribe = async (productId: string) => {
    if (!isAuthenticated) {
      alert("Please log in to subscribe.");
      return;
    }

    try {
      const session = await productAPI.createCheckoutSession(productId);
      window.location.href = session.url;
    } catch (error: any) {
      console.error("Error creating checkout session:", error);
        alert("Failed to initiate payment. Please try again later.");
    }
  };

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
          <button
            onClick={() => handleSubscribe(tier.id)}
            disabled={!isAuthenticated}
            style={{ 
              padding: '10px 20px', 
              fontSize: '1em', 
              cursor: isAuthenticated ? 'pointer' : 'not-allowed', 
              backgroundColor: isAuthenticated ? '#007bff' : '#6c757d', 
              color: 'white', 
              border: 'none', 
              borderRadius: '5px' 
            }}
          >
            {isAuthenticated ? "Buy Now" : "Log in to Buy"}
          </button>
        </div>
      ))}
    </div>
  );
};

export default PricingPage;
