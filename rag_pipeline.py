import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Load the embedding model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Read sample documents
with open('sample_docs.txt', 'r') as f:
    text = f.read()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
chunks = text_splitter.split_text(text)

print(f"Split document into {len(chunks)} chunks\n")

# Initialize ChromaDB
client = chromadb.Client()
collection = client.create_collection(name="docs")

# Generate embeddings and add to ChromaDB
for i, chunk in enumerate(chunks):
    embedding = embedding_model.encode(chunk).tolist()
    collection.add(
        embeddings=[embedding],
        documents=[chunk],
        ids=[f"chunk_{i}"]
    )

print("Documents indexed in ChromaDB\n")

# RAG Query Function
def query_rag(question, n_results=2):
    # Embed the question
    question_embedding = embedding_model.encode(question).tolist()
    
    # Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    
    # Display results
    print(f"Question: {question}\n")
    print("Retrieved Context:")
    print("-" * 50)
    for i, doc in enumerate(results['documents'][0], 1):
        print(f"{i}. {doc}\n")
    
    return results['documents'][0]

# Example queries
if __name__ == "__main__":
    query_rag("What is RAG?")
    print("\n" + "="*50 + "\n")
    query_rag("How does deep learning work?")
