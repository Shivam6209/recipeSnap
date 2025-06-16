import React, { useState } from 'react';
import { Check, X, Plus, Carrot } from 'lucide-react';

const IngredientsList = ({ ingredients, onIngredientsUpdate }) => {
  const [customIngredient, setCustomIngredient] = useState('');
  const [editableIngredients, setEditableIngredients] = useState(ingredients);

  const removeIngredient = (index) => {
    const updated = editableIngredients.filter((_, i) => i !== index);
    setEditableIngredients(updated);
    onIngredientsUpdate(updated);
  };

  const addCustomIngredient = () => {
    if (customIngredient.trim() && !editableIngredients.includes(customIngredient.trim())) {
      const updated = [...editableIngredients, customIngredient.trim()];
      setEditableIngredients(updated);
      onIngredientsUpdate(updated);
      setCustomIngredient('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addCustomIngredient();
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="flex items-center mb-6">
        <Carrot className="w-8 h-8 text-green-600 mr-3" />
        <h2 className="text-3xl font-bold text-gray-800">
          Step 2: Identified Ingredients
        </h2>
      </div>

      {editableIngredients.length > 0 ? (
        <div className="space-y-6">
          {/* Ingredients Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {editableIngredients.map((ingredient, index) => (
              <div
                key={index}
                className="flex items-center justify-between bg-green-50 border border-green-200 rounded-lg px-4 py-3 group hover:bg-green-100 transition-colors duration-200"
              >
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-600 mr-2" />
                  <span className="font-medium text-gray-800">{ingredient}</span>
                </div>
                <button
                  onClick={() => removeIngredient(index)}
                  className="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 transition-all duration-200"
                  title="Remove ingredient"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {/* Add Custom Ingredient */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-3">
              Add missing ingredients:
            </h3>
            <div className="flex space-x-3">
              <input
                type="text"
                value={customIngredient}
                onChange={(e) => setCustomIngredient(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="e.g., olive oil, salt, pepper..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
              <button
                onClick={addCustomIngredient}
                disabled={!customIngredient.trim()}
                className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white font-medium rounded-lg transition-colors duration-200 flex items-center"
              >
                <Plus className="w-4 h-4 mr-1" />
                Add
              </button>
            </div>
          </div>

          {/* Summary */}
          <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
            <p className="text-indigo-800">
              <strong>{editableIngredients.length} ingredients</strong> ready for recipe generation.
              You can remove unwanted items or add missing ones above.
            </p>
          </div>
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Carrot className="w-16 h-16 mx-auto" />
          </div>
          <p className="text-xl text-gray-600">No ingredients detected</p>
          <p className="text-gray-500 mt-2">
            Try uploading a clearer image with visible ingredients
          </p>
        </div>
      )}
    </div>
  );
};

export default IngredientsList; 