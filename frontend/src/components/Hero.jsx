/**
 * Hero Section Component
 */

import React, { useState, useEffect } from 'react';

export default function Hero() {
  const [isVisible, setIsVisible] = useState(false);

  const handleGetStarted = () => {
    document.getElementById('predict').scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const handleScroll = () => {
      const element = document.getElementById('hero-animation');
      if (element) {
        const rect = element.getBoundingClientRect();
        const isElementVisible = rect.top < window.innerHeight * 0.75;
        setIsVisible(isElementVisible);
      }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Check initial visibility
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <section className="relative py-20 sm:py-32 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-50 via-transparent to-purple-50 -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="animate-fadeInUp">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-900 leading-tight mb-6">
              AI-Powered Pneumonia Detection from
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500"> Chest X-rays</span>
            </h1>
            <p className="text-lg text-slate-600 mb-8 leading-relaxed">
              Upload X-ray images and receive instant AI-assisted screening results. Powered by advanced deep learning models for accurate pneumonia detection.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <button 
                onClick={handleGetStarted}
                className="btn-primary"
              >
                Upload X-ray
              </button>
              <button 
                onClick={() => document.getElementById('how-it-works').scrollIntoView({ behavior: 'smooth' })} 
                className="btn-secondary"
              >
                Learn More
              </button>
            </div>

            {/* Features */}
            <div className="grid grid-cols-2 gap-4 mt-12">
              <div>
                <p className="text-3xl font-bold text-blue-500">98%</p>
                <p className="text-slate-600">Accuracy</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-blue-500">10K+</p>
                <p className="text-slate-600">Predictions</p>
              </div>
            </div>
          </div>

          {/* Right Image - Animated Scanning & Monitor */}
          <div id="hero-animation" className="hidden md:block animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
            <style>{`
              @keyframes scan {
                0% {
                  top: -100%;
                  opacity: 0.8;
                }
                50% {
                  opacity: 1;
                }
                100% {
                  top: 100%;
                  opacity: 0.3;
                }
              }

              @keyframes xrayPulse {
                0%, 100% {
                  opacity: 0.6;
                }
                50% {
                  opacity: 1;
                }
              }

              @keyframes monitorFade {
                0% {
                  opacity: 0;
                  transform: scale(0.95);
                }
                100% {
                  opacity: 1;
                  transform: scale(1);
                }
              }

              @keyframes resultsPulse {
                0% {
                  opacity: 0;
                  transform: translateY(10px);
                }
                100% {
                  opacity: 1;
                  transform: translateY(0);
                }
              }

              .animate-scan {
                animation: scan 2s ease-in-out infinite;
              }

              .animate-xray-pulse {
                animation: xrayPulse 1.5s ease-in-out infinite;
              }

              .animate-monitor-fade {
                animation: monitorFade 3s ease-out forwards;
              }

              .animate-results-pulse {
                animation: resultsPulse 1s ease-out forwards;
                animation-delay: 2s;
              }
            `}</style>

            <div className="relative">
              {/* Glow background */}
              <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 rounded-2xl blur-3xl opacity-20" />
              
              {/* Main Container */}
              <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 shadow-2xl overflow-hidden">
                
                {/* X-ray Stage (showing first) */}
                {!isVisible && (
                  <div className="aspect-square bg-gradient-to-br from-slate-700 to-slate-800 rounded-lg flex items-center justify-center relative overflow-hidden">
                    {/* Scan line */}
                    <div className="absolute inset-0 animate-scan">
                      <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent" />
                    </div>

                    {/* X-ray image placeholder */}
                    <div className={`text-center ${isVisible ? '' : 'animate-xray-pulse'}`}>
                      <svg className="w-24 h-24 mx-auto text-cyan-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <p className="text-cyan-400 text-sm font-semibold">Scanning X-ray...</p>
                      <p className="text-slate-400 text-xs mt-2">Processing with AI</p>
                    </div>
                  </div>
                )}

                {/* Monitor WITH Results (showing after scroll) */}
                {isVisible && (
                  <div className="aspect-square bg-gradient-to-br from-slate-700 to-slate-800 rounded-lg overflow-hidden animate-monitor-fade relative">
                    {/* Monitor bezel */}
                    <div className="absolute inset-4 border-2 border-slate-600 rounded-lg overflow-hidden">
                      {/* Monitor screen */}
                      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 to-blue-900 p-4 flex flex-col justify-between">
                        {/* Screen header */}
                        <div className="text-xs text-cyan-400 font-mono mb-2">
                          <p>SYNAPSE-X ANALYSIS v1.0</p>
                          <p className="text-green-400">&gt; Status: COMPLETE</p>
                        </div>

                        {/* Result content */}
                        <div className="animate-results-pulse text-center flex-1 flex flex-col justify-center">
                          <p className="text-cyan-400 text-xs mb-2 font-mono">PREDICTION:</p>
                          <p className="text-green-400 text-lg font-bold mb-3">✓ NORMAL</p>
                          <p className="text-slate-300 text-xs mb-3">Confidence: 94.2%</p>
                          
                          {/* Progress bar */}
                          <div className="bg-slate-700 rounded-full h-1 mb-3 overflow-hidden">
                            <div className="bg-gradient-to-r from-cyan-400 to-green-400 h-full" style={{ width: '94.2%' }} />
                          </div>

                          <p className="text-slate-400 text-xs">No pneumonia detected</p>
                        </div>

                        {/* Footer */}
                        <div className="text-xs text-slate-500 font-mono">
                          <p>&gt; Ready for new scan</p>
                        </div>
                      </div>
                    </div>

                    {/* Monitor stand */}
                    <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-16 h-2 bg-slate-600 rounded-t-lg" />
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
