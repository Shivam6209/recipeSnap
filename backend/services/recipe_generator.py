"""
Recipe Generation Service
Uses Mistral AI model to generate recipes based on identified ingredients
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
import os
import json
import re
from typing import List, Dict, Any
import asyncio

from models.schemas import Recipe

logger = logging.getLogger(__name__)

class RecipeGenerator:
    """
    Recipe generator using Mistral AI model
    """
    
    def __init__(self):
        """Initialize the recipe generation model"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Model cache directory
        self.cache_dir = os.getenv("MODEL_CACHE_DIR", "./models_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Initialize model
        self._load_model()
        
        # Recipe templates and prompts
        self.recipe_prompt_template = """
You are a professional chef and recipe creator. Given a list of ingredients, create detailed, delicious recipes that make the best use of these ingredients.

Available ingredients: {ingredients}

Please create 2-3 different recipes using these ingredients. For each recipe, provide:
1. Recipe name
2. Brief description
3. Complete ingredient list (including quantities)
4. Step-by-step instructions
5. Preparation time
6. Cooking time
7. Number of servings
8. Difficulty level (Easy/Medium/Hard)
9. Cuisine type

Format your response as JSON with the following structure:
{{
    "recipes": [
        {{
            "name": "Recipe Name",
            "description": "Brief description",
            "ingredients": ["ingredient 1", "ingredient 2", ...],
            "instructions": ["step 1", "step 2", ...],
            "prep_time": "X minutes",
            "cook_time": "X minutes",
            "servings": X,
            "difficulty": "Easy/Medium/Hard",
            "cuisine_type": "Cuisine Type"
        }}
    ]
}}

Make sure the recipes are practical, delicious, and use the available ingredients effectively.
"""
    
    def _load_model(self):
        """Load the Mistral model"""
        try:
            logger.info("Loading Mistral model for recipe generation...")
            model_name = "mistralai/Mistral-7B-Instruct-v0.1"
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=self.cache_dir,
                trust_remote_code=True
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with appropriate settings for CPU/GPU
            model_kwargs = {
                "cache_dir": self.cache_dir,
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if self.device.type == "cuda" else torch.float32,
                "low_cpu_mem_usage": True
            }
            
            # For CPU, use smaller precision and enable optimizations
            if self.device.type == "cpu":
                model_kwargs.update({
                    "torch_dtype": torch.float32,
                    "device_map": None
                })
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                **model_kwargs
            )
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info("Mistral model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load Mistral model: {e}")
            # Fallback to a smaller model or mock responses
            logger.warning("Falling back to mock recipe generation")
            self.model = None
            self.tokenizer = None
    
    def _generate_text(self, prompt: str, max_length: int = 1024) -> str:
        """Generate text using the Mistral model"""
        if self.model is None or self.tokenizer is None:
            return self._generate_mock_response(prompt)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            generated_text = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )
            
            return generated_text.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate text: {e}")
            return self._generate_mock_response(prompt)
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate mock recipe response when model is not available"""
        logger.info("Generating mock recipe response")
        
        # Extract ingredients from prompt
        ingredients_match = re.search(r'Available ingredients: (.+)', prompt)
        ingredients = []
        if ingredients_match:
            ingredients_text = ingredients_match.group(1)
            ingredients = [ing.strip() for ing in ingredients_text.split(',')]
        
        # Create mock recipes
        mock_recipes = {
            "recipes": [
                {
                    "name": f"Quick {ingredients[0] if ingredients else 'Vegetable'} Stir Fry",
                    "description": f"A delicious and quick stir fry featuring {', '.join(ingredients[:3]) if len(ingredients) >= 3 else 'fresh ingredients'}",
                    "ingredients": ingredients + ["soy sauce", "garlic", "ginger", "oil"],
                    "instructions": [
                        "Heat oil in a large pan or wok over medium-high heat",
                        "Add garlic and ginger, stir for 30 seconds",
                        f"Add {ingredients[0] if ingredients else 'vegetables'} and cook for 3-4 minutes",
                        "Add remaining ingredients and stir fry for 2-3 minutes",
                        "Season with soy sauce and serve hot"
                    ],
                    "prep_time": "10 minutes",
                    "cook_time": "8 minutes",
                    "servings": 2,
                    "difficulty": "Easy",
                    "cuisine_type": "Asian"
                },
                {
                    "name": f"Simple {ingredients[1] if len(ingredients) > 1 else 'Garden'} Salad",
                    "description": f"Fresh and healthy salad with {', '.join(ingredients[:2]) if len(ingredients) >= 2 else 'seasonal ingredients'}",
                    "ingredients": ingredients + ["olive oil", "lemon juice", "salt", "pepper"],
                    "instructions": [
                        "Wash and prepare all vegetables",
                        "Cut ingredients into bite-sized pieces",
                        "Combine all ingredients in a large bowl",
                        "Drizzle with olive oil and lemon juice",
                        "Season with salt and pepper, toss and serve"
                    ],
                    "prep_time": "15 minutes",
                    "cook_time": "0 minutes",
                    "servings": 2,
                    "difficulty": "Easy",
                    "cuisine_type": "Mediterranean"
                }
            ]
        }
        
        return json.dumps(mock_recipes, indent=2)
    
    def _parse_recipe_response(self, response: str) -> List[Recipe]:
        """Parse the AI response into Recipe objects"""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
            else:
                # If no JSON found, try to parse the entire response
                data = json.loads(response)
            
            recipes = []
            for recipe_data in data.get("recipes", []):
                recipe = Recipe(
                    name=recipe_data.get("name", "Unnamed Recipe"),
                    description=recipe_data.get("description", ""),
                    ingredients=recipe_data.get("ingredients", []),
                    instructions=recipe_data.get("instructions", []),
                    prep_time=recipe_data.get("prep_time"),
                    cook_time=recipe_data.get("cook_time"),
                    servings=recipe_data.get("servings"),
                    difficulty=recipe_data.get("difficulty"),
                    cuisine_type=recipe_data.get("cuisine_type")
                )
                recipes.append(recipe)
            
            return recipes
            
        except Exception as e:
            logger.error(f"Failed to parse recipe response: {e}")
            logger.debug(f"Response was: {response}")
            
            # Return a fallback recipe
            return [Recipe(
                name="Simple Mixed Dish",
                description="A simple dish using your available ingredients",
                ingredients=["Your available ingredients", "Salt", "Pepper", "Oil"],
                instructions=[
                    "Prepare all ingredients",
                    "Cook according to your preference",
                    "Season to taste",
                    "Serve hot"
                ],
                prep_time="10 minutes",
                cook_time="15 minutes",
                servings=2,
                difficulty="Easy",
                cuisine_type="Home Cooking"
            )]
    
    async def generate_recipes(self, ingredients: List[str]) -> List[Recipe]:
        """
        Generate recipes based on available ingredients
        """
        try:
            if not ingredients:
                raise ValueError("No ingredients provided")
            
            # Create prompt
            ingredients_str = ", ".join(ingredients)
            prompt = self.recipe_prompt_template.format(ingredients=ingredients_str)
            
            logger.info(f"Generating recipes for ingredients: {ingredients_str}")
            
            # Generate recipes using AI model
            response = await asyncio.to_thread(
                self._generate_text, 
                prompt, 
                max_length=1024
            )
            
            logger.debug(f"AI Response: {response}")
            
            # Parse response into Recipe objects
            recipes = self._parse_recipe_response(response)
            
            logger.info(f"Generated {len(recipes)} recipes")
            
            return recipes
            
        except Exception as e:
            logger.error(f"Failed to generate recipes: {e}")
            raise e 