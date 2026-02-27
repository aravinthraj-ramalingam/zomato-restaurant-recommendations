# Zomato AI Restaurant Recommendation Service 🍕🤖

A premium, AI-powered restaurant recommendation engine that leverages human-like reasoning to find your perfect meal. Built using FastAPI for the backend and a modern glassmorphism UI for the frontend.

## ✨ Features

- **Dynamic Search**: Filter restaurants by location, cuisine, price, and rating.
- **Smart Logic**: Dependent dropdowns that refresh available options based on your selected location.
- **Chef's AI Rationale**: Integrated with **Google Gemini LLM** to provide personalized, human-like reasons for why certain restaurants match your taste.
- **Deduplicated Results**: Ensures you see a diverse range of unique restaurants, not just multiple branches of the same chain.
- **Optimized Performance**: Custom-optimized SQLite database (reduced from 578MB to 31MB) designed for high performance in serverless environments.
- **Glassmorphism UI**: A sleek, modern user interface with smooth animations and responsive design.

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML5, CSS3 (Custom Glassmorphism), JavaScript (ES6+).
- **Backend**: FastAPI (Python), Uvicorn.
- **AI Engine**: Google Gemini Pro API (via `google-genai` SDK).
- **Database**: SQLite (Optimised Data Pipeline).
- **Deployment**: Vercel (Serverless Functions).

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aravinthraj-ramalingam/zomato-restaurant-recommendations.git
   cd zomato-restaurant-recommendations
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**:
   ```bash
   python run.py
   ```
   Open `http://localhost:8080` in your browser.

### Deployment to Vercel

1. Install Vercel CLI: `npm i -g vercel`.
2. Run `vercel` in the project root.
3. Add `GEMINI_API_KEY` to your Vercel Project Environment Variables.

## 📁 Project Structure

```text
├── api/
│   ├── index.py           # Vercel Serverless Entry Point
│   ├── db_service.py      # SQLite Query Engine
│   ├── ai_service.py      # Gemini LLM Integration
│   └── zomato.db          # Optimized Database (31MB)
├── index.html             # Frontend UI
├── index.css              # Styling & Animations
├── app.js                 # API Integration & UI Logic
├── vercel.json            # Vercel Configuration
└── requirements.txt       # Python Dependencies
```

## 📊 Data Source

The dataset used in this project is sourced from [Hugging Face: Zomato Restaurant Recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation).

---
Developed with ❤️ by [aravinthraj-ramalingam](https://github.com/aravinthraj-ramalingam)
