"""
RecipeSnap Backend - AI Cooking Assistant
Main FastAPI application server
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any

from services.image_processor import ImageProcessor
from services.recipe_generator import RecipeGenerator
from models.schemas import RecipeResponse, IngredientResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
image_processor = None
recipe_generator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize AI models on startup"""
    global image_processor, recipe_generator
    
    logger.info("Loading AI models...")
    try:
        image_processor = ImageProcessor()
        recipe_generator = RecipeGenerator()
        logger.info("AI models loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load AI models: {e}")
        # Don't raise - allow app to start with mock responses
        image_processor = None
        recipe_generator = None
    
    yield
    
    # Cleanup (if needed)
    logger.info("Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="RecipeSnap API",
    description="AI-powered cooking assistant that identifies ingredients and suggests recipes",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RecipeSnap API is running!", "status": "healthy"}

@app.post("/analyze-ingredients", response_model=IngredientResponse)
async def analyze_ingredients(file: UploadFile = File(...)):
    """
    Analyze uploaded image to identify ingredients
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image file
        image_data = await file.read()
        
        # Process image to identify ingredients
        ingredients = await image_processor.identify_ingredients(image_data)
        
        return IngredientResponse(
            ingredients=ingredients,
            message="Ingredients identified successfully"
        )
    
    except Exception as e:
        logger.error(f"Error analyzing ingredients: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze ingredients: {str(e)}")

@app.post("/generate-recipes", response_model=RecipeResponse)
async def generate_recipes(ingredients: List[str]):
    """
    Generate recipes based on identified ingredients
    """
    if not ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")
    
    try:
        # Generate recipes using AI
        recipes = await recipe_generator.generate_recipes(ingredients)
        
        return RecipeResponse(
            recipes=recipes,
            ingredients_used=ingredients,
            message="Recipes generated successfully"
        )
    
    except Exception as e:
        logger.error(f"Error generating recipes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate recipes: {str(e)}")

@app.post("/full-analysis", response_model=Dict[str, Any])
async def full_analysis(file: UploadFile = File(...)):
    """
    Complete workflow: analyze image and generate recipes
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image file
        image_data = await file.read()
        
        # Step 1: Identify ingredients
        ingredients = await image_processor.identify_ingredients(image_data)
        
        if not ingredients:
            return {
                "ingredients": [],
                "recipes": [],
                "message": "No ingredients detected in the image"
            }
        
        # Step 2: Generate recipes
        recipes = await recipe_generator.generate_recipes(ingredients)
        
        return {
            "ingredients": ingredients,
            "recipes": recipes,
            "message": "Analysis completed successfully"
        }
    
    except Exception as e:
        logger.error(f"Error in full analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "127.0.0.1")  # Use localhost instead of 0.0.0.0
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    ) 