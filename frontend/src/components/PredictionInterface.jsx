/**
 * Main prediction interface.
 */

import React, { useEffect, useState } from 'react';
import ImagePreviewCard from './ImagePreviewCard';
import { submitPrediction } from '../services/apiService';

const MAX_FILES = 10;
const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];
const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png'];

const isAffectedPrediction = (prediction) => ['Affected', 'Pneumonia'].includes(prediction);

const hasAllowedExtension = (file) => {
  const extension = file.name.split('.').pop()?.toLowerCase();
  return ALLOWED_EXTENSIONS.includes(extension);
};

export default function PredictionInterface() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [responseMeta, setResponseMeta] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('PredictionInterface mounted');
  }, []);

  const validateFiles = (files) => {
    if (files.length > MAX_FILES) {
      return `Please select ${MAX_FILES} images or fewer`;
    }

    const invalidType = files.find((file) => {
      const browserTypeOk = file.type ? ALLOWED_TYPES.includes(file.type) : true;
      return !browserTypeOk || !hasAllowedExtension(file);
    });
    if (invalidType) {
      return `${invalidType.name} is not a supported image type`;
    }

    const oversized = files.find((file) => file.size > MAX_FILE_SIZE);
    if (oversized) {
      return `${oversized.name} is larger than 10 MB`;
    }

    return null;
  };

  const setSelectedFiles = (files) => {
    const validationError = validateFiles(files);
    if (validationError) {
      setError(validationError);
      return;
    }

    setUploadedFiles(files);
    setPredictions([]);
    setResponseMeta(null);
    setError(null);
  };

  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setSelectedFiles(Array.from(e.dataTransfer.files));
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleAnalyze = async () => {
    if (uploadedFiles.length === 0) {
      setError('Please upload at least one image');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await submitPrediction(uploadedFiles);
      setPredictions(response.predictions || []);
      setResponseMeta(response);
    } catch (err) {
      setError(err.message || 'Failed to analyze images');
      console.error('Prediction error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const clearAll = () => {
    setUploadedFiles([]);
    setPredictions([]);
    setResponseMeta(null);
    setError(null);
  };

  const removeFile = (indexToRemove) => {
    setUploadedFiles(uploadedFiles.filter((_, idx) => idx !== indexToRemove));
    setPredictions([]);
    setResponseMeta(null);
  };

  return (
    <section id="predict" className="py-16 sm:py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">
            Upload & Analyze
          </h2>
          <p className="text-lg text-slate-600">
            Upload chest X-ray images for instant AI-powered pneumonia screening
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            <p>{error}</p>
            <div className="mt-2 flex gap-3">
              {uploadedFiles.length > 0 && (
                <button
                  onClick={handleAnalyze}
                  disabled={isLoading}
                  className="text-sm font-semibold underline hover:no-underline disabled:opacity-50"
                >
                  Retry
                </button>
              )}
              <button
                onClick={() => setError(null)}
                className="text-sm underline hover:no-underline"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Upload X-Ray Images
            </h3>

            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className="border-2 border-dashed border-slate-300 rounded-2xl p-8 text-center bg-slate-50 hover:bg-blue-50 hover:border-blue-400 transition-all cursor-pointer mb-6"
            >
              <input
                type="file"
                multiple
                accept=".jpg,.jpeg,.png"
                onChange={handleFileChange}
                className="hidden"
                id="fileInput"
              />
              <label htmlFor="fileInput" className="cursor-pointer block">
                <svg
                  className="w-16 h-16 mx-auto mb-4 text-slate-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3v-6"
                  />
                </svg>
                <p className="text-xl font-semibold text-slate-900 mb-2">
                  Drag & drop images here
                </p>
                <p className="text-slate-600">or click to select files</p>
              </label>
            </div>

            {uploadedFiles.length > 0 && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <p className="text-sm font-semibold text-slate-900">
                    {uploadedFiles.length} image(s) selected
                  </p>
                  <button
                    onClick={clearAll}
                    disabled={isLoading}
                    className="text-red-500 hover:text-red-700 text-sm font-medium"
                  >
                    Clear All
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  {uploadedFiles.map((file, idx) => (
                    <ImagePreviewCard
                      key={`${file.name}-${idx}`}
                      file={file}
                      index={idx}
                      onRemove={removeFile}
                    />
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={uploadedFiles.length === 0 || isLoading}
              className="btn-primary w-full mt-6 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Processing...' : 'Analyze Images'}
            </button>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Prediction Results
            </h3>
            {responseMeta?.processing_time_ms != null && (
              <p className="text-sm text-slate-500 mb-3">
                Completed in {responseMeta.processing_time_ms} ms
              </p>
            )}

            <div className="bg-slate-50 rounded-2xl p-6 min-h-96 overflow-y-auto">
              {predictions.length === 0 ? (
                <div className="h-full flex items-center justify-center text-center">
                  <div>
                    <svg
                      className="w-16 h-16 mx-auto mb-4 text-slate-300"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    <p className="text-slate-500 font-medium">Upload images to see results</p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {predictions.map((pred, idx) => {
                    const isError = pred.status === 'error';
                    const isAffected = isAffectedPrediction(pred.prediction);
                    return (
                      <div key={`${pred.filename}-${idx}`} className="bg-white p-4 rounded-lg border-2 border-slate-200">
                        <div className="flex items-center justify-between gap-3 mb-3">
                          <p className="font-semibold text-slate-900 truncate">{pred.filename}</p>
                          <span
                            className={`px-3 py-1 rounded-full text-sm font-bold whitespace-nowrap ${
                              isError
                                ? 'bg-amber-100 text-amber-700'
                                : isAffected
                                ? 'bg-red-100 text-red-700'
                                : 'bg-green-100 text-green-700'
                            }`}
                          >
                            {isError ? 'Analysis Error' : isAffected ? 'Affected Lung' : 'Normal Lung'}
                          </span>
                        </div>

                        {isError ? (
                          <p className="text-sm text-amber-700">
                            {pred.error || 'Unable to analyze this image'}
                          </p>
                        ) : (
                          <div className="space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="text-sm text-slate-600">Confidence:</span>
                              <span className="font-bold text-slate-900">
                                {Number(pred.confidence || 0).toFixed(1)}%
                              </span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full transition-all ${
                                  isAffected ? 'bg-red-500' : 'bg-green-500'
                                }`}
                                style={{ width: `${Math.min(Number(pred.confidence || 0), 100)}%` }}
                              />
                            </div>
                            <div className="grid grid-cols-2 gap-3 pt-2 text-xs text-slate-600">
                              <span>Normal: {Number(pred.probability_normal || 0).toFixed(1)}%</span>
                              <span>Pneumonia: {Number(pred.probability_pneumonia || 0).toFixed(1)}%</span>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="mt-12 p-4 bg-amber-50 border border-amber-200 rounded-lg text-center">
          <p className="text-sm text-amber-800">
            <strong>Medical Disclaimer:</strong> This system is an AI-assisted screening tool and is not a substitute for professional medical diagnosis.
          </p>
        </div>
      </div>
    </section>
  );
}
