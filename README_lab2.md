# Lab 2: PDF RAG Chatbot

Chat with your PDF documents using RAG (Retrieval Augmented Generation).

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your PDF:
   - **Option A**: Place a PDF file named `document.pdf` in this folder
   - **Option B**: Use Google Drive:
     1. Upload PDF to Google Drive
     2. Right-click → Share → Get link → Copy file ID
     3. Update `PDF_URL` in `pdf_rag_chatbot.py` with your file ID

## Google Drive File ID

To get the file ID from a Google Drive link:
- Link format: `https://drive.google.com/file/d/FILE_ID_HERE/view`
- Extract the `FILE_ID_HERE` part
- Update in code: `PDF_URL = "https://drive.google.com/uc?export=download&id=FILE_ID_HERE"`

## Run

```bash
python pdf_rag_chatbot.py
```

## How it works

1. **Load PDF**: Uses PyPDFLoader to extract text from PDF
2. **Chunk**: Splits text into 500-character chunks with 100-char overlap
3. **Embed**: Generates embeddings using `all-MiniLM-L6-v2`
4. **Store**: Saves vectors in ChromaDB (persistent storage in `./chroma_pdf_db`)
5. **Query**: Retrieves relevant chunks and generates answers using DistilGPT2

## Features

- Persistent storage (data saved between runs)
- Interactive chat interface
- Context-aware responses
- Page metadata tracking

## Upgrade LLM

For better responses, replace `distilgpt2` with:
- `gpt2-medium` (larger but better)
- `facebook/opt-1.3b` (even better, needs more RAM)
- Or use an API-based model (OpenAI, Anthropic, etc.)
