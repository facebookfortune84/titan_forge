import React, { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Loader, AlertCircle, CheckCircle2 } from "lucide-react";

export default function CheckoutPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const tier = searchParams.get("tier") || "basic";
  const isMonthly = searchParams.get("monthly") === "true";
  
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const pricing = {
    basic: {
      monthly: 2999,
      annual: 2499,
      name: "Basic",
      features: ["5 AI Agents", "10k tasks/month", "Email support"],
    },
    pro: {
      monthly: 4999,
      annual: 4499,
      name: "Pro",
      features: ["Unlimited Agents", "Unlimited tasks", "Priority support"],
    },
  };

  const plan = pricing[tier as keyof typeof pricing] || pricing.basic;
  const amount = isMonthly ? plan.monthly : plan.annual;
  const interval = isMonthly ? "/month" : "/year";

  const handleCheckout = async () => {
    setProcessing(true);
    setError("");
    
    try {
      // Call Stripe checkout endpoint
      const response = await fetch("http://localhost:8000/api/v1/payments/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tier,
          interval: isMonthly ? "month" : "year",
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.checkout_url) {
          window.location.href = data.checkout_url;
        } else {
          setSuccess(true);
          setTimeout(() => navigate("/dashboard"), 3000);
        }
      } else {
        setError("Checkout failed. Please try again.");
      }
    } catch (err) {
      setError("An error occurred. Please check your connection.");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="bg-slate-900/50 backdrop-blur border border-purple-500/20 rounded-lg p-8 text-center">
          <h1 className="text-3xl font-bold text-white mb-2">Checkout</h1>
          <p className="text-slate-400 mb-8">{plan.name} Plan</p>

          <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-6 mb-8">
            <div className="text-4xl font-bold text-white mb-2">
              ${(amount / 100).toFixed(2)}
              <span className="text-lg text-slate-400 font-normal">{interval}</span>
            </div>
            <p className="text-slate-400">Billed {isMonthly ? "monthly" : "annually"}</p>
          </div>

          <div className="mb-8 text-left">
            <h3 className="font-semibold text-white mb-4">Includes:</h3>
            <ul className="space-y-3">
              {plan.features.map((feature, idx) => (
                <li key={idx} className="flex items-center gap-3 text-slate-300">
                  <CheckCircle2 size={20} className="text-green-500 flex-shrink-0" />
                  {feature}
                </li>
              ))}
            </ul>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6 flex items-center gap-3">
              <AlertCircle size={20} className="text-red-400 flex-shrink-0" />
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          {success && (
            <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4 mb-6 flex items-center gap-3">
              <CheckCircle2 size={20} className="text-green-400 flex-shrink-0" />
              <p className="text-green-300 text-sm">Subscription confirmed! Redirecting...</p>
            </div>
          )}

          <button
            onClick={handleCheckout}
            disabled={processing}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
          >
            {processing ? (
              <>
                <Loader size={20} className="animate-spin" />
                Processing...
              </>
            ) : (
              "Complete Purchase"
            )}
          </button>

          <p className="text-sm text-slate-500 mt-6">
            Secure checkout powered by Stripe
          </p>
        </div>
      </div>
    </div>
  );
}
