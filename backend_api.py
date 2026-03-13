from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Global variables
embedding_model = None
llm = None
collection = None
pdf_loaded = False

print("Initializing models...")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
llm = pipeline("text-generation", model="distilgpt2", max_new_tokens=150, device=-1)
print("Models loaded!")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "pdf_loaded": pdf_loaded})

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    global collection, pdf_loaded
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files allowed"}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load and chunk PDF
        loader = PyPDFLoader(filepath)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create ChromaDB collection
        client = chromadb.PersistentClient(path="./chroma_pdf_db")
        try:
            client.delete_collection(name="pdf_docs")
        except:
            pass
        
        collection = client.create_collection(name="pdf_docs")
        
        # Add chunks
        for i, chunk in enumerate(chunks):
            text = chunk.page_content
            embedding = embedding_model.encode(text).tolist()
            collection.add(
                embeddings=[embedding],
                documents=[text],
                metadatas=[{"page": chunk.metadata.get("page", 0)}],
                ids=[f"chunk_{i}"]
            )
        
        pdf_loaded = True
        
        return jsonify({
            "message": "PDF processed successfully",
            "pages": len(documents),
            "chunks": len(chunks),
            "filename": filename
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query():
    global collection, pdf_loaded
    
    if not pdf_loaded:
        return jsonify({"error": "Please upload a PDF first"}), 400
    
    data = request.json
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    try:
        # Embed question
        question_embedding = embedding_model.encode(question).tolist()
        
        # Retrieve relevant chunks
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3
        )
        
        # Combine context
        context = "\n\n".join(results['documents'][0])
        
        # Create prompt
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
        
        # Generate answer
        response = llm(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)
        answer = response[0]['generated_text'][len(prompt):].strip()
        
        return jsonify({
            "answer": answer,
            "context": results['documents'][0],
            "pages": [m.get('page', 0) for m in results['metadatas'][0]]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
