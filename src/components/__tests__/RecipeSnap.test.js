import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import RecipeSnap from '../RecipeSnap';

// Mock the child components
jest.mock('../ImageUpload', () => {
  return function MockImageUpload({ onAnalysisComplete }) {
    return (
      <div data-testid="image-upload">
        <button 
          onClick={() => onAnalysisComplete({
            ingredients: ['tomato', 'onion'],
            recipes: []
          })}
        >
          Mock Upload
        </button>
      </div>
    );
  };
});

jest.mock('../IngredientsList', () => {
  return function MockIngredientsList({ ingredients }) {
    return (
      <div data-testid="ingredients-list">
        {ingredients.map(ingredient => (
          <span key={ingredient}>{ingredient}</span>
        ))}
      </div>
    );
  };
});

jest.mock('../RecipesList', () => {
  return function MockRecipesList({ recipes }) {
    return (
      <div data-testid="recipes-list">
        {recipes.length} recipes
      </div>
    );
  };
});

jest.mock('../LoadingSpinner', () => {
  return function MockLoadingSpinner() {
    return <div data-testid="loading-spinner">Loading...</div>;
  };
});

describe('RecipeSnap', () => {
  test('renders main heading', () => {
    render(<RecipeSnap />);
    expect(screen.getByText('RecipeSnap')).toBeInTheDocument();
  });

  test('shows upload step initially', () => {
    render(<RecipeSnap />);
    expect(screen.getByText('Step 1: Upload Your Fridge Photo')).toBeInTheDocument();
    expect(screen.getByTestId('image-upload')).toBeInTheDocument();
  });

  test('handles image analysis and shows ingredients', async () => {
    render(<RecipeSnap />);
    
    const uploadButton = screen.getByText('Mock Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByTestId('ingredients-list')).toBeInTheDocument();
      expect(screen.getByText('tomato')).toBeInTheDocument();
      expect(screen.getByText('onion')).toBeInTheDocument();
    });
  });

  test('shows start over button after analysis', async () => {
    render(<RecipeSnap />);
    
    const uploadButton = screen.getByText('Mock Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByText('Start Over')).toBeInTheDocument();
    });
  });

  test('resets app when start over is clicked', async () => {
    render(<RecipeSnap />);
    
    // Trigger analysis
    const uploadButton = screen.getByText('Mock Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByText('Start Over')).toBeInTheDocument();
    });

    // Click start over
    const startOverButton = screen.getByText('Start Over');
    fireEvent.click(startOverButton);

    // Should be back to upload step
    expect(screen.getByText('Step 1: Upload Your Fridge Photo')).toBeInTheDocument();
  });
}); 