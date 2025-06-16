import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon, X } from 'lucide-react';
import axios from 'axios';
import API_CONFIG from '../config/api';

const ImageUpload = ({ onAnalysisComplete, onError, setLoading }) => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  });

  const analyzeImage = async () => {
    if (!uploadedImage) {
      onError('Please select an image first');
      return;
    }

    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', uploadedImage);

      const response = await axios.post(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.FULL_ANALYSIS}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000 // 60 seconds timeout
      });

      if (response.data) {
        onAnalysisComplete(response.data);
      } else {
        onError('No data received from server');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      
      if (error.code === 'ECONNABORTED') {
        onError('Request timed out. Please try again with a smaller image.');
      } else if (error.response) {
        onError(`Server error: ${error.response.data.detail || error.response.statusText}`);
      } else if (error.request) {
        onError('Unable to connect to server. Please check if the backend is running.');
      } else {
        onError(`Error: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const removeImage = () => {
    setUploadedImage(null);
    setImagePreview(null);
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      {!imagePreview ? (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
            isDragActive
              ? 'border-indigo-500 bg-indigo-50'
              : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          <div className="space-y-4">
            <div className="flex justify-center">
              <Upload className="w-16 h-16 text-gray-400" />
            </div>
            <div>
              <p className="text-xl font-semibold text-gray-700">
                {isDragActive ? 'Drop your image here' : 'Upload your fridge photo'}
              </p>
              <p className="text-gray-500 mt-2">
                Drag and drop an image, or click to select
              </p>
              <p className="text-sm text-gray-400 mt-1">
                Supports: JPG, PNG, GIF, WebP (max 10MB)
              </p>
            </div>
          </div>
        </div>
      ) : (
        /* Image Preview */
        <div className="space-y-4">
          <div className="relative bg-gray-100 rounded-xl p-4">
            <button
              onClick={removeImage}
              className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition-colors duration-200"
            >
              <X className="w-4 h-4" />
            </button>
            <div className="flex items-center justify-center">
              <img
                src={imagePreview}
                alt="Uploaded preview"
                className="max-h-96 max-w-full rounded-lg shadow-md"
              />
            </div>
          </div>
          
          <div className="flex items-center justify-center space-x-4">
            <div className="flex items-center text-green-600">
              <ImageIcon className="w-5 h-5 mr-2" />
              <span className="font-medium">Image ready for analysis</span>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        {imagePreview && (
          <>
            <button
              onClick={removeImage}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              Choose Different Image
            </button>
            <button
              onClick={analyzeImage}
              className="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              Analyze Ingredients
            </button>
          </>
        )}
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-800 mb-2">Tips for best results:</h3>
        <ul className="text-blue-700 text-sm space-y-1">
          <li>• Take a clear, well-lit photo of your ingredients</li>
          <li>• Make sure ingredients are visible and not overlapping too much</li>
          <li>• Include a variety of ingredients for more recipe options</li>
          <li>• The AI works best with common fruits, vegetables, and pantry items</li>
        </ul>
      </div>
    </div>
  );
};

export default ImageUpload; 