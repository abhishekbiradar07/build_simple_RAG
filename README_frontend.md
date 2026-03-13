# PDF RAG Chatbot with React Frontend

Full-stack PDF chatbot with React frontend and Flask backend.

## Setup

### Backend

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask API:
```bash
python backend_api.py
```

Backend runs on `http://localhost:5000`

### Frontend

1. Navigate to frontend folder:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start React app:
```bash
npm start
```

Frontend runs on `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Click "Choose PDF file" and select a PDF
3. Click "Upload & Process" (wait for processing)
4. Start asking questions about your PDF!

## Features

- Drag & drop PDF upload
- Real-time chat interface
- Shows source pages for answers
- Persistent vector storage
- Beautiful gradient UI

## Architecture

- **Frontend**: React with Axios for API calls
- **Backend**: Flask REST API
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector DB**: ChromaDB (persistent)
- **LLM**: DistilGPT2 (can be upgraded)

## API Endpoints

- `GET /api/health` - Check server status
- `POST /api/upload` - Upload and process PDF
- `POST /api/query` - Ask questions about PDF
