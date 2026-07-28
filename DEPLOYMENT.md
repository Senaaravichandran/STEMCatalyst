# STEM Catalyst - Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### Prerequisites
1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **API Keys**: Get your API keys ready:
   - Mistral AI API Key
   - Hugging Face Token
   - AssemblyAI API Key (for voice features)

### Deployment Process

#### Option 1: Using the Automated Script
```bash
# Run the deployment preparation script
./deploy-to-vercel.bat
```

#### Option 2: Manual Deployment

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Build Frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

3. **Deploy to Vercel**
   ```bash
   vercel
   ```
   - Follow the prompts
   - Choose "Link to existing project" or create new
   - Select "y" for build settings

4. **Set Environment Variables**
   Go to your Vercel dashboard → Project Settings → Environment Variables
   
   Add these variables:
   ```
   NVIDIA_API_KEY=your_actual_nvidia_key
   HUGGINGFACE_TOKEN=your_actual_hf_token
   ASSEMBLYAI_API_KEY=your_actual_assemblyai_key
   SECRET_KEY=your_random_secret_key
   ```

#### Option 3: Git-based Deployment

1. **Push to GitHub/GitLab**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Connect Repository in Vercel**
   - Go to Vercel dashboard
   - Click "Import Project"
   - Connect your Git repository
   - Deploy automatically

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NVIDIA_API_KEY` | NVIDIA AI API key for problem solving | Yes |
| `HUGGINGFACE_TOKEN` | Hugging Face token for AI models | No |
| `ASSEMBLYAI_API_KEY` | AssemblyAI key for voice transcription | Yes (if using voice) |
| `SECRET_KEY` | Flask secret key (generate random string) | Yes |

### Post-Deployment

1. **Test Your App**: Visit your Vercel URL
2. **Custom Domain** (optional): Add in Vercel dashboard
3. **Monitor**: Check Vercel function logs for any issues

### Troubleshooting

**Issue**: API calls failing
- **Solution**: Check environment variables are set correctly

**Issue**: CORS errors
- **Solution**: The app auto-detects Vercel domain, but check console for errors

**Issue**: Build failures
- **Solution**: Ensure all dependencies in package.json and requirements.txt

### Project Structure for Vercel

```
STEMCatalyst/
├── vercel.json          # Vercel configuration
├── frontend/            # React app (builds to /build)
├── backend/            # Flask API (becomes serverless functions)
├── .env.template       # Environment variables template
└── deploy-to-vercel.bat # Automated deployment script
```

## 🔧 Development vs Production

- **Development**: `npm start` in frontend, `python app.py` in backend
- **Production**: Deployed as static site + serverless functions on Vercel

## 📱 Features Supported in Vercel

✅ Problem solving with AI  
✅ Voice input processing  
✅ Image generation  
✅ Real-time responses  
✅ All STEM subjects  
✅ Mobile responsive  

## 🚦 Status

After deployment, your app will be available at:
- **Vercel URL**: `https://your-project-name.vercel.app`
- **Custom Domain**: (if configured)