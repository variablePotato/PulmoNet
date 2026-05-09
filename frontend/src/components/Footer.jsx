import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const handleNavClick = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="bg-slate-900 text-slate-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <div>
            <div className="flex items-center space-x-2 mb-4 cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
              <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-500 rounded-lg flex items-center justify-center shadow-lg shadow-purple-500/50 border border-purple-400">
                <span className="text-white font-bold">X</span>
              </div>
              <div>
                <h3 className="font-bold text-white">SYNAPSE-X</h3>
                <p className="text-xs">AI Pneumonia Detection</p>
              </div>
            </div>
            <p className="text-sm text-slate-400">
              Professional medical AI platform for chest X-ray analysis
            </p>
          </div>

          <div>
            <h4 className="font-bold text-white mb-4">Product</h4>
            <ul className="space-y-2 text-sm">
              <li><button onClick={() => handleNavClick('features')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Features</button></li>
              <li><button onClick={() => handleNavClick('how-it-works')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">How It Works</button></li>
              <li><button onClick={() => handleNavClick('predict')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">API Docs</button></li>
              <li><button onClick={() => handleNavClick('predict')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Integrations</button></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-white mb-4">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><button onClick={() => alert('About page coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">About</button></li>
              <li><button onClick={() => alert('Blog coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Blog</button></li>
              <li><button onClick={() => alert('Contact us at info@synapse-x.ai')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Contact</button></li>
              <li><button onClick={() => alert('Careers page coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Careers</button></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-white mb-4">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li><button onClick={() => alert('Privacy Policy coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Privacy</button></li>
              <li><button onClick={() => alert('Terms of Service coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Terms</button></li>
              <li><button onClick={() => alert('Security page coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Security</button></li>
              <li><button onClick={() => alert('Compliance info coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Compliance</button></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-12">
          <div className="bg-blue-900/30 border border-blue-700/30 rounded-lg p-4 mb-8">
            <p className="text-xs text-slate-300 leading-relaxed">
              <strong>Medical Disclaimer:</strong> SYNAPSE-X is an AI-assisted screening tool designed to support radiologists and healthcare professionals. 
              It is not a substitute for professional medical diagnosis, treatment, or advice. Always consult qualified healthcare professionals for medical decisions. 
              Results should be interpreted in clinical context by licensed medical practitioners.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row justify-between items-center">
            <p className="text-sm text-slate-400">
              © {currentYear} SYNAPSE-X. All rights reserved.
            </p>
            <div className="flex items-center gap-6 mt-4 sm:mt-0">
              <button onClick={() => alert('Twitter: @SYNAPSE_X')} className="text-slate-400 hover:text-white transition-colors bg-none border-none cursor-pointer">Twitter</button>
              <button onClick={() => alert('GitHub: coming soon')} className="text-slate-400 hover:text-white transition-colors bg-none border-none cursor-pointer">GitHub</button>
              <button onClick={() => alert('LinkedIn: coming soon')} className="text-slate-400 hover:text-white transition-colors bg-none border-none cursor-pointer">LinkedIn</button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
