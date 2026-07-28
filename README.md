<p align="center">
  <img src="https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React" />
  <img src="https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Together.ai-Llama_3.3_70B-6366F1?style=for-the-badge&logo=meta&logoColor=white" alt="Together.ai" />
  <img src="https://img.shields.io/badge/Pollinations.ai-Image_Gen-FF6B6B?style=for-the-badge" alt="Pollinations" />
  <img src="https://img.shields.io/badge/AssemblyAI-Voice-0052CC?style=for-the-badge" alt="AssemblyAI" />
</p>

# 🚀 STEMCatalyst

> **AI-powered STEM education platform** — Solve problems, understand concepts, and learn faster with Together.ai's Llama 3.3 70B model.

**Built by [Senaaravichandran A](https://github.com/Senaaravichandran) • Flaunch Internship Program • Generative AI Intern**

---

## 📖 About

STEMCatalyst is a full-stack web application that makes STEM education accessible, interactive, and personalized. Powered by **Together.ai's Llama 3.3 70B Versatile** model, it provides expert-quality explanations, step-by-step problem solutions, and personalized study strategies across five STEM subjects.

### Why STEMCatalyst?

| Problem | Solution | Impact |
|---------|----------|--------|
| 🎯 Students struggle with STEM subjects without instant, personalized help | 💡 AI assistant with detailed explanations adapted to learning levels | 🌟 Quality STEM education accessible to everyone, 24/7 |

---

## ✨ Features

### 🧠 Problem Solver
Solve complex problems in **Physics, Chemistry, Mathematics, Biology**, and **Computer Science** with detailed step-by-step explanations. Subject-locked responses ensure focused, accurate answers.

### 🎤 Voice Input
Speak your questions naturally using **AssemblyAI-powered** voice recognition trained on 13,000+ samples. Perfect for hands-free learning.

### 💡 Concept Explainer
Get clear explanations tailored to your learning level — **Beginner, Intermediate, or Advanced**. Includes real-world examples and historical context.

### 📐 Formula Reference
Quick access to important formulas organized by subject and topic. Each formula includes variable definitions, units, and application examples.

### 📚 Study Tips
Personalized study strategies based on your **learning style** (Visual, Auditory, Reading/Writing, Kinesthetic), study goals, and specific challenges.

### 🎨 AI Image Generator & Analyzer
Generate educational diagrams, visualizations, and concept illustrations using **15+ AI models** from Pollinations.ai. Includes a Story Concept Explainer and Image Analyzer.

### 🌙 Dark Mode
Full dark mode support with smooth transitions. Persists your preference across sessions.

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| **React 18** | Modern component-based UI |
| **Tailwind CSS** | Utility-first responsive styling |
| **Lucide React** | Premium SVG icons |
| **KaTeX** | Mathematical equation rendering |
| **Axios** | HTTP client for API calls |

### Backend
| Technology | Purpose |
|-----------|---------|
| **Python Flask** | RESTful API server |
| **Flask-CORS** | Cross-origin resource sharing |
| **Gunicorn** | Production WSGI server (Render) |

### AI Services
| Service | Model | Purpose |
|---------|-------|---------|
| **Together.ai** | `llama-3.3-70b-versatile` | Problem solving, concept explanation, formulas, study tips |
| **Pollinations.ai** | Flux, DALL-E 3, SDXL, + 12 more | AI image generation (free, no API key needed) |
| **AssemblyAI** | Universal-2 | Speech-to-text voice input |

### Data
- **Math problem datasets** (JSONL format) for training & search
- **ScienceQA dataset** for science questions
- **Text-to-speech training data** (13,100 samples) for voice enhancement

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.8+
- **Node.js** 16+
- **npm** or **yarn**
- **Together.ai API Key** — [Get one free at api.together.ai](https://api.together.ai/)
- **AssemblyAI API Key** — [Get one free at assemblyai.com](https://www.assemblyai.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Senaaravichandran/STEMCatalyst.git
   cd STEMCatalyst
   ```

2. **Set up environment variables**
   
   Create a `.env` file in the `backend/` folder:
   ```env
   # Together.ai API Key (Llama 3.3 70B)
   # Get it from: https://api.together.ai/
   GROQ_API_KEY=your_together_ai_api_key_here

   # AssemblyAI (voice-to-text)
   ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

   # Flask settings
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your-secret-key-here
   PORT=5000
   HOST=0.0.0.0
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

### Running Locally

**Terminal 1 — Start Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 — Start Frontend:**
```bash
cd frontend
npm start
```

Open **http://localhost:3000** in your browser 🎉

---

## 🌐 Deploy to Render

STEMCatalyst is configured for **one-click deployment** on [Render](https://render.com).

### Backend (Flask API)

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo: `Senaaravichandran/STEMCatalyst`
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
4. Add **Environment Variables**:
   | Key | Value |
   |-----|-------|
   | `GROQ_API_KEY` | Your Together.ai API key (obtained from https://api.together.ai/) |
   | `ASSEMBLYAI_API_KEY` | Your AssemblyAI key |
   | `SECRET_KEY` | Any random strong string |
   | `FLASK_DEBUG` | `False` |
5. Click **Create Web Service** — your API will be live at `https://your-app.onrender.com`

### Frontend (React)

1. Go to **New → Static Site**
2. Connect the same repo
3. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
4. Add **Environment Variable**:
   | Key | Value |
   |-----|-------|
   | `REACT_APP_API_URL` | `https://your-backend.onrender.com` |
5. Click **Create Static Site**

---

## 📁 Project Structure

```
STEMCatalyst/
├── backend/                    # Flask API server
│   ├── api/
│   │   └── routes.py           # All API route handlers
│   ├── services/
│   │   ├── ai_service.py       # AI orchestration layer
│   │   ├── groq_service.py     # Together.ai (Llama 3.3 70B) integration
│   │   ├── pollinations_image_service.py
│   │   ├── voice_service.py    # AssemblyAI voice processing
│   │   ├── data_service.py     # Dataset management
│   │   └── fallback_service.py # Offline fallback content
│   ├── app.py                  # Flask application factory
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables (not committed)
│
├── frontend/                   # React application
│   ├── public/                 # Static assets & index.html
│   └── src/
│       ├── components/         # Reusable UI components
│       │   ├── SolutionRenderer.js
│       │   ├── ImageGenerator.js
│       │   ├── VoiceInput.js
│       │   ├── Button.js
│       │   └── Card.js
│       ├── views/              # Page components
│       │   ├── HomeView.js     # Landing page
│       │   ├── ProblemSolverView.js
│       │   ├── VoiceView.js
│       │   ├── ConceptExplainerView.js
│       │   ├── FormulaReferenceView.js
│       │   └── StudyTipsView.js
│       ├── navigation/         # Sidebar navigation
│       ├── services/api.js     # Axios API client
│       ├── App.js              # Main app with dark mode
│       └── index.css           # Global styles & design system
│
├── data/                       # Training & reference datasets
│   ├── maths/                  # Math problem datasets (JSONL)
│   ├── science/                # ScienceQA dataset
│   └── text2speech/            # Voice training data (13K+ samples)
│
├── render.yaml                 # Render deployment configuration
├── .env.template               # Environment variable template
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check with service status |
| `/api/solve` | POST | Solve a STEM problem |
| `/api/explain` | POST | Explain a concept |
| `/api/formulas` | POST | Get formulas by subject/topic |
| `/api/study-tips` | POST | Get personalized study tips |
| `/api/generate-image` | POST | Generate educational images |
| `/api/analyze-image` | POST | Analyze uploaded images |
| `/api/voice-search` | POST | Search voice training data |
| `/api/voice-training-stats` | GET | Voice dataset statistics |
| `/api/datasets` | GET | Available datasets |
| `/api/search-problems` | POST | Search math/science problems |

---

## 🎯 Future Enhancements

- [ ] User accounts and progress tracking
- [ ] Practice problem generator with difficulty scaling
- [ ] Collaborative study rooms
- [ ] Mobile application (React Native)
- [ ] Multi-language support
- [ ] Spaced repetition flashcard system

---

## 👨‍💻 Author

**Senaaravichandran A**

Built as part of the **Flaunch Internship Program** as a **Generative AI Intern**

- 🐙 GitHub: [@Senaaravichandran](https://github.com/Senaaravichandran)
- 💼 LinkedIn: [Senaaravichandran](https://www.linkedin.com/in/senaa2407)

---

## 🙏 Acknowledgments

- **[Together.ai](https://together.ai)** — Llama 3.3 70B Versatile model for AI-powered problem solving
- **[Pollinations.ai](https://pollinations.ai)** — Free AI image generation with 15+ models
- **[AssemblyAI](https://www.assemblyai.com)** — Speech-to-text voice recognition
- **[Flaunch](https://flaunch.in)** — For the internship opportunity

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <b>STEMCatalyst</b> — Making STEM education accessible to everyone 🌟
  <br/>
  <sub>Powered by Together.ai • Llama 3.3 70B Versatile</sub>
</p>
