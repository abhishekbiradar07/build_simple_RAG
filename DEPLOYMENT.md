# Deployment Guide

## Architecture

This app requires two separate deployments:
1. **Frontend** (React) → Vercel
2. **Backend** (Flask + ML models) → Render/Railway/Heroku

## Option 1: Deploy Frontend to Vercel + Backend to Render (Recommended)

### Step 1: Deploy Backend to Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `abhishekbiradar07/build_simple_RAG`
4. Configure:
   - **Name**: `pdf-rag-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend_api:app`
   - **Instance Type**: Free (or paid for better performance)
5. Add environment variable:
   - `PYTHON_VERSION`: `3.11.0`
6. Click "Create Web Service"
7. Wait for deployment (10-15 mins for model downloads)
8. Copy your backend URL (e.g., `https://pdf-rag-backend.onrender.com`)

### Step 2: Deploy Frontend to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy from root directory:
```bash
vercel
```

4. During setup:
   - Set up and deploy? **Y**
   - Which scope? Choose your account
   - Link to existing project? **N**
   - Project name? `pdf-rag-frontend`
   - In which directory is your code? `./frontend`
   - Override settings? **Y**
   - Build Command? `npm run build`
   - Output Directory? `build`
   - Development Command? `npm start`

5. Set environment variable:
```bash
vercel env add REACT_APP_API_URL
```
Enter your Render backend URL: `https://pdf-rag-backend.onrender.com/api`

6. Redeploy with env variable:
```bash
vercel --prod
```

## Option 2: Deploy Everything to Render

1. Deploy as a monorepo on Render
2. Use Render's static site for frontend
3. Use Render's web service for backend

## Option 3: Local Backend + Vercel Frontend

If you want to keep backend running locally:

1. Deploy only frontend to Vercel
2. Use ngrok to expose local backend:
```bash
ngrok http 5000
```
3. Set `REACT_APP_API_URL` to your ngrok URL

## Backend Requirements for Production

Add to `requirements.txt`:
```
gunicorn
```

Create `Procfile` for Heroku/Render:
```
web: gunicorn backend_api:app
```

## Important Notes

- **Vercel Limitations**: Cannot run heavy ML models in serverless functions (50MB limit, 10s timeout)
- **Render Free Tier**: Spins down after inactivity, first request takes 30-60s
- **Model Size**: sentence-transformers + distilgpt2 = ~500MB, needs persistent server
- **CORS**: Already configured in `backend_api.py` with `flask-cors`

## Testing Deployment

1. Visit your Vercel URL
2. Upload a PDF
3. Ask questions
4. Check browser console for any CORS or API errors

## Troubleshooting

- **CORS errors**: Ensure backend URL is correct in environment variables
- **Slow responses**: Upgrade Render instance or use better LLM API
- **Model loading fails**: Increase Render instance memory
- **Build fails**: Check Node.js version compatibility
