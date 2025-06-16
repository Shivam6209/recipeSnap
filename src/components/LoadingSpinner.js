import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ message = "Analyzing your ingredients..." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
        <div className="absolute inset-0 w-12 h-12 border-4 border-indigo-200 rounded-full animate-pulse"></div>
      </div>
      <p className="mt-4 text-lg font-medium text-gray-700">{message}</p>
      <p className="mt-2 text-sm text-gray-500">This may take a few moments...</p>
      
      {/* Progress dots */}
      <div className="flex space-x-1 mt-4">
        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></div>
        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
      </div>
    </div>
  );
};

export default LoadingSpinner; 