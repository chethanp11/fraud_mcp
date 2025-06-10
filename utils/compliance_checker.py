# =============================================================== #
# =============== utils/compliance_checker.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Verify user instruction/tool against compliance SOPs
# 📚 Grounding : Vector DB (Qdrant) via LlamaIndex
# ✅ Used by   : planner_agent, decision_agent, flows, tools
# =============================================================== #

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os

# =============================================================== #
# ==================== CONFIGURATION SECTION ==================== #
# =============================================================== #
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "compliance_sops")

# Set a similarity threshold
COMPLIANCE_THRESHOLD = 0.75  # Can be adjusted

# =============================================================== #
# ================== QDRANT CLIENT + INDEX SETUP ================ #
# =============================================================== #
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
vector_store = QdrantVectorStore(client=client, collection_name=QDRANT_COLLECTION)

index = VectorStoreIndex.from_vector_store(vector_store)

# =============================================================== #
# ============== COMPLIANCE MATCHING FUNCTION =================== #
# =============================================================== #
def is_action_compliant(user_input: str) -> tuple[bool, str]:
    """
    Check whether the given user input is compliant with SOPs.

    Args:
        user_input (str): Natural language instruction or task

    Returns:
        tuple: (is_compliant (bool), reason_or_source (str))
    """
    # Perform semantic search
    query_engine = index.as_query_engine(similarity_top_k=1)
    response = query_engine.query(user_input)

    # Parse match and similarity
    if hasattr(response, "source_nodes") and response.source_nodes:
        node = response.source_nodes[0]
        similarity = node.score if hasattr(node, "score") else 0.0
        source = node.text if hasattr(node, "text") else "Unknown source"

        # Debug print (can be logged)
        # print(f"Matched with score: {similarity:.2f}")

        if similarity >= COMPLIANCE_THRESHOLD:
            return True, f"Matched SOP: {source}"
        else:
            return False, "No compliant SOP match found"

    return False, "No relevant SOP found in vector store"

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #