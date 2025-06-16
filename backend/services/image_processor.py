"""
Image Processing Service
Handles image captioning and object detection for ingredient identification
"""

import torch
from transformers import (
    VisionEncoderDecoderModel, 
    ViTImageProcessor, 
    AutoTokenizer,
    DetrImageProcessor,
    DetrForObjectDetection
)
from PIL import Image
import io
import logging
import os
import re
from typing import List, Dict, Tuple
import asyncio

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Image processor for identifying ingredients using AI models
    """
    
    def __init__(self):
        """Initialize the image processing models"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Model cache directory
        self.cache_dir = os.getenv("MODEL_CACHE_DIR", "./models_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Initialize models
        self._load_captioning_model()
        self._load_object_detection_model()
        
        # Common food ingredients for filtering
        self.food_keywords = {
            'vegetables': ['tomato', 'onion', 'carrot', 'potato', 'pepper', 'lettuce', 'spinach', 
                          'broccoli', 'cauliflower', 'cucumber', 'celery', 'garlic', 'ginger',
                          'mushroom', 'corn', 'peas', 'beans', 'cabbage', 'zucchini', 'eggplant'],
            'fruits': ['apple', 'banana', 'orange', 'lemon', 'lime', 'strawberry', 'blueberry',
                      'grape', 'pineapple', 'mango', 'avocado', 'peach', 'pear', 'cherry'],
            'proteins': ['chicken', 'beef', 'pork', 'fish', 'salmon', 'tuna', 'shrimp', 'egg',
                        'tofu', 'cheese', 'milk', 'yogurt', 'turkey', 'ham', 'bacon'],
            'grains': ['rice', 'pasta', 'bread', 'flour', 'oats', 'quinoa', 'barley', 'wheat'],
            'herbs_spices': ['basil', 'oregano', 'thyme', 'rosemary', 'parsley', 'cilantro',
                           'mint', 'sage', 'salt', 'pepper', 'paprika', 'cumin', 'turmeric'],
            'pantry': ['oil', 'butter', 'sugar', 'honey', 'vinegar', 'soy sauce', 'olive oil']
        }
        
        # Flatten all food keywords
        self.all_food_items = []
        for category in self.food_keywords.values():
            self.all_food_items.extend(category)
    
    def _load_captioning_model(self):
        """Load the image captioning model"""
        try:
            logger.info("Loading image captioning model...")
            model_name = "nlpconnect/vit-gpt2-image-captioning"
            
            self.caption_model = VisionEncoderDecoderModel.from_pretrained(
                model_name, 
                cache_dir=self.cache_dir
            )
            self.caption_processor = ViTImageProcessor.from_pretrained(
                model_name,
                cache_dir=self.cache_dir
            )
            self.caption_tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=self.cache_dir
            )
            
            self.caption_model.to(self.device)
            self.caption_model.eval()
            
            logger.info("Image captioning model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load captioning model: {e}")
            raise e
    
    def _load_object_detection_model(self):
        """Load the object detection model"""
        try:
            logger.info("Loading object detection model...")
            model_name = "facebook/detr-resnet-50"
            
            self.detection_processor = DetrImageProcessor.from_pretrained(
                model_name,
                cache_dir=self.cache_dir
            )
            self.detection_model = DetrForObjectDetection.from_pretrained(
                model_name,
                cache_dir=self.cache_dir
            )
            
            self.detection_model.to(self.device)
            self.detection_model.eval()
            
            logger.info("Object detection model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load object detection model: {e}")
            raise e
    
    def _preprocess_image(self, image_data: bytes) -> Image.Image:
        """Preprocess image data"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return image
            
        except Exception as e:
            logger.error(f"Failed to preprocess image: {e}")
            raise e
    
    def _generate_caption(self, image: Image.Image) -> str:
        """Generate caption for the image"""
        try:
            # Process image
            pixel_values = self.caption_processor(
                images=image, 
                return_tensors="pt"
            ).pixel_values.to(self.device)
            
            # Generate caption
            with torch.no_grad():
                output_ids = self.caption_model.generate(
                    pixel_values,
                    max_length=50,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Decode caption
            caption = self.caption_tokenizer.decode(
                output_ids[0], 
                skip_special_tokens=True
            )
            
            return caption.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate caption: {e}")
            return ""
    
    def _detect_objects(self, image: Image.Image) -> List[Dict]:
        """Detect objects in the image"""
        try:
            # Process image
            inputs = self.detection_processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Detect objects
            with torch.no_grad():
                outputs = self.detection_model(**inputs)
            
            # Process results
            target_sizes = torch.tensor([image.size[::-1]]).to(self.device)
            results = self.detection_processor.post_process_object_detection(
                outputs, 
                target_sizes=target_sizes, 
                threshold=0.5
            )[0]
            
            detected_objects = []
            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                object_name = self.detection_model.config.id2label[label.item()]
                confidence = score.item()
                
                detected_objects.append({
                    "name": object_name,
                    "confidence": confidence,
                    "box": box.tolist()
                })
            
            return detected_objects
            
        except Exception as e:
            logger.error(f"Failed to detect objects: {e}")
            return []
    
    def _extract_ingredients_from_text(self, text: str) -> List[str]:
        """Extract food ingredients from text using keyword matching"""
        text_lower = text.lower()
        found_ingredients = []
        
        for ingredient in self.all_food_items:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(ingredient.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_ingredients.append(ingredient.title())
        
        return list(set(found_ingredients))  # Remove duplicates
    
    def _filter_food_objects(self, objects: List[Dict]) -> List[str]:
        """Filter detected objects to keep only food-related items"""
        food_objects = []
        
        for obj in objects:
            object_name = obj["name"].lower()
            
            # Check if the detected object is food-related
            if any(food_item in object_name for food_item in self.all_food_items):
                food_objects.append(obj["name"].title())
            
            # Also check for common food containers/items
            food_containers = ['bowl', 'plate', 'cup', 'bottle', 'jar', 'can']
            if any(container in object_name for container in food_containers):
                # Don't add the container itself, but it indicates food presence
                continue
        
        return list(set(food_objects))
    
    async def identify_ingredients(self, image_data: bytes) -> List[str]:
        """
        Main method to identify ingredients from image
        Combines image captioning and object detection
        """
        try:
            # Preprocess image
            image = self._preprocess_image(image_data)
            
            # Run both models concurrently
            caption_task = asyncio.create_task(
                asyncio.to_thread(self._generate_caption, image)
            )
            objects_task = asyncio.create_task(
                asyncio.to_thread(self._detect_objects, image)
            )
            
            # Wait for both tasks to complete
            caption, detected_objects = await asyncio.gather(caption_task, objects_task)
            
            logger.info(f"Generated caption: {caption}")
            logger.info(f"Detected {len(detected_objects)} objects")
            
            # Extract ingredients from caption
            caption_ingredients = self._extract_ingredients_from_text(caption)
            
            # Filter food objects from detection
            object_ingredients = self._filter_food_objects(detected_objects)
            
            # Combine and deduplicate ingredients
            all_ingredients = list(set(caption_ingredients + object_ingredients))
            
            logger.info(f"Identified ingredients: {all_ingredients}")
            
            return all_ingredients
            
        except Exception as e:
            logger.error(f"Failed to identify ingredients: {e}")
            raise e 