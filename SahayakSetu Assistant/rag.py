from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load text data
with open("data.txt", "r") as f:
    texts = f.read().split("\n\n")

# Create vector store
vectorstore = FAISS.from_texts(texts, embeddings)

# Create retriever
retriever = vectorstore.as_retriever()

def get_context(query):
    docs = retriever.get_relevant_documents(query)
    return "\n".join([doc.page_content for doc in docs])