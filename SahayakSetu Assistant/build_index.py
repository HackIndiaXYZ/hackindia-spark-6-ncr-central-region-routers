import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ✅ embeddings (local only)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Load structured data
with open("firecrawl_data.json", "r") as f:
    documents = json.load(f)

# 🔥 USE ONLY TEXT FIELD (IMPORTANT)
texts = [doc["text"] for doc in documents]

print(f"Total documents: {len(texts)}")

# 🔥 Create FAISS index
vectorstore = FAISS.from_texts(texts, embeddings)

# 🔥 Save index
vectorstore.save_local("faiss_index")

print("✅ FAISS index saved")