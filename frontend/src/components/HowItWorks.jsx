/**
 * How It Works Section Component
 */

import React from 'react';

export default function HowItWorks() {
  const steps = [
    {
      number: '1',
      title: 'Upload X-ray',
      description: 'Upload your chest X-ray images (JPG, JPEG, or PNG)',
      icon: '📤'
    },
    {
      number: '2',
      title: 'AI Processing',
      description: 'Our deep learning model analyzes the image in real-time',
      icon: '⚙️'
    },
    {
      number: '3',
      title: 'Get Results',
      description: 'Receive instant predictions with confidence scores',
      icon: '📊'
    }
  ];

  return (
    <section id="how-it-works" className="py-16 sm:py-24 bg-gradient-to-b from-white to-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">
            How It Works
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Simple three-step process to get professional pneumonia detection results
          </p>
        </div>

        {/* Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="relative group">
              {/* Card */}
              <div className="card-medical p-8 h-full text-center">
                {/* Step Number */}
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-2xl mx-auto mb-6 group-hover:shadow-lg group-hover:scale-110 transition-all duration-300">
                  {step.number}
                </div>

                {/* Icon */}
                <div className="text-4xl mb-4">{step.icon}</div>

                {/* Title */}
                <h3 className="text-xl font-bold text-slate-900 mb-3">
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-slate-600">
                  {step.description}
                </p>
              </div>

              {/* Connector Line (hidden on mobile) */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-blue-300 to-transparent" />
              )}
            </div>
          ))}
        </div>

        {/* Process Diagram */}
        <div className="mt-16 p-8 bg-slate-100 rounded-2xl">
          <p className="text-center text-slate-600 mb-6 font-semibold">
            Complete Process Flow
          </p>
          <div className="flex items-center justify-center gap-4 flex-wrap">
            <div className="px-4 py-2 bg-white rounded-lg shadow text-sm font-medium text-slate-700">
              📁 Upload
            </div>
            <div className="text-slate-400">→</div>
            <div className="px-4 py-2 bg-white rounded-lg shadow text-sm font-medium text-slate-700">
              🔄 Preprocess
            </div>
            <div className="text-slate-400">→</div>
            <div className="px-4 py-2 bg-white rounded-lg shadow text-sm font-medium text-slate-700">
              🧠 Inference
            </div>
            <div className="text-slate-400">→</div>
            <div className="px-4 py-2 bg-white rounded-lg shadow text-sm font-medium text-slate-700">
              📊 Results
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
