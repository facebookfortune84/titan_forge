import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export default function TermsPage() {
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
        <h1 className="text-4xl font-bold text-white mb-8">Terms of Service</h1>
        
        <div className="prose prose-invert max-w-none text-slate-300 space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-white mb-4">1. Terms</h2>
            <p>
              By accessing and using this website and service, you accept and agree to be bound by the terms
              and provision of this agreement. TitanForge reserves the right to modify these terms at any time.
              Your continued use signifies acceptance of these changes.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">2. Use License</h2>
            <p>
              Permission is granted to temporarily download one copy of the materials (information or software)
              on TitanForge's website for personal, non-commercial transitory viewing only. This is the grant of
              a license, not a transfer of title, and under this license you may not:
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>Modifying or copying the materials</li>
              <li>Using the materials for any commercial purpose or for any public display</li>
              <li>Attempting to decompile or reverse engineer any software contained on the website</li>
              <li>Removing any copyright or other proprietary notations from the materials</li>
              <li>Transferring the materials to another person or "mirroring" the materials on any other server</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">3. Disclaimer</h2>
            <p>
              The materials on TitanForge's website are provided on an 'as is' basis. TitanForge makes no
              warranties, expressed or implied, and hereby disclaims and negates all other warranties including,
              without limitation, implied warranties or conditions of merchantability, fitness for a particular
              purpose, or non-infringement of intellectual property or other violation of rights.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">4. Limitations</h2>
            <p>
              In no event shall TitanForge or its suppliers be liable for any damages (including, without
              limitation, damages for loss of data or profit, or due to business interruption) arising out of
              the use or inability to use the materials on TitanForge's website.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">5. Accuracy of Materials</h2>
            <p>
              The materials appearing on TitanForge's website could include technical, typographical, or
              photographic errors. TitanForge does not warrant that any of the materials on its website are
              accurate, complete, or current. TitanForge may make changes to the materials contained on its
              website at any time without notice.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">6. Links</h2>
            <p>
              TitanForge has not reviewed all of the sites linked to its website and is not responsible for
              the contents of any such linked site. The inclusion of any link does not imply endorsement by
              TitanForge of the site. Use of any such linked website is at the user's own risk.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">7. Modifications</h2>
            <p>
              TitanForge may revise these terms of service for its website at any time without notice. By using
              this website, you are agreeing to be bound by the then current version of these terms of service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-white mb-4">8. Governing Law</h2>
            <p>
              These terms and conditions are governed by and construed in accordance with the laws of the United
              States, and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
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
