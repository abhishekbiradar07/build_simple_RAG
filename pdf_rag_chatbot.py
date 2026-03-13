import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import os

# Configuration
PDF_URL = "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID"  # Replace with your Google Drive file ID
PDF_PATH = "document.pdf"

print("Initializing models...")
# Load embedding model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load LLM for generation (using a small open model)
llm = pipeline(
    "text-generation",
    model="distilgpt2",  # Small open model, replace with larger if needed
    max_new_tokens=150,
    device=-1  # Use CPU, change to 0 for GPU
)

print("Models loaded!\n")

# Step 1: Download PDF from Google Drive (or use local file)
def download_pdf(url, save_path):
    """Download PDF from Google Drive"""
    import urllib.request
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"PDF downloaded to {save_path}\n")
    except Exception as e:
        print(f"Error downloading: {e}")
        print("Using local PDF if available...\n")

# Step 2: Load and chunk PDF
def load_and_chunk_pdf(pdf_path):
    """Load PDF and split into chunks"""
    print(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    print(f"Loaded {len(documents)} pages\n")
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    
    print(f"Split into {len(chunks)} chunks\n")
    return chunks

# Step 3: Create ChromaDB collection and add embeddings
def create_vector_db(chunks):
    """Create ChromaDB collection with embeddings"""
    print("Creating vector database...")
    
    # Use persistent storage
    client = chromadb.PersistentClient(path="./chroma_pdf_db")
    
    # Delete existing collection if it exists
    try:
        client.delete_collection(name="pdf_docs")
    except:
        pass
    
    collection = client.create_collection(name="pdf_docs")
    
    # Add chunks with embeddings
    for i, chunk in enumerate(chunks):
        text = chunk.page_content
        embedding = embedding_model.encode(text).tolist()
        
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"page": chunk.metadata.get("page", 0)}],
            ids=[f"chunk_{i}"]
        )
    
    print(f"Added {len(chunks)} chunks to ChromaDB\n")
    return collection

# Step 4: RAG Query Function
def rag_query(collection, question, n_results=3):
    """Retrieve relevant context and generate answer"""
    # Embed question
    question_embedding = embedding_model.encode(question).tolist()
    
    # Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
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
    
    return answer, results['documents'][0]

# Step 5: Chat loop
def chat_with_pdf(collection):
    """Interactive chat with PDF"""
    print("="*60)
    print("PDF RAG Chatbot - Type 'quit' to exit")
    print("="*60 + "\n")
    
    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        print("\nThinking...\n")
        answer, context_chunks = rag_query(collection, question)
        
        print(f"Bot: {answer}\n")
        print(f"(Retrieved {len(context_chunks)} relevant chunks)")
        print("-"*60 + "\n")

# Main execution
if __name__ == "__main__":
    # Option 1: Download from Google Drive (uncomment and add your file ID)
    # download_pdf(PDF_URL, PDF_PATH)
    
    # Option 2: Use local PDF (place your PDF in the same folder)
    if not os.path.exists(PDF_PATH):
        print(f"Please place a PDF file named '{PDF_PATH}' in this folder")
        print("Or update PDF_URL with your Google Drive file ID\n")
        exit(1)
    
    # Load and process PDF
    chunks = load_and_chunk_pdf(PDF_PATH)
    
    # Create vector database
    collection = create_vector_db(chunks)
    
    # Start chat
    chat_with_pdf(collection)
