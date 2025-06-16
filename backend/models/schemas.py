"""
Pydantic schemas for API request and response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Recipe(BaseModel):
    """Recipe model"""
    name: str = Field(..., description="Recipe name")
    description: str = Field(..., description="Brief recipe description")
    ingredients: List[str] = Field(..., description="List of ingredients needed")
    instructions: List[str] = Field(..., description="Step-by-step cooking instructions")
    prep_time: Optional[str] = Field(None, description="Preparation time")
    cook_time: Optional[str] = Field(None, description="Cooking time")
    servings: Optional[int] = Field(None, description="Number of servings")
    difficulty: Optional[str] = Field(None, description="Difficulty level (Easy, Medium, Hard)")
    cuisine_type: Optional[str] = Field(None, description="Type of cuisine")

class IngredientResponse(BaseModel):
    """Response model for ingredient identification"""
    ingredients: List[str] = Field(..., description="List of identified ingredients")
    message: str = Field(..., description="Response message")
    confidence_scores: Optional[Dict[str, float]] = Field(None, description="Confidence scores for each ingredient")

class RecipeResponse(BaseModel):
    """Response model for recipe generation"""
    recipes: List[Recipe] = Field(..., description="List of generated recipes")
    ingredients_used: List[str] = Field(..., description="Ingredients that were used for recipe generation")
    message: str = Field(..., description="Response message")

class RecipeRequest(BaseModel):
    """Request model for recipe generation"""
    ingredients: List[str] = Field(..., description="List of available ingredients")
    dietary_restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions (vegetarian, vegan, gluten-free, etc.)")
    cuisine_preference: Optional[str] = Field(None, description="Preferred cuisine type")
    difficulty_level: Optional[str] = Field(None, description="Preferred difficulty level")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code") 