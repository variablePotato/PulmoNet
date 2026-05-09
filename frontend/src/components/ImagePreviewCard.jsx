/**
 * Image Preview Card Component
 */

import React from 'react';

export default function ImagePreviewCard({ file, index, onRemove }) {
  const [preview, setPreview] = React.useState(null);

  React.useEffect(() => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  }, [file]);

  const fileSizeMB = (file.size / 1024 / 1024).toFixed(2);

  return (
    <div className="card-medical p-4">
      {/* Image Preview */}
      <div className="relative bg-gradient-to-br from-slate-100 to-slate-200 rounded-lg overflow-hidden mb-4">
        {preview ? (
          <img 
            src={preview} 
            alt={file.name}
            className="w-full h-40 object-cover"
          />
        ) : (
          <div className="w-full h-40 flex items-center justify-center">
            <div className="animate-spin">
              <div className="w-8 h-8 border-4 border-slate-200 border-t-blue-500 rounded-full" />
            </div>
          </div>
        )}

        {/* Remove Button */}
        <button
          onClick={() => onRemove(index)}
          className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors shadow-lg"
        >
          ✕
        </button>
      </div>

      {/* File Info */}
      <div className="space-y-2">
        <p className="text-sm font-semibold text-slate-900 truncate">
          {file.name}
        </p>
        <p className="text-xs text-slate-500">
          {fileSizeMB} MB
        </p>
      </div>
    </div>
  );
}
