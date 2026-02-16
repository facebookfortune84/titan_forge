import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export default function PrivacyPage() {
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
        <h1 className="text-4xl font-bold text-white mb-8">Privacy Policy</h1>
        
        <div className="prose prose-invert max-w-none text-slate-300 space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-white mb-4">1. Introduction</h2>
            <p>
              TitanForge ("we," "us," or "our") operates the TitanForge platform. This page informs you
              of our policies regarding the collection, use, and disclosure of personal data when you use
              our service and the choices you have associated with that data.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">2. Information Collection and Use</h2>
            <p>We collect several different types of information for various purposes to provide and improve
              our service to you.
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>Personal Data: Email address, first name, last name, company name, company size</li>
              <li>Usage Data: Information about how you access and use the service</li>
              <li>Cookies and Similar Tracking Technologies</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">3. Use of Data</h2>
            <p>TitanForge uses the collected data for various purposes:</p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>To provide and maintain our service</li>
              <li>To notify you about changes to our service</li>
              <li>To allow you to participate in interactive features</li>
              <li>To provide customer support</li>
              <li>To gather analysis or valuable information to improve the service</li>
              <li>To monitor the usage of our service</li>
              <li>To detect, prevent and address technical and security issues</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">4. Security of Data</h2>
            <p>
              The security of your data is important to us but remember that no method of transmission over
              the Internet or method of electronic storage is 100% secure. While we strive to use commercially
              acceptable means to protect your Personal Data, we cannot guarantee its absolute security.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">5. Contact Us</h2>
            <p>
              If you have any questions about this Privacy Policy, please contact us at:
              <br /> Email: privacy@titanforge.io
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
