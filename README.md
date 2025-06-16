# RecipeSnap - AI Cooking Assistant from Your Fridge

RecipeSnap is an AI-powered cooking assistant that identifies ingredients from photos of your fridge and generates delicious recipes using those ingredients. Simply upload a photo, and let AI do the magic!

## 🚀 Features

- **Image Analysis**: Upload photos of your fridge or ingredients
- **AI-Powered Ingredient Detection**: Uses computer vision to identify ingredients
- **Smart Recipe Generation**: Creates personalized recipes based on available ingredients
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Real-time Processing**: Fast ingredient identification and recipe generation

## 🤖 AI Models Used

- **Image Captioning**: `nlpconnect/vit-gpt2-image-captioning`
- **Object Detection**: `facebook/detr-resnet-50`
- **Recipe Generation**: `mistralai/Mistral-7B-Instruct-v0.1`

## 🏗️ Architecture

### Backend (FastAPI + AI Models)
- FastAPI server for REST API endpoints
- Image processing service with Hugging Face Transformers
- Recipe generation using Mistral AI
- Async processing for better performance

### Frontend (React + Tailwind CSS)
- Modern React application with hooks
- Drag-and-drop image upload
- Responsive design with Tailwind CSS
- Component-based architecture

## 📋 Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- Git

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd recipeSnap
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r ../requirements.txt
```

#### Environment Configuration
```bash
# Copy the environment template
cp ../env.example .env

# Edit .env file with your settings (optional)
# HUGGINGFACE_TOKEN=your_token_here  # Optional, for faster downloads
# DEVICE=cpu  # or 'cuda' if you have GPU
```

#### Start Backend Server
```bash
python main.py
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup

#### Open New Terminal and Navigate to Project Root
```bash
cd /path/to/recipeSnap
```

#### Install Dependencies
```bash
npm install
```

#### Start Frontend Development Server
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## 🎯 Usage

1. **Upload Image**: Drag and drop or click to upload a photo of your fridge/ingredients
2. **Review Ingredients**: Check the AI-identified ingredients and add/remove as needed
3. **Get Recipes**: View AI-generated recipes based on your ingredients
4. **Cook & Enjoy**: Follow the detailed recipe instructions

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
npm test
```

## 📁 Project Structure

```
recipeSnap/
├── backend/
│   ├── main.py                 # FastAPI application
│   │   └── schemas.py          # Pydantic models
│   ├── services/
│   │   ├── image_processor.py  # Image analysis service
│   │   └── recipe_generator.py # Recipe generation service
│   └── tests/                  # Backend tests
├── src/
│   ├── components/
│   │   ├── RecipeSnap.js       # Main component
│   │   ├── ImageUpload.js      # Image upload component
│   │   ├── IngredientsList.js  # Ingredients display
│   │   ├── RecipesList.js      # Recipes display
│   │   └── LoadingSpinner.js   # Loading component
│   ├── App.js                  # React app entry
│   └── index.js                # React DOM entry
├── public/
│   └── index.html              # HTML template
├── requirements.txt            # Python dependencies
├── package.json               # Node.js dependencies
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Hugging Face API Token (optional, for faster model downloads)
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Server Configuration
PORT=8000
HOST=0.0.0.0

# Model Configuration
DEVICE=cpu  # Set to 'cuda' if you have a GPU available

# Cache Directory for Models
MODEL_CACHE_DIR=./models_cache
```

### Model Configuration

The application will automatically download and cache the required AI models on first run. This may take some time depending on your internet connection.

**Model Sizes:**
- Image Captioning Model: ~1.3GB
- Object Detection Model: ~160MB
- Recipe Generation Model: ~13GB (will use mock responses if model fails to load)

## 🚀 Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files (example with serve)
npx serve -s build -l 3000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Main Endpoints

- `POST /full-analysis` - Upload image and get ingredients + recipes
- `POST /analyze-ingredients` - Upload image and get ingredients only
- `POST /generate-recipes` - Generate recipes from ingredient list
- `GET /` - Health check

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Errors**: 
   - Ensure you have enough disk space (>15GB recommended)
   - Check internet connection for model downloads
   - Try setting `DEVICE=cpu` in environment variables

2. **Frontend Connection Issues**:
   - Ensure backend is running on port 8000
   - Check CORS settings in main.py

3. **Memory Issues**:
   - Close other applications to free up RAM
   - Consider using CPU instead of GPU if running out of memory

### Performance Tips

- Use GPU if available for faster processing
- Resize large images before upload
- Close unused browser tabs to free memory

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hugging Face for providing the AI models
- FastAPI for the excellent web framework
- React team for the frontend framework
- Tailwind CSS for the styling framework

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for home cooks everywhere!**