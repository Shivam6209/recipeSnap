"""
Tests for Image Processing Service
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import io

from services.image_processor import ImageProcessor

class TestImageProcessor:
    """Test cases for ImageProcessor"""
    
    @pytest.fixture
    def mock_image_processor(self):
        """Create a mock image processor for testing"""
        with patch('services.image_processor.torch'), \
             patch('services.image_processor.VisionEncoderDecoderModel'), \
             patch('services.image_processor.ViTImageProcessor'), \
             patch('services.image_processor.AutoTokenizer'), \
             patch('services.image_processor.DetrImageProcessor'), \
             patch('services.image_processor.DetrForObjectDetection'):
            processor = ImageProcessor()
            return processor
    
    def test_init(self, mock_image_processor):
        """Test ImageProcessor initialization"""
        assert mock_image_processor is not None
        assert hasattr(mock_image_processor, 'device')
        assert hasattr(mock_image_processor, 'food_keywords')
        assert hasattr(mock_image_processor, 'all_food_items')
    
    def test_extract_ingredients_from_text(self, mock_image_processor):
        """Test ingredient extraction from text"""
        test_text = "I see tomatoes, onions, and chicken in the image"
        
        ingredients = mock_image_processor._extract_ingredients_from_text(test_text)
        
        assert 'Tomato' in ingredients
        assert 'Onion' in ingredients
        assert 'Chicken' in ingredients 