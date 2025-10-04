@echo off
REM BioWhisper Quick Setup Script for Windows
REM Run: setup.bat

echo ========================================
echo 🎯 BioWhisper Setup Script (Windows)
echo ========================================
echo.

REM Check prerequisites
echo 1️⃣  Checking prerequisites...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+
    exit /b 1
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 18+
    exit /b 1
)

python --version
node --version
echo.

REM Backend setup
echo 2️⃣  Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo    Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo    Activating virtual environment...
call venv\Scripts\activate.bat

echo    Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo    Creating .env file from example...
    copy .env.example .env
    echo    ⚠️  Please edit backend\.env and add your API keys
)

REM Create uploads directory
if not exist "uploads" mkdir uploads

echo ✅ Backend setup complete
echo.

cd ..

REM Frontend setup
echo 3️⃣  Setting up frontend...
cd frontend

echo    Installing Node dependencies...
call npm install

REM Create .env if it doesn't exist
if not exist ".env" (
    echo    Creating .env file from example...
    copy .env.example .env
)

echo ✅ Frontend setup complete
echo.

cd ..

REM Final instructions
echo ========================================
echo 🎉 Setup Complete!
echo.
echo 📝 Next Steps:
echo.
echo 1. Configure API keys in backend\.env:
echo    - GEMINI_API_KEY (get from https://makersuite.google.com/app/apikey)
echo    - ELEVENLABS_API_KEY (get from https://elevenlabs.io/)
echo.
echo 2. Start the backend:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python app.py
echo.
echo 3. In a new terminal, start the frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:3000 in your browser
echo.
echo 📚 Documentation:
echo    - README.md: Full documentation
echo    - DEMO_INSTRUCTIONS.md: Demo guide
echo    - API docs: http://localhost:8000/docs
echo.
echo ========================================

pause
