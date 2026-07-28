@echo off
echo ================================
echo STEM Catalyst - Vercel Deployment
echo ================================

echo.
echo [1/4] Installing Vercel CLI...
npm install -g vercel

echo.
echo [2/4] Building frontend...
cd frontend
call npm install
call npm run build
cd ..

echo.
echo [3/4] Setting up backend dependencies...
pip install -r backend/requirements.txt

echo.
echo [4/4] Ready for deployment!
echo.
echo Next steps:
echo 1. Run: vercel
echo 2. Follow the prompts to deploy
echo 3. Set up environment variables in Vercel dashboard
echo.
echo Environment variables to set in Vercel:
echo - NVIDIA_API_KEY
echo - HUGGINGFACE_TOKEN  
echo - ASSEMBLYAI_API_KEY
echo - SECRET_KEY
echo.
pause