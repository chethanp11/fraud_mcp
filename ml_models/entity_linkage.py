# =============================================================== #
# ============ ml_models/entity_linkage.py ====================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Identify related entities using dummy linkage logic
# 🔗 Simulates relationships based on shared metadata
# 🎯 Output    : List of linked entity pairs or clusters
# ✅ Used by  : tools/detect_fraud.py or downstream flows
# =============================================================== #

from typing import List, Dict

# =============================================================== #
# =============== DUMMY ENTITY LINKAGE FUNCTION ================= #
# =============================================================== #

def find_linked_entities(entities: List[Dict]) -> List[List[str]]:
    """
    Simulate linkage between entities based on shared metadata
    (e.g., phone number, address, device ID).

    Args:
        entities (List[Dict]): List of entity records, each with metadata

    Returns:
        List[List[str]]: List of clusters (linked entity IDs)
    """

    clusters = []
    seen = set()

    for i, entity in enumerate(entities):
        group = [entity["entity_id"]]
        for j in range(i + 1, len(entities)):
            other = entities[j]
            # Dummy rule: shared email or phone = potential linkage
            if (
                entity.get("email") == other.get("email")
                or entity.get("phone") == other.get("phone")
            ):
                group.append(other["entity_id"])
        if len(group) > 1:
            # Avoid duplicates
            group_sorted = tuple(sorted(group))
            if group_sorted not in seen:
                clusters.append(group)
                seen.add(group_sorted)

    return clusters


# =============================================================== #
# ======================= SAMPLE USAGE ========================== #
# =============================================================== #

if __name__ == "__main__":
    test_entities = [
        {"entity_id": "A1", "email": "x@example.com", "phone": "123"},
        {"entity_id": "A2", "email": "x@example.com", "phone": "999"},
        {"entity_id": "B1", "email": "y@example.com", "phone": "123"},
        {"entity_id": "C1", "email": "z@example.com", "phone": "888"},
    ]

    linked = find_linked_entities(test_entities)
    for cluster in linked:
        print("Linked entities:", cluster)

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #