import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from utils import clean_text, chunk_text

DATA_FILE = "club_data.txt"
INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "chunks.pkl"
EMBEDDINGS_FILE = "embeddings.npy"

def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_faiss_index(index, path):
    faiss.write_index(index, path)

def build():
    print("🔹 Loading document...")
    text = load_document(DATA_FILE)
    print("\n===== DEBUG: Document Loaded =====")
    print("TEXT LENGTH:", len(text))
    print("TEXT PREVIEW:", text[:300])
    print("=================================\n")

    print("🔹 Cleaning text...")
    cleaned = clean_text(text)

    print("🔹 Chunking text...")
    chunks = chunk_text(cleaned, chunk_size=180, overlap=40)
    print(f"Total chunks created: {len(chunks)}")
    print("Chunks Created:", len(chunks))
    if len(chunks) > 0:
       print("First Chunk Preview:", chunks[0][:200])
    else:
       print("NO CHUNKS — TEXT NOT READ")


    print("🔹 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔹 Creating embeddings...")
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

    print("🔹 Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print("🔹 Saving index & metadata...")
    save_faiss_index(index, INDEX_FILE)

    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    np.save(EMBEDDINGS_FILE, embeddings)

    print("✅ Indexing complete!")
    print("Files created:")
    print(f"- {INDEX_FILE}")
    print(f"- {CHUNKS_FILE}")
    print(f"- {EMBEDDINGS_FILE}")

if __name__ == "__main__":
    build()
