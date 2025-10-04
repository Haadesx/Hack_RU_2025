#!/bin/bash

# BioWhisper Quick Setup Script
# Run: bash setup.sh

set -e  # Exit on error

echo "🎯 BioWhisper Setup Script"
echo "=========================="
echo ""

# Check prerequisites
echo "1️⃣  Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

echo "✅ Python $(python3 --version)"
echo "✅ Node $(node --version)"
echo ""

# Backend setup
echo "2️⃣  Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "   Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "   Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "   Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "   Creating .env file from example..."
    cp .env.example .env
    echo "   ⚠️  Please edit backend/.env and add your API keys"
fi

# Create uploads directory
mkdir -p uploads

echo "✅ Backend setup complete"
echo ""

cd ..

# Frontend setup
echo "3️⃣  Setting up frontend..."
cd frontend

# Install dependencies
echo "   Installing Node dependencies..."
npm install

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "   Creating .env file from example..."
    cp .env.example .env
fi

echo "✅ Frontend setup complete"
echo ""

cd ..

# Final instructions
echo "=========================="
echo "🎉 Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Configure API keys in backend/.env:"
echo "   - GEMINI_API_KEY (get from https://makersuite.google.com/app/apikey)"
echo "   - ELEVENLABS_API_KEY (get from https://elevenlabs.io/)"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 Documentation:"
echo "   - README.md: Full documentation"
echo "   - DEMO_INSTRUCTIONS.md: Demo guide"
echo "   - API docs: http://localhost:8000/docs"
echo ""
echo "=========================="
