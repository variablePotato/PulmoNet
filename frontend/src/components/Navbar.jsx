/**
 * Navigation Bar Component
 */

import React from 'react';

export default function Navbar() {
  const handleGetStarted = () => {
    document.getElementById('predict').scrollIntoView({ behavior: 'smooth' });
  };

  const handleNavClick = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur-md shadow-sm border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2 cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-500 rounded-lg flex items-center justify-center shadow-lg shadow-purple-500/50 border border-purple-400">
              <span className="text-white font-bold text-lg">X</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">SYNAPSE-X</h1>
              <p className="text-xs text-slate-500">Pneumonia Detection</p>
            </div>
          </div>

          {/* Navigation */}
          <div className="hidden sm:flex items-center space-x-8">
            <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="text-slate-600 hover:text-slate-900 font-medium transition-colors bg-none border-none cursor-pointer">
              Home
            </button>
            <button onClick={() => handleNavClick('predict')} className="text-slate-600 hover:text-slate-900 font-medium transition-colors bg-none border-none cursor-pointer">
              Predict
            </button>
            <button onClick={() => handleNavClick('how-it-works')} className="text-slate-600 hover:text-slate-900 font-medium transition-colors bg-none border-none cursor-pointer">
              How It Works
            </button>
            <button onClick={() => handleNavClick('features')} className="text-slate-600 hover:text-slate-900 font-medium transition-colors bg-none border-none cursor-pointer">
              Contact
            </button>
          </div>

          {/* CTA Button */}
          <button onClick={handleGetStarted} className="btn-primary hidden sm:block">
            Get Started
          </button>
        </div>
      </div>
    </nav>
  );
}
