// @ts-nocheck
import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  ArrowRight, Check, Star, Zap, Shield, Cpu, Users,
  GitBranch, TrendingUp, Code, Sparkles, Lock, Bell,
  Menu, X, Play, ChevronDown, AlertCircle
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function LandingPagePro() {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<"basic" | "pro" | null>(null);
  const [showLiveDemo, setShowLiveDemo] = useState(false);
  const [leadFormData, setLeadFormData] = useState({
    email: "",
    company: "",
    size: "51-500",
    firstname: "",
    lastname: "",
  });
  const [leadFormSubmitting, setLeadFormSubmitting] = useState(false);
  const [leadFormSuccess, setLeadFormSuccess] = useState(false);
  const [cookieAccepted, setCookieAccepted] = useState(false);
  const [showCookieConsent, setShowCookieConsent] = useState(!localStorage.getItem("titanforge_cookies"));

  useEffect(() => {
    if (cookieAccepted) {
      localStorage.setItem("titanforge_cookies", "accepted");
      setShowCookieConsent(false);
    }
  }, [cookieAccepted]);

  const handleLeadFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLeadFormSubmitting(true);

    try {
      const response = await fetch("http://localhost:8000/api/v1/sales/lead-magnet/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: leadFormData.email,
          company_name: leadFormData.company,
          company_size: leadFormData.size,
          first_name: leadFormData.firstname,
          last_name: leadFormData.lastname,
        }),
      });

      if (response.ok) {
        setLeadFormSuccess(true);
        setLeadFormData({ email: "", company: "", size: "51-500", firstname: "", lastname: "" });
        setTimeout(() => setLeadFormSuccess(false), 5000);
      }
    } catch (error) {
      console.error("Lead form error:", error);
    } finally {
      setLeadFormSubmitting(false);
    }
  };

  const handleCheckout = (tier: "basic" | "pro") => {
    const monthlyPrice = tier === "basic" ? 2999 : 4999;
    navigate(`/checkout?tier=${tier}&monthly=${monthlyPrice}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 text-white overflow-hidden">
      {/* --- COOKIE CONSENT --- */}
      <AnimatePresence>
        {showCookieConsent && (
          <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            className="fixed bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur border-t border-purple-500/30 p-4 z-50"
          >
            <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
              <p className="text-sm text-slate-300">
                We use cookies to enhance your experience. By continuing, you agree to our{" "}
                <Link to="/privacy" className="text-purple-400 hover:text-purple-300 underline">
                  Privacy Policy
                </Link>
                .
              </p>
              <button
                onClick={() => setCookieAccepted(true)}
                className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-semibold whitespace-nowrap transition"
              >
                Accept All
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* --- NAVIGATION --- */}
      <nav className="sticky top-0 z-40 backdrop-blur-lg bg-slate-950/50 border-b border-purple-500/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 group">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Zap className="text-white" size={24} />
              </div>
              <span className="font-bold text-xl bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                TitanForge
              </span>
            </Link>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-slate-300 hover:text-white transition">
                Features
              </a>
              <a href="#pricing" className="text-slate-300 hover:text-white transition">
                Pricing
              </a>
              <Link to="/blog" className="text-slate-300 hover:text-white transition">
                Blog
              </Link>
              <a href="#about" className="text-slate-300 hover:text-white transition">
                About
              </a>
            </div>

            {/* Auth Buttons */}
            <div className="hidden md:flex items-center gap-4">
              <Link
                to="/login"
                className="px-4 py-2 text-slate-300 hover:text-white transition"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-semibold transition"
              >
                Get Started
              </Link>
            </div>

            {/* Mobile Menu Button */}
            <button
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>

          {/* Mobile Menu */}
          <AnimatePresence>
            {mobileMenuOpen && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="md:hidden mt-4 pt-4 border-t border-purple-500/20 space-y-4"
              >
                <a href="#features" className="block text-slate-300 hover:text-white">
                  Features
                </a>
                <a href="#pricing" className="block text-slate-300 hover:text-white">
                  Pricing
                </a>
                <Link to="/blog" className="block text-slate-300 hover:text-white">
                  Blog
                </Link>
                <Link to="/login" className="block text-slate-300 hover:text-white">
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block w-full px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg font-semibold text-center"
                >
                  Get Started
                </Link>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </nav>

      {/* --- HERO SECTION --- */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-20 left-10 w-72 h-72 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl animate-blob" />
          <div className="absolute top-40 right-10 w-72 h-72 bg-blue-600 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000" />
          <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-pink-600 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/20 border border-purple-500/30 rounded-full mb-6 backdrop-blur">
              <Sparkles size={16} className="text-purple-400" />
              <span className="text-sm font-semibold text-purple-300">
                AI-Powered Development Agency
              </span>
            </div>

            {/* Main Headline */}
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black mb-6 leading-tight">
              Replace Your{" "}
              <span className="bg-gradient-to-r from-purple-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                Expensive Agency
              </span>
            </h1>

            {/* Subheadline */}
            <p className="text-xl sm:text-2xl text-slate-300 mb-8 max-w-2xl mx-auto leading-relaxed">
              AI-powered software development agency that delivers in days, not weeks. Save $84K+/year while shipping faster.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowLiveDemo(true)}
                className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold text-lg flex items-center justify-center gap-2 transition shadow-lg hover:shadow-purple-500/50"
              >
                <Play size={20} />
                Watch Live Demo
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setLeadFormSubmitting(!leadFormSubmitting)}
                className="px-8 py-4 bg-slate-700/50 border-2 border-purple-500/50 hover:bg-slate-700/70 rounded-lg font-bold text-lg flex items-center justify-center gap-2 transition"
              >
                Get ROI Calculator
                <ArrowRight size={20} />
              </motion.button>
            </div>

            {/* Social Proof */}
            <div className="flex items-center justify-center gap-8 text-sm text-slate-400">
              <div className="flex items-center gap-2">
                <Users size={16} />
                <span>50+ companies shipped features</span>
              </div>
              <div className="hidden sm:flex items-center gap-2">
                <TrendingUp size={16} />
                <span>14.4:1 LTV/CAC ratio</span>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* --- FEATURES SECTION --- */}
      <section id="features" className="py-24 bg-slate-900/50 border-t border-purple-500/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-black mb-4">Why Teams Choose TitanForge</h2>
            <p className="text-xl text-slate-400">Everything you need to ship features at superhuman speed</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Zap className="text-purple-400" size={32} />,
                title: "3-5x Faster",
                description: "Ship in days instead of weeks. AI agents work 24/7 without fatigue.",
              },
              {
                icon: <TrendingUp className="text-blue-400" size={32} />,
                title: "Save $84K/Year",
                description: "No hiring, onboarding, or management overhead. Just results.",
              },
              {
                icon: <Lock className="text-green-400" size={32} />,
                title: "You Own Everything",
                description: "Your code, your infrastructure, zero vendor lock-in.",
              },
              {
                icon: <Cpu className="text-pink-400" size={32} />,
                title: "AI Agent Swarm",
                description: "5-10 specialized AI agents assigned to your projects.",
              },
              {
                icon: <Shield className="text-cyan-400" size={32} />,
                title: "Enterprise Quality",
                description: "Production-grade security, testing, and documentation included.",
              },
              {
                icon: <Users className="text-indigo-400" size={32} />,
                title: "Dedicated Support",
                description: "Slack channel access with dedicated success manager.",
              },
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="p-6 bg-slate-800/50 border border-purple-500/20 rounded-lg hover:border-purple-500/50 transition group"
              >
                <div className="mb-4 p-3 bg-slate-700/50 rounded-lg w-fit group-hover:scale-110 transition">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-bold mb-2">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* --- LIVE DEMO SECTION --- */}
      {showLiveDemo && (
        <section className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="w-full max-w-4xl bg-slate-900 rounded-2xl p-6 border border-purple-500/30"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-2xl font-bold">Live TitanForge Demo</h3>
              <button
                onClick={() => setShowLiveDemo(false)}
                className="p-2 hover:bg-slate-800 rounded-lg transition"
              >
                <X size={24} />
              </button>
            </div>

            {/* Demo Video Placeholder */}
            <div className="bg-gradient-to-br from-purple-600/20 to-blue-600/20 border border-purple-500/30 rounded-lg aspect-video flex items-center justify-center">
              <div className="text-center">
                <Cpu size={64} className="mx-auto mb-4 text-purple-400 opacity-50" />
                <p className="text-slate-400">
                  [Live demo video showing agents working on a real project]
                </p>
                <p className="text-sm text-slate-500 mt-2">
                  Shows: Agent assignment → Code generation → Testing → Deployment
                </p>
              </div>
            </div>

            {/* Demo Features */}
            <div className="mt-6 grid md:grid-cols-2 gap-4">
              <div className="flex items-start gap-3">
                <Check size={20} className="text-green-400 mt-1" />
                <div>
                  <h4 className="font-bold">Real-time Agent Status</h4>
                  <p className="text-sm text-slate-400">See what your agents are working on right now</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Check size={20} className="text-green-400 mt-1" />
                <div>
                  <h4 className="font-bold">Live Code Delivery</h4>
                  <p className="text-sm text-slate-400">Artifacts delivered as they're completed</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Check size={20} className="text-green-400 mt-1" />
                <div>
                  <h4 className="font-bold">Multi-Modal Commands</h4>
                  <p className="text-sm text-slate-400">Voice, text, or written directives</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Check size={20} className="text-green-400 mt-1" />
                <div>
                  <h4 className="font-bold">Intelligent Routing</h4>
                  <p className="text-sm text-slate-400">Tasks auto-routed to best agents</p>
                </div>
              </div>
            </div>
          </motion.div>
        </section>
      )}

      {/* --- PRICING SECTION --- */}
      <section id="pricing" className="py-24 bg-slate-950/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-black mb-4">Simple, Transparent Pricing</h2>
            <p className="text-xl text-slate-400">Choose the plan that fits your team</p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Basic Plan */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="p-8 bg-slate-800/50 border border-purple-500/30 rounded-lg hover:border-purple-500/50 transition relative"
            >
              <div className="absolute -top-4 left-6 px-3 py-1 bg-purple-600 text-sm font-bold rounded-full">
                POPULAR
              </div>

              <h3 className="text-2xl font-bold mb-2">Basic</h3>
              <p className="text-slate-400 mb-6">Perfect for startups and teams</p>

              <div className="mb-6">
                <span className="text-4xl font-black">$2,999</span>
                <span className="text-slate-400">/month</span>
                <p className="text-sm text-green-400 mt-2">or $2,499/month (save 17% annually)</p>
              </div>

              <ul className="space-y-3 mb-8">
                {[
                  "5 AI Developers",
                  "40 hours/month",
                  "Email Support",
                  "Standard API",
                  "GitHub Integration",
                  "Weekly Reports",
                ].map((item, idx) => (
                  <li key={idx} className="flex items-center gap-3">
                    <Check size={20} className="text-green-400" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleCheckout("basic")}
                className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold transition"
              >
                Get Started
              </button>
            </motion.div>

            {/* Pro Plan */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="p-8 bg-gradient-to-br from-purple-600/20 to-blue-600/20 border-2 border-purple-500/50 rounded-lg relative transform md:scale-105 md:-translate-y-4"
            >
              <div className="absolute -top-4 left-6 px-3 py-1 bg-blue-600 text-sm font-bold rounded-full">
                BEST VALUE
              </div>

              <h3 className="text-2xl font-bold mb-2">Pro</h3>
              <p className="text-slate-300 mb-6">For high-growth companies</p>

              <div className="mb-6">
                <span className="text-4xl font-black">$4,999</span>
                <span className="text-slate-400">/month</span>
                <p className="text-sm text-green-400 mt-2">or $4,499/month (save 10% annually)</p>
              </div>

              <ul className="space-y-3 mb-8">
                {[
                  "10 AI Developers",
                  "Unlimited hours",
                  "Dedicated Support + Slack",
                  "Priority API (99.95% SLA)",
                  "GitHub + Full Integration",
                  "Daily Reports + Analytics",
                  "Custom AI Training",
                  "Quarterly Strategy Calls",
                ].map((item, idx) => (
                  <li key={idx} className="flex items-center gap-3">
                    <Check size={20} className="text-green-400" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleCheckout("pro")}
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold transition"
              >
                Get Started
              </button>
            </motion.div>
          </div>

          {/* One-time services */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mt-16 p-8 bg-slate-800/30 border border-slate-700/50 rounded-lg max-w-2xl mx-auto"
          >
            <h3 className="text-2xl font-bold mb-6 text-center">One-Time Projects</h3>
            <div className="grid sm:grid-cols-3 gap-4">
              {[
                { title: "Small", price: "$1,999", desc: "API or component" },
                { title: "Medium", price: "$3,999", desc: "Full feature" },
                { title: "Large", price: "$5,999", desc: "Complex system" },
              ].map((item, idx) => (
                <div key={idx} className="text-center">
                  <h4 className="font-bold mb-2">{item.title}</h4>
                  <p className="text-2xl font-black text-purple-400 mb-1">{item.price}</p>
                  <p className="text-sm text-slate-400">{item.desc}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* --- LEAD MAGNET FORM --- */}
      <section className="py-24 bg-gradient-to-r from-purple-900/50 to-blue-900/50 border-y border-purple-500/30">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl sm:text-4xl font-black mb-4">
              Get Your Personalized ROI Calculator
            </h2>
            <p className="text-lg text-slate-300">
              See exactly how much you can save with TitanForge. Takes 60 seconds.
            </p>
          </motion.div>

          {leadFormSuccess ? (
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="p-8 bg-green-500/20 border border-green-500/50 rounded-lg text-center"
            >
              <Check size={48} className="mx-auto mb-4 text-green-400" />
              <h3 className="text-2xl font-bold mb-2">✅ Check Your Email!</h3>
              <p className="text-slate-300">
                Your personalized ROI calculator has been sent. It should arrive in the next minute.
              </p>
            </motion.div>
          ) : (
            <form onSubmit={handleLeadFormSubmit} className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="First Name"
                  value={leadFormData.firstname}
                  onChange={(e) =>
                    setLeadFormData({ ...leadFormData, firstname: e.target.value })
                  }
                  className="px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg focus:outline-none focus:border-purple-500 transition"
                  required
                />
                <input
                  type="text"
                  placeholder="Last Name"
                  value={leadFormData.lastname}
                  onChange={(e) =>
                    setLeadFormData({ ...leadFormData, lastname: e.target.value })
                  }
                  className="px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg focus:outline-none focus:border-purple-500 transition"
                  required
                />
              </div>

              <input
                type="email"
                placeholder="Work Email"
                value={leadFormData.email}
                onChange={(e) => setLeadFormData({ ...leadFormData, email: e.target.value })}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg focus:outline-none focus:border-purple-500 transition"
                required
              />

              <input
                type="text"
                placeholder="Company Name"
                value={leadFormData.company}
                onChange={(e) => setLeadFormData({ ...leadFormData, company: e.target.value })}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg focus:outline-none focus:border-purple-500 transition"
                required
              />

              <select
                value={leadFormData.size}
                onChange={(e) => setLeadFormData({ ...leadFormData, size: e.target.value })}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg focus:outline-none focus:border-purple-500 transition text-slate-300"
              >
                <option value="1-10">1-10 employees</option>
                <option value="11-50">11-50 employees</option>
                <option value="51-500">51-500 employees</option>
                <option value="500+">500+ employees</option>
              </select>

              <button
                type="submit"
                disabled={leadFormSubmitting}
                className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 rounded-lg font-bold transition flex items-center justify-center gap-2"
              >
                {leadFormSubmitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Sending...
                  </>
                ) : (
                  <>
                    Download ROI Calculator
                    <ArrowRight size={20} />
                  </>
                )}
              </button>

              <p className="text-xs text-slate-500 text-center">
                We'll never share your info. See our{" "}
                <Link to="/privacy" className="text-purple-400 hover:text-purple-300 underline">
                  Privacy Policy
                </Link>
                .
              </p>
            </form>
          )}
        </div>
      </section>

      {/* --- TESTIMONIALS SECTION --- */}
      <section className="py-24 bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-black mb-4">Loved by Developers</h2>
            <p className="text-xl text-slate-400">Real feedback from real teams</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                name: "Alice Chen",
                role: "VP Engineering, Acme Corp",
                text: "Saved us 3 weeks on a critical feature. The quality is indistinguishable from our best engineers.",
                avatar: "🧑‍💼",
              },
              {
                name: "Marcus Johnson",
                role: "Founder, TechStartup",
                text: "Cut our development costs by 60% while actually shipping faster. Game changer.",
                avatar: "👨‍💻",
              },
              {
                name: "Sarah Williams",
                role: "CTO, Digital Agency",
                text: "Our clients see no difference. Our velocity doubled. We charge more and deliver faster.",
                avatar: "👩‍💼",
              },
            ].map((testimonial, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="p-6 bg-slate-800/50 border border-purple-500/20 rounded-lg hover:border-purple-500/50 transition"
              >
                <div className="flex items-center gap-4 mb-4">
                  <span className="text-4xl">{testimonial.avatar}</span>
                  <div>
                    <h4 className="font-bold">{testimonial.name}</h4>
                    <p className="text-sm text-slate-400">{testimonial.role}</p>
                  </div>
                </div>

                <div className="flex gap-1 mb-3">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={16} className="fill-yellow-400 text-yellow-400" />
                  ))}
                </div>

                <p className="text-slate-300 italic">"{testimonial.text}"</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* --- FOOTER --- */}
      <footer className="border-t border-purple-500/20 bg-slate-950/50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            {/* Brand */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <Zap className="text-white" size={20} />
                </div>
                <span className="font-bold text-lg bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                  TitanForge
                </span>
              </div>
              <p className="text-sm text-slate-400">
                AI-powered development agency. Ship faster, save more.
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 className="font-bold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li>
                  <a href="#features" className="hover:text-white transition">
                    Features
                  </a>
                </li>
                <li>
                  <a href="#pricing" className="hover:text-white transition">
                    Pricing
                  </a>
                </li>
                <li>
                  <Link to="/blog" className="hover:text-white transition">
                    Blog
                  </Link>
                </li>
              </ul>
            </div>

            {/* Legal */}
            <div>
              <h4 className="font-bold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li>
                  <Link to="/privacy" className="hover:text-white transition">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link to="/terms" className="hover:text-white transition">
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link to="/data-sale" className="hover:text-white transition">
                    Data Sale Agreement
                  </Link>
                </li>
                <li>
                  <Link to="/affiliate" className="hover:text-white transition">
                    Affiliate Disclaimer
                  </Link>
                </li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h4 className="font-bold mb-4">Contact</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li>
                  <a href="mailto:support@titanforge.com" className="hover:text-white transition">
                    support@titanforge.com
                  </a>
                </li>
                <li>
                  <a href="mailto:sales@titanforge.com" className="hover:text-white transition">
                    sales@titanforge.com
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-700/50 pt-8 flex flex-col sm:flex-row items-center justify-between text-sm text-slate-500">
            <p>&copy; 2026 TitanForge. All rights reserved.</p>
            <div className="flex gap-6 mt-4 sm:mt-0">
              <a href="#" className="hover:text-slate-300 transition">
                Twitter
              </a>
              <a href="#" className="hover:text-slate-300 transition">
                LinkedIn
              </a>
              <a href="#" className="hover:text-slate-300 transition">
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
