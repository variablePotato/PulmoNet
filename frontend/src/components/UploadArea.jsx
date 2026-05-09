/**
 * Image Upload Area Component
 */

import React, { useState, useRef } from 'react';

export default function UploadArea({ onFilesSelected, isLoading }) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    onFilesSelected(files);
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    onFilesSelected(files);
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        relative border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 cursor-pointer
        ${isDragging 
          ? 'border-blue-500 bg-blue-50' 
          : 'border-slate-300 bg-slate-50 hover:border-blue-400 hover:bg-blue-50'
        }
        ${isLoading ? 'opacity-50 pointer-events-none' : ''}
      `}
      onClick={() => !isLoading && fileInputRef.current?.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".jpg,.jpeg,.png"
        onChange={handleFileSelect}
        className="hidden"
        disabled={isLoading}
      />

      <svg className="w-16 h-16 mx-auto mb-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3v-6" />
      </svg>

      <p className="text-xl font-semibold text-slate-900 mb-2">
        Drag & drop images here
      </p>
      <p className="text-slate-600 mb-4">
        or click to select files
      </p>

      <p className="text-sm text-slate-500">
        Supported formats: JPG, JPEG, PNG (Max 10 images, 10 MB each)
      </p>

      <p className="text-xs text-slate-400 mt-3 italic">
        📋 Recommended image quality: clear chest X-ray image
      </p>
    </div>
  );
}
