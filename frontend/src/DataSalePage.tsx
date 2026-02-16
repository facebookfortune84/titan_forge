import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export default function DataSalePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950">
      {/* Header */}
      <div className="border-b border-purple-500/20 bg-slate-950/50 backdrop-blur sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <Link to="/" className="flex items-center gap-2 text-purple-400 hover:text-purple-300">
            <ArrowLeft size={20} />
            Back to Home
          </Link>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold text-white mb-8">Data Sale Opt-Out Notice</h1>
        
        <div className="prose prose-invert max-w-none text-slate-300 space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-white mb-4">Your Privacy Rights</h2>
            <p>
              At TitanForge, we respect your privacy and your right to control how your personal information
              is used. This page explains your rights regarding the sale or sharing of your personal information.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">Data Sale Policy</h2>
            <p>
              TitanForge does NOT sell your personal information to third parties for commercial purposes.
              We may share aggregated, de-identified data for analytics and improvement purposes, but we never
              sell personal information that identifies you.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">How We Use Your Information</h2>
            <p>We use your information to:</p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>Provide and improve our service</li>
              <li>Personalize your experience</li>
              <li>Communicate with you about updates and features</li>
              <li>Analyze usage patterns (in aggregated form)</li>
              <li>Comply with legal obligations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">Your Opt-Out Rights</h2>
            <p>
              If you live in a jurisdiction with specific privacy rights (such as California, Virginia,
              Colorado, Connecticut, or Utah), you have the right to:
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>Know what personal information we have about you</li>
              <li>Request deletion of your personal information</li>
              <li>Opt-out of the sale of your personal information</li>
              <li>Request that we not discriminate against you for exercising your privacy rights</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">How to Exercise Your Rights</h2>
            <p>
              To exercise any of your privacy rights, please contact us at:
              <br /> Email: privacy@titanforge.io
              <br /> Subject: "Data Privacy Request"
            </p>
            <p className="mt-4">
              We will respond to your request within 30 days. Please note that we may need to verify your
              identity before fulfilling your request.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">Third-Party Sharing</h2>
            <p>
              We may share your information with trusted service providers who assist us in operating our
              website and conducting our business. These service providers are contractually obligated to
              keep your information confidential and use it only for the purposes we specify.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">Changes to This Notice</h2>
            <p>
              We may update this notice from time to time. We will notify you of any changes by posting the
              new notice on this page and updating the "Last updated" date below.
            </p>
          </section>

          <p className="text-sm text-slate-500 mt-12">
            Last updated: February 2026
          </p>
        </div>
      </div>
    </div>
  );
}
