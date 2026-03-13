# Quick Deploy Instructions

## Your Frontend is Already Deployed! 🎉

Your React app is live on Cloudflare Pages (check the terminal output for the URL).

## Deploy Backend in 5 Minutes:

### Option 1: Render (Recommended - Free)

1. Go to https://render.com and sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect repository: `abhishekbiradar07/build_simple_RAG`
4. Configure:
   - **Name**: `pdf-rag-backend`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend_api:app`
   - **Instance Type**: Free
5. Click "Create Web Service"
6. Wait 10-15 minutes for deployment
7. Copy your backend URL (e.g., `https://pdf-rag-backend.onrender.com`)

### Update Frontend with Backend URL:

Once backend is deployed, update your Cloudflare Pages environment variable:

```bash
wrangler pages deployment create pdf-rag-chatbot --branch=main
```

Or in Cloudflare Dashboard:
1. Go to Pages → pdf-rag-chatbot → Settings → Environment Variables
2. Add: `REACT_APP_API_URL` = `https://your-backend-url.onrender.com/api`
3. Redeploy

### Option 2: Railway (Also Free)

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Railway auto-detects Python and deploys
5. Copy the URL and update frontend

### Option 3: Use Local Backend (Quick Test)

1. Keep backend running locally: `python backend_api.py`
2. Download ngrok: https://ngrok.com/download
3. Sign up and get auth token
4. Run: `ngrok http 5000`
5. Copy the https URL
6. Update frontend environment variable

## Current Status:

✅ Frontend: Deployed on Cloudflare Pages
⏳ Backend: Needs deployment (choose option above)

## Test Your App:

Once backend is deployed, visit your Cloudflare Pages URL and:
1. Upload a PDF
2. Ask questions
3. Get AI-powered answers!
