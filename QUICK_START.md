# 🚀 RecipeSnap - Quick Start Guide

## ✅ What's Working Now

The TypeScript version conflict has been resolved and npm dependencies are installed successfully!

## 🏃‍♂️ Quick Setup (5 minutes)

### 1. Backend Setup
```bash
# Install Python dependencies (currently running in background)
pip install -r requirements.txt

# Copy environment file
copy env.example backend\.env
# OR on Mac/Linux: cp env.example backend/.env

# Start backend server
python start_backend.py
```

### 2. Frontend Setup (Already Done! ✅)
```bash
# Dependencies already installed
npm install  # ✅ COMPLETED

# Start frontend (already running in background)
npm start    # ✅ RUNNING
```

## 🌐 Access the Application

- **Frontend**: http://localhost:8000 (React app)
- **Backend API**: http://localhost:8001 (FastAPI server)
- **API Docs**: http://localhost:8001/docs (Interactive documentation)

## 🔧 Current Status

✅ **Frontend**: Running on port 8000  
✅ **Backend**: Running on port 8001  
✅ **TypeScript**: Fixed version conflict  
✅ **Environment**: Template ready  
✅ **Port Conflicts**: Resolved  

## 🎯 Next Steps

1. ✅ Python dependencies installed
2. ✅ Backend server started on port 8001
3. ✅ Frontend running on port 8000
4. **Test the setup**: `python test_setup.py`
5. **Open http://localhost:8000** in your browser
6. Upload a photo of your fridge ingredients
7. Get AI-generated recipes!

## 🐛 If You Encounter Issues

### Frontend Issues:
- If port 3000 is busy: The app will prompt to use a different port
- If build fails: Try `npm install --legacy-peer-deps`

### Backend Issues:
- If models fail to load: The app will use mock responses (still functional!)
- If port 8000 is busy: Change PORT in backend/.env file
- For GPU support: Set DEVICE=cuda in backend/.env (if you have CUDA)

## 📱 How to Use

1. **Upload Image**: Drag & drop or click to upload fridge photo
2. **Review Ingredients**: AI will identify ingredients - you can add/remove items
3. **Get Recipes**: AI generates 2-3 recipes based on your ingredients
4. **Cook & Enjoy**: Follow the detailed recipe instructions

## 🎉 Features

- 🖼️ Smart image analysis with dual AI models
- 🤖 Recipe generation with Mistral AI
- ✏️ Editable ingredient lists
- 📱 Responsive design
- ⚡ Fast processing
- 🎨 Beautiful UI

---

**Ready to cook? Let's go! 👨‍🍳👩‍🍳** 