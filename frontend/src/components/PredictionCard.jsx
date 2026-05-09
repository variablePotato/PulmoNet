/**
 * Prediction Card Component
 */

import React from 'react';
import LoadingSpinner from './LoadingSpinner';

export default function PredictionCard({ prediction, imagePreview, isLoading }) {
  const isPneumonia = prediction?.prediction === 'Pneumonia';
  const confidence = prediction?.confidence || 0;

  if (isLoading) {
    return (
      <div className="card-medical p-6">
        <div className="bg-gradient-to-br from-slate-100 to-slate-200 rounded-lg mb-4 h-40 flex items-center justify-center">
          <LoadingSpinner />
        </div>
        <div className="space-y-4">
          <div className="h-6 bg-slate-200 rounded-lg animate-shimmer" />
          <div className="h-4 bg-slate-200 rounded-lg animate-shimmer w-2/3" />
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="card-medical p-6 flex items-center justify-center h-full text-slate-400">
        <p>Predictions will appear here</p>
      </div>
    );
  }

  return (
    <div className="card-medical p-6 flex flex-col h-full">
      {/* Image Preview */}
      <div className="bg-gradient-to-br from-slate-100 to-slate-200 rounded-lg overflow-hidden mb-4">
        {imagePreview ? (
          <img 
            src={imagePreview} 
            alt="Prediction"
            className="w-full h-40 object-cover"
          />
        ) : (
          <div className="w-full h-40 flex items-center justify-center">
            <span className="text-slate-400">No preview</span>
          </div>
        )}
      </div>

      {/* Prediction Result */}
      <div className="flex-1">
        {/* Status Badge */}
        <div className={`
          inline-flex items-center px-4 py-2 rounded-full font-semibold mb-4
          ${isPneumonia 
            ? 'bg-red-100 text-red-700' 
            : 'bg-green-100 text-green-700'
          }
        `}>
          {isPneumonia ? '🔴 Pneumonia Detected' : '✓ Normal'}
        </div>

        {/* Confidence Score */}
        <div className="mb-4">
          <p className="text-sm text-slate-600 mb-2">Confidence Score</p>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold text-slate-900">
              {confidence.toFixed(1)}%
            </p>
            <p className="text-slate-500 mb-1">
              {confidence > 90 ? 'High' : confidence > 70 ? 'Medium' : 'Low'}
            </p>
          </div>
        </div>

        {/* Probability Details */}
        <div className="space-y-3 pt-4 border-t border-slate-200">
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-slate-700">Normal</span>
              <span className="text-sm font-semibold text-slate-900">
                {(prediction?.probability_normal * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${prediction?.probability_normal * 100}%` }}
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-slate-700">Pneumonia</span>
              <span className="text-sm font-semibold text-slate-900">
                {(prediction?.probability_pneumonia * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
              <div 
                className="bg-red-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${prediction?.probability_pneumonia * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
