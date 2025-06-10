# =============================================================== #
# =========== resources/vector_store/fraud_patterns.py ========== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Interface with Qdrant to store and search fraud patterns
# 🧠 Backend   : LlamaIndex + Qdrant Vector Store
# ✅ Used by   : flows, tools for similarity checks
# =============================================================== #

from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from qdrant_client import QdrantClient
import os

# =============================================================== #
# ======================== CONFIG & INIT ======================== #
# =============================================================== #

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "fraud_patterns"

qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
vector_store = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_NAME)
embed_model = OpenAIEmbedding(model="text-embedding-3-small")  # or gte embedding
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# =============================================================== #
# ==================== INDEXING NEW DOCUMENTS =================== #
# =============================================================== #

def index_fraud_docs(doc_folder: str):
    """
    Index fraud-related documents from a folder into Qdrant.

    Args:
        doc_folder (str): Path to directory with fraud pattern files
    """
    docs = SimpleDirectoryReader(doc_folder).load_data()
    index = VectorStoreIndex.from_documents(
        docs,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    index.storage_context.persist(persist_dir=".qdrant_index")

# =============================================================== #
# ====================== QUERY SIMILARITY ======================= #
# =============================================================== #

def search_similar_patterns(query: str, top_k: int = 3):
    """
    Search indexed fraud patterns similar to a query.

    Args:
        query (str): Natural language or pattern query
        top_k (int): Number of top results to return

    Returns:
        list[str]: Matching document chunks
    """
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)
    query_engine = index.as_query_engine()
    results = query_engine.query(query)
    return results.response

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #