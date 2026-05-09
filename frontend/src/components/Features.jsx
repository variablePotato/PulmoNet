/**
 * Features Section Component
 */

import React from 'react';

export default function Features() {
  const features = [
    {
      title: 'Fast Detection',
      description: 'Process multiple images in seconds',
      icon: '⚡'
    },
    {
      title: 'Batch Processing',
      description: 'Upload up to 10 images at once',
      icon: '📦'
    },
    {
      title: 'Accurate Screening',
      description: 'AI model trained on thousands of X-rays',
      icon: '🎯'
    },
    {
      title: 'Secure Processing',
      description: 'Your images are processed securely',
      icon: '🔒'
    },
    {
      title: 'Detailed Reports',
      description: 'Get confidence scores and probabilities',
      icon: '📈'
    },
    {
      title: 'Easy Integration',
      description: 'REST API for seamless integration',
      icon: '🔌'
    }
  ];

  return (
    <section id="features" className="py-16 sm:py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">
            Powerful Features
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Everything you need for accurate pneumonia detection
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="card-medical p-8">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-slate-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <button 
            onClick={() => document.getElementById('predict').scrollIntoView({ behavior: 'smooth' })}
            className="btn-primary"
          >
            Start Predicting Now
          </button>
        </div>
      </div>
    </section>
  );
}
