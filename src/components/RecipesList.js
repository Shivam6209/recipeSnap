import React, { useState } from 'react';
import { Clock, Users, ChefHat, Globe, Star, ChevronDown, ChevronUp } from 'lucide-react';

const RecipeCard = ({ recipe, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy':
        return 'text-green-600 bg-green-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'hard':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="recipe-card bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
      {/* Recipe Header */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-start justify-between mb-4">
          <h3 className="text-2xl font-bold text-gray-800 flex-1">
            {recipe.name}
          </h3>
          <div className="flex items-center space-x-2 ml-4">
            <Star className="w-5 h-5 text-yellow-500" />
            <span className="text-sm text-gray-600">AI Generated</span>
          </div>
        </div>
        
        <p className="text-gray-600 mb-4">{recipe.description}</p>
        
        {/* Recipe Meta Info */}
        <div className="flex flex-wrap items-center gap-4 text-sm">
          {recipe.prep_time && (
            <div className="flex items-center text-gray-600">
              <Clock className="w-4 h-4 mr-1" />
              <span>Prep: {recipe.prep_time}</span>
            </div>
          )}
          
          {recipe.cook_time && (
            <div className="flex items-center text-gray-600">
              <Clock className="w-4 h-4 mr-1" />
              <span>Cook: {recipe.cook_time}</span>
            </div>
          )}
          
          {recipe.servings && (
            <div className="flex items-center text-gray-600">
              <Users className="w-4 h-4 mr-1" />
              <span>{recipe.servings} servings</span>
            </div>
          )}
          
          {recipe.difficulty && (
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(recipe.difficulty)}`}>
              {recipe.difficulty}
            </span>
          )}
          
          {recipe.cuisine_type && (
            <div className="flex items-center text-gray-600">
              <Globe className="w-4 h-4 mr-1" />
              <span>{recipe.cuisine_type}</span>
            </div>
          )}
        </div>
      </div>

      {/* Expandable Content */}
      <div className="p-6">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full flex items-center justify-between text-left mb-4 p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200"
        >
          <span className="font-semibold text-gray-800">
            View Full Recipe
          </span>
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-600" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-600" />
          )}
        </button>

        {isExpanded && (
          <div className="space-y-6 fade-in">
            {/* Ingredients */}
            <div>
              <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                <ChefHat className="w-5 h-5 mr-2 text-indigo-600" />
                Ingredients
              </h4>
              <ul className="space-y-2">
                {recipe.ingredients.map((ingredient, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="w-2 h-2 bg-indigo-600 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    <span className="text-gray-700">{ingredient}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Instructions */}
            <div>
              <h4 className="font-semibold text-gray-800 mb-3">Instructions</h4>
              <ol className="space-y-3">
                {recipe.instructions.map((instruction, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="bg-indigo-600 text-white text-sm font-bold rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                      {idx + 1}
                    </span>
                    <span className="text-gray-700">{instruction}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const RecipesList = ({ recipes }) => {
  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="flex items-center mb-8">
        <ChefHat className="w-8 h-8 text-purple-600 mr-3" />
        <h2 className="text-3xl font-bold text-gray-800">
          Step 3: Your AI-Generated Recipes
        </h2>
      </div>

      {recipes.length > 0 ? (
        <div className="space-y-6">
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
            <p className="text-purple-800">
              <strong>{recipes.length} delicious recipe{recipes.length > 1 ? 's' : ''}</strong> generated 
              based on your ingredients. Click on any recipe to view the full details!
            </p>
          </div>

          <div className="grid gap-6">
            {recipes.map((recipe, index) => (
              <RecipeCard key={index} recipe={recipe} index={index} />
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <ChefHat className="w-16 h-16 mx-auto" />
          </div>
          <p className="text-xl text-gray-600">No recipes generated</p>
          <p className="text-gray-500 mt-2">
            Try adding more ingredients or check your connection
          </p>
        </div>
      )}
    </div>
  );
};

export default RecipesList; 