import React, { useState } from 'react';
import ImageUpload from './ImageUpload';
import IngredientsList from './IngredientsList';
import RecipesList from './RecipesList';
import LoadingSpinner from './LoadingSpinner';
import { ChefHat, Camera, Sparkles } from 'lucide-react';

const RecipeSnap = () => {
  const [ingredients, setIngredients] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState('upload'); // upload, ingredients, recipes

  const handleImageAnalysis = async (analysisResult) => {
    setIngredients(analysisResult.ingredients);
    setRecipes(analysisResult.recipes);
    
    if (analysisResult.ingredients.length > 0) {
      setCurrentStep('ingredients');
      if (analysisResult.recipes.length > 0) {
        setTimeout(() => setCurrentStep('recipes'), 1000);
      }
    }
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setLoading(false);
  };

  const resetApp = () => {
    setIngredients([]);
    setRecipes([]);
    setError(null);
    setCurrentStep('upload');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 fade-in">
          <div className="flex items-center justify-center mb-4">
            <ChefHat className="w-12 h-12 text-indigo-600 mr-3" />
            <h1 className="text-5xl font-bold text-gray-800">RecipeSnap</h1>
            <Sparkles className="w-8 h-8 text-yellow-500 ml-3" />
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered cooking assistant that turns your fridge ingredients into delicious recipes
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 fade-in">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
            <button 
              onClick={() => setError(null)}
              className="float-right text-red-700 hover:text-red-900"
            >
              ×
            </button>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && (
          <div className="flex justify-center mb-8">
            <LoadingSpinner />
          </div>
        )}

        {/* Main Content */}
        <div className="space-y-8">
          {/* Step 1: Image Upload */}
          {currentStep === 'upload' && (
            <div className="fade-in">
              <div className="bg-white rounded-2xl shadow-xl p-8">
                <div className="flex items-center mb-6">
                  <Camera className="w-8 h-8 text-indigo-600 mr-3" />
                  <h2 className="text-3xl font-bold text-gray-800">
                    Step 1: Upload Your Fridge Photo
                  </h2>
                </div>
                <ImageUpload 
                  onAnalysisComplete={handleImageAnalysis}
                  onError={handleError}
                  setLoading={setLoading}
                />
              </div>
            </div>
          )}

          {/* Step 2: Ingredients Display */}
          {(currentStep === 'ingredients' || currentStep === 'recipes') && ingredients.length > 0 && (
            <div className="fade-in">
              <IngredientsList 
                ingredients={ingredients}
                onIngredientsUpdate={setIngredients}
              />
            </div>
          )}

          {/* Step 3: Recipes Display */}
          {currentStep === 'recipes' && recipes.length > 0 && (
            <div className="fade-in">
              <RecipesList recipes={recipes} />
            </div>
          )}

          {/* Reset Button */}
          {currentStep !== 'upload' && (
            <div className="text-center fade-in">
              <button
                onClick={resetApp}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-8 rounded-full transition duration-300 transform hover:scale-105"
              >
                Start Over
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-16 text-gray-500">
          <p>Powered by AI • Made with ❤️ for home cooks</p>
        </div>
      </div>
    </div>
  );
};

export default RecipeSnap; 