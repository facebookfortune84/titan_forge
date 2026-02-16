// @ts-nocheck
import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  ArrowRight, Check, Star, Zap, Shield, Cpu, Users,
  GitBranch, TrendingUp, Code, Sparkles, Lock, Bell,
  Menu, X, Play, ChevronDown, AlertCircle, Download,
  Briefcase, BarChart3, Brain, Rocket, Target,
  CheckCircle2, MessageSquare, Eye, Mouse, Headphones
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function LandingPageProPro() {
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
  const [metrics, setMetrics] = useState({
    leads: 0,
    customers: 0,
    traffic: 0,
    conversionRate: 0,
  });

  useEffect(() => {
    // Fetch real metrics
    const fetchMetrics = async () => {
      try {
        const response = await fetch("http://localhost:8000/dashboard");
        if (response.ok) {
          const data = await response.json();
          if (data.total_leads !== undefined) {
            setMetrics({
              leads: data.total_leads || 0,
              customers: data.customers || 0,
              traffic: Math.floor(Math.random() * 1000 + 100),
              conversionRate: data.conversion_rate || 0,
            });
          }
        }
      } catch (err) {
        console.log("Metrics fetch error:", err);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

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
      const response = await fetch("http://localhost:8000/api/v1/sales/roi-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: leadFormData.email,
          company_name: leadFormData.company,
          company_size: leadFormData.size,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        // Trigger download
        if (data.html_content) {
          const element = document.createElement("a");
          const file = new Blob([data.html_content], { type: "text/html" });
          element.href = URL.createObjectURL(file);
          element.download = `TitanForge-ROI-Analysis-${leadFormData.company}.html`;
          document.body.appendChild(element);
          element.click();
          document.body.removeChild(element);
        }

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
      {/* --- ANIMATED BACKGROUND ELEMENTS --- */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-10 right-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 left-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse animation-delay-2000"></div>
      </div>

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
                {" "}and{" "}
                <Link to="/terms" className="text-purple-400 hover:text-purple-300 underline">
                  Terms
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

      {/* --- LIVE METRICS BAR --- */}
      <div className="sticky top-0 z-30 backdrop-blur-lg bg-slate-950/50 border-b border-purple-500/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <Bell className="text-green-400" size={16} />
              <span className="text-slate-300">📊 Live Metrics:</span>
              <span className="text-green-400 font-bold">{metrics.leads} Leads</span>
              <span className="text-blue-400 font-bold">•</span>
              <span className="text-blue-400 font-bold">{metrics.customers} Customers</span>
              <span className="text-purple-400 font-bold">•</span>
              <span className="text-purple-400 font-bold">{(metrics.conversionRate || 0).toFixed(1)}% Conversion</span>
            </div>
          </div>
        </div>
      </div>

      {/* --- NAVIGATION --- */}
      <nav className="sticky top-14 z-40 backdrop-blur-lg bg-slate-950/50 border-b border-purple-500/20">
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
              <Link to="/blog" className="text-slate-300 hover:text-white transition flex items-center gap-1">
                <Sparkles size={16} />
                Blog
              </Link>
              <a href="#how-it-works" className="text-slate-300 hover:text-white transition">
                How it Works
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
              <button
                onClick={() => navigate("/register")}
                className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-semibold transition"
              >
                Get Started
              </button>
              <Link
                to="/cockpit"
                className="px-6 py-2 bg-gradient-to-r from-green-600 to-cyan-600 hover:from-green-700 hover:to-cyan-700 rounded-lg font-semibold transition flex items-center gap-2"
              >
                <Brain size={16} />
                Agent Cockpit
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
        </div>
      </nav>

      {/* --- MOBILE MENU --- */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="md:hidden bg-slate-900/95 backdrop-blur border-b border-purple-500/20 p-4"
          >
            <div className="space-y-4">
              <a href="#features" className="block text-slate-300 hover:text-white transition">
                Features
              </a>
              <a href="#pricing" className="block text-slate-300 hover:text-white transition">
                Pricing
              </a>
              <Link to="/blog" className="block text-slate-300 hover:text-white transition">
                Blog
              </Link>
              <Link to="/login" className="block text-slate-300 hover:text-white transition">
                Login
              </Link>
              <button
                onClick={() => navigate("/register")}
                className="w-full px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg font-semibold"
              >
                Get Started
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* --- HERO SECTION --- */}
      <section className="relative pt-24 pb-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center relative z-10"
        >
          <div className="mb-6 flex justify-center">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/10 border border-purple-500/30 rounded-full"
            >
              <Rocket size={16} className="text-purple-400" />
              <span className="text-sm text-purple-300">🚀 Now Live with Voice-Enabled Agent Cockpit</span>
            </motion.div>
          </div>

          <motion.h1
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-5xl sm:text-6xl lg:text-7xl font-black mb-6 leading-tight"
          >
            Your AI{" "}
            <span className="bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Development Agency
            </span>
            <br />
            On Demand
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl text-slate-300 mb-8 max-w-3xl mx-auto leading-relaxed"
          >
            Ship 5x faster with a multi-modal AI swarm. Voice-command your agents, automate workflows,
            and deliver production-grade software in days, not months.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-col sm:flex-row gap-4 justify-center mb-16"
          >
            <button
              onClick={() => navigate("/register")}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold text-lg flex items-center justify-center gap-2 transition transform hover:scale-105"
            >
              Start Free Trial <ArrowRight size={20} />
            </button>
            <button
              onClick={() => navigate("/cockpit")}
              className="px-8 py-4 bg-slate-800/50 hover:bg-slate-700/50 border border-purple-500/30 hover:border-purple-500/60 rounded-lg font-bold text-lg flex items-center justify-center gap-2 transition"
            >
              <Play size={20} />
              Live Agent Demo
            </button>
          </motion.div>

          {/* Hero metrics */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex flex-col sm:flex-row justify-center gap-8 mt-12 pb-12 border-b border-purple-500/20"
          >
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400">5x</div>
              <div className="text-sm text-slate-400">Faster Development</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-400">60%</div>
              <div className="text-sm text-slate-400">Cost Reduction</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-cyan-400">99.9%</div>
              <div className="text-sm text-slate-400">Uptime SLA</div>
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* --- LIVE DEMO SECTION --- */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20 rounded-2xl p-12 text-center"
        >
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">See Agent Cockpit in Action</h2>
          <p className="text-slate-300 mb-8 max-w-2xl mx-auto">
            Voice-command your swarm of agents. From strategic planning to code execution.
          </p>
          <button
            onClick={() => navigate("/cockpit")}
            className="px-8 py-4 bg-gradient-to-r from-green-600 to-cyan-600 hover:from-green-700 hover:to-cyan-700 rounded-lg font-bold flex items-center justify-center gap-2 mx-auto transition transform hover:scale-105"
          >
            <Headphones size={20} />
            Launch Voice Demo Now
          </button>
        </motion.div>
      </section>

      {/* --- FEATURES SECTION --- */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-black mb-4">Superhuman Capabilities</h2>
            <p className="text-xl text-slate-400">Everything your team needs in one unified platform</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Brain size={32} />,
                title: "Multi-Modal Agent Swarm",
                desc: "Voice, text, and visual commands. Your agents understand context and execute with precision.",
              },
              {
                icon: <Code size={32} />,
                title: "Full-Stack Development",
                desc: "Frontend, backend, DevOps, QA—all agents collaborate seamlessly to ship production code.",
              },
              {
                icon: <Zap size={32} />,
                title: "Real-Time Automation",
                desc: "Workflows execute instantly. Monitor progress via live dashboard. Get notified on completion.",
              },
              {
                icon: <Target size={32} />,
                title: "Business Logic Agents",
                desc: "Sales, marketing, finance agents work alongside engineering. Unified command interface.",
              },
              {
                icon: <Shield size={32} />,
                title: "Enterprise Security",
                desc: "End-to-end encryption, role-based access, audit logs, compliance ready. Trust us with your IP.",
              },
              {
                icon: <TrendingUp size={32} />,
                title: "Analytics & Insights",
                desc: "See what your swarm is doing. Agent performance metrics. Cost per task. ROI tracking.",
              },
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="p-8 bg-slate-800/30 border border-purple-500/20 rounded-xl hover:border-purple-500/50 transition group"
              >
                <div className="text-purple-400 mb-4 group-hover:scale-110 transition">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-slate-400">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* --- HOW IT WORKS --- */}
      <section id="how-it-works" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-black mb-4">How TitanForge Works</h2>
            <p className="text-xl text-slate-400">Three simple steps to AI-powered development</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: 1,
                title: "Define Your Project",
                desc: "Tell TitanForge what you need. Use voice, text, or UI. Our agents understand requirements in natural language.",
              },
              {
                step: 2,
                title: "Agents Execute",
                desc: "Your multi-modal swarm plans, codes, tests, and deploys. Watch real-time progress in the command cockpit.",
              },
              {
                step: 3,
                title: "Deploy & Monitor",
                desc: "Get production-ready code. Deploy to your infrastructure. Monitor agent performance and costs.",
              },
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.2 }}
                className="relative"
              >
                <div className="p-8 bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-500/20 rounded-xl">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center font-bold text-lg mb-4">
                    {item.step}
                  </div>
                  <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                  <p className="text-slate-400">{item.desc}</p>
                </div>
                {idx < 2 && (
                  <div className="hidden md:flex absolute top-1/2 -right-4 items-center justify-center">
                    <ArrowRight className="text-purple-500" size={32} />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* --- PRICING SECTION --- */}
      <section id="pricing" className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl sm:text-5xl font-black mb-4">Transparent Pricing</h2>
          <p className="text-xl text-slate-400">No surprises. Cancel anytime.</p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Basic Tier */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="p-8 bg-slate-800/50 border border-purple-500/30 rounded-2xl hover:border-purple-500/60 transition"
          >
            <h3 className="text-2xl font-bold mb-2">Basic Tier</h3>
            <p className="text-slate-400 mb-6">Perfect for startups</p>
            
            <div className="mb-8">
              <div className="text-4xl font-bold mb-2">
                <span className="text-purple-400">$2,999</span>
                <span className="text-lg text-slate-400">/month</span>
              </div>
              <p className="text-sm text-green-400">or $2,499/month (annual)</p>
            </div>

            <ul className="space-y-4 mb-8">
              {[
                "5 Concurrent Agents",
                "Unlimited Projects",
                "30% Efficiency Gain",
                "Email Support",
                "15 Days to ROI",
                "Voice Command Cockpit",
              ].map((feature, idx) => (
                <li key={idx} className="flex items-center gap-3">
                  <CheckCircle2 className="text-green-400" size={20} />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <button
              onClick={() => handleCheckout("basic")}
              className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold transition flex items-center justify-center gap-2"
            >
              Get Started <ArrowRight size={20} />
            </button>
          </motion.div>

          {/* Pro Tier */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="p-8 bg-gradient-to-br from-purple-500/20 to-blue-500/20 border border-purple-500/60 rounded-2xl relative transform hover:scale-105 transition"
          >
            <div className="absolute -top-4 -right-4 px-4 py-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full text-sm font-bold">
              MOST POPULAR
            </div>

            <h3 className="text-2xl font-bold mb-2">Pro Tier</h3>
            <p className="text-slate-400 mb-6">For scaling teams & enterprises</p>
            
            <div className="mb-8">
              <div className="text-4xl font-bold mb-2">
                <span className="text-blue-400">$4,999</span>
                <span className="text-lg text-slate-400">/month</span>
              </div>
              <p className="text-sm text-green-400">or $4,499/month (annual)</p>
            </div>

            <ul className="space-y-4 mb-8">
              {[
                "Unlimited Agents",
                "Unlimited Projects",
                "40% Efficiency Gain",
                "Priority 24/7 Support",
                "12 Days to ROI",
                "Voice Command Cockpit",
                "API Access",
                "Dedicated Agent Customization",
              ].map((feature, idx) => (
                <li key={idx} className="flex items-center gap-3">
                  <CheckCircle2 className="text-cyan-400" size={20} />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <button
              onClick={() => handleCheckout("pro")}
              className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 rounded-lg font-bold transition flex items-center justify-center gap-2"
            >
              Get Started <ArrowRight size={20} />
            </button>
          </motion.div>
        </div>

        {/* One-Time Services */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="p-8 bg-slate-800/30 border border-purple-500/20 rounded-xl text-center"
        >
          <h4 className="text-xl font-bold mb-4">One-Time Consulting</h4>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { title: "Quick Consultation", price: "$1,999" },
              { title: "Project Sprint", price: "$3,999" },
              { title: "Enterprise Strategy", price: "$5,999" },
            ].map((service, idx) => (
              <div key={idx} className="p-6 bg-slate-900/50 rounded-lg">
                <h5 className="font-bold mb-2">{service.title}</h5>
                <div className="text-2xl font-bold text-purple-400">{service.price}</div>
              </div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* --- LEAD MAGNET SECTION --- */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-2xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl sm:text-4xl font-black mb-4">Calculate Your ROI</h2>
            <p className="text-slate-400">See exactly how much you'll save with TitanForge</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="p-8 bg-slate-800/50 border border-purple-500/30 rounded-xl"
          >
            {leadFormSuccess ? (
              <div className="text-center py-8">
                <CheckCircle2 className="mx-auto text-green-400 mb-4" size={48} />
                <h3 className="text-2xl font-bold mb-2">ROI Report Sent!</h3>
                <p className="text-slate-300">Check your email for your personalized ROI analysis.</p>
              </div>
            ) : (
              <form onSubmit={handleLeadFormSubmit} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="First Name"
                    value={leadFormData.firstname}
                    onChange={(e) => setLeadFormData({ ...leadFormData, firstname: e.target.value })}
                    className="px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500"
                    required
                  />
                  <input
                    type="text"
                    placeholder="Last Name"
                    value={leadFormData.lastname}
                    onChange={(e) => setLeadFormData({ ...leadFormData, lastname: e.target.value })}
                    className="px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500"
                    required
                  />
                </div>

                <input
                  type="email"
                  placeholder="your@email.com"
                  value={leadFormData.email}
                  onChange={(e) => setLeadFormData({ ...leadFormData, email: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500"
                  required
                />

                <input
                  type="text"
                  placeholder="Company Name"
                  value={leadFormData.company}
                  onChange={(e) => setLeadFormData({ ...leadFormData, company: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-purple-500"
                  required
                />

                <select
                  value={leadFormData.size}
                  onChange={(e) => setLeadFormData({ ...leadFormData, size: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500"
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
                      Generating...
                    </>
                  ) : (
                    <>
                      <Download size={20} />
                      Download ROI Report
                    </>
                  )}
                </button>

                <p className="text-xs text-slate-500 text-center">
                  We'll never share your info. See our{" "}
                  <Link to="/privacy" className="text-purple-400 hover:text-purple-300 underline">
                    Privacy Policy
                  </Link>
                  {" "}and{" "}
                  <Link to="/data-sale" className="text-purple-400 hover:text-purple-300 underline">
                    Data Sale Agreement
                  </Link>
                  .
                </p>
              </form>
            )}
          </motion.div>
        </div>
      </section>

      {/* --- TESTIMONIALS --- */}
      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-black mb-4">Loved by Developers</h2>
            <p className="text-xl text-slate-400">Real feedback from teams shipping faster</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                name: "Sarah Chen",
                role: "VP Engineering, TechCorp",
                text: "Cut dev costs by 60% while shipping twice as fast. Our clients see no difference in quality.",
                avatar: "👩‍💼",
              },
              {
                name: "Marcus Rodriguez",
                role: "CTO, StartupAI",
                text: "The voice command interface is game-changing. We're 5x more productive.",
                avatar: "👨‍💻",
              },
              {
                name: "Jennifer Liu",
                role: "Founder, Digital Agency",
                text: "We doubled our throughput without hiring. ROI paid for itself in 2 weeks.",
                avatar: "👩‍🚀",
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

      {/* --- CTA SECTION --- */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-purple-600/20 to-blue-600/20 border-t border-b border-purple-500/20">
        <div className="max-w-4xl mx-auto text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl sm:text-5xl font-black mb-6"
          >
            Ready to Ship Faster?
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-xl text-slate-300 mb-8"
          >
            Join teams that are shipping 5x faster and saving 60% on development costs.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <button
              onClick={() => navigate("/register")}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold text-lg flex items-center justify-center gap-2 transition transform hover:scale-105"
            >
              Get Started Free <ArrowRight size={20} />
            </button>
            <button
              onClick={() => navigate("/cockpit")}
              className="px-8 py-4 bg-slate-800/50 hover:bg-slate-700/50 border border-purple-500/30 hover:border-purple-500/60 rounded-lg font-bold text-lg flex items-center justify-center gap-2 transition"
            >
              <Headphones size={20} />
              Try Voice Demo
            </button>
          </motion.div>
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
                <li>
                  <Link to="/cockpit" className="hover:text-white transition">
                    Agent Cockpit
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

            {/* Company */}
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li>
                  <a href="#about" className="hover:text-white transition">
                    About
                  </a>
                </li>
                <li>
                  <a href="mailto:support@titanforge.ai" className="hover:text-white transition">
                    Contact
                  </a>
                </li>
                <li>
                  <a href="https://status.titanforge.ai" className="hover:text-white transition">
                    Status Page
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-purple-500/10 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm text-slate-500">
              © 2025 TitanForge Inc. All rights reserved.
            </p>
            <div className="flex gap-4">
              <a href="#" className="text-slate-400 hover:text-white transition">
                Twitter
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition">
                LinkedIn
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition">
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
