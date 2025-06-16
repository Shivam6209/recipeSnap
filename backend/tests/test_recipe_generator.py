"""
Tests for Recipe Generation Service
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
import json

from services.recipe_generator import RecipeGenerator
from models.schemas import Recipe

class TestRecipeGenerator:
    """Test cases for RecipeGenerator"""
    
    @pytest.fixture
    def mock_recipe_generator(self):
        """Create a mock recipe generator for testing"""
        with patch('services.recipe_generator.AutoTokenizer'), \
             patch('services.recipe_generator.AutoModelForCausalLM'):
            generator = RecipeGenerator()
            return generator
    
    def test_init(self, mock_recipe_generator):
        """Test RecipeGenerator initialization"""
        assert mock_recipe_generator is not None
        assert hasattr(mock_recipe_generator, 'device')
        assert hasattr(mock_recipe_generator, 'recipe_prompt_template')
    
    def test_generate_mock_response(self, mock_recipe_generator):
        """Test mock response generation"""
        prompt = "Available ingredients: tomato, onion, chicken"
        
        response = mock_recipe_generator._generate_mock_response(prompt)
        
        assert isinstance(response, str)
        data = json.loads(response)
        assert 'recipes' in data
        assert len(data['recipes']) > 0
    
    def test_parse_recipe_response(self, mock_recipe_generator):
        """Test recipe response parsing"""
        mock_response = json.dumps({
            "recipes": [
                {
                    "name": "Test Recipe",
                    "description": "A test recipe",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "instructions": ["step1", "step2"],
                    "prep_time": "10 minutes",
                    "cook_time": "15 minutes",
                    "servings": 2,
                    "difficulty": "Easy",
                    "cuisine_type": "Test"
                }
            ]
        })
        
        recipes = mock_recipe_generator._parse_recipe_response(mock_response)
        
        assert len(recipes) == 1
        assert isinstance(recipes[0], Recipe)
        assert recipes[0].name == "Test Recipe"
    
    @pytest.mark.asyncio
    async def test_generate_recipes_success(self, mock_recipe_generator):
        """Test successful recipe generation"""
        test_ingredients = ["tomato", "onion", "chicken"]
        
        # Mock the text generation to return a valid response
        mock_recipe_generator._generate_text = Mock(return_value=json.dumps({
            "recipes": [
                {
                    "name": "Chicken Stir Fry",
                    "description": "Quick chicken stir fry",
                    "ingredients": test_ingredients,
                    "instructions": ["Cook chicken", "Add vegetables"],
                    "prep_time": "10 minutes",
                    "cook_time": "15 minutes",
                    "servings": 2,
                    "difficulty": "Easy",
                    "cuisine_type": "Asian"
                }
            ]
        }))
        
        recipes = await mock_recipe_generator.generate_recipes(test_ingredients)
        
        assert len(recipes) == 1
        assert isinstance(recipes[0], Recipe)
        assert recipes[0].name == "Chicken Stir Fry"
    
    @pytest.mark.asyncio
    async def test_generate_recipes_empty_ingredients(self, mock_recipe_generator):
        """Test recipe generation with empty ingredients"""
        with pytest.raises(ValueError):
            await mock_recipe_generator.generate_recipes([]) 