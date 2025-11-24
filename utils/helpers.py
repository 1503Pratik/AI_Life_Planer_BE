from bson import ObjectId

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format."""
    if not doc:
        return None

    doc["_id"] = str(doc["_id"])

    # Convert ObjectId fields inside nested keys (if any)
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)

    return doc


def serialize_list(docs):
    """Convert list of MongoDB docs to JSON serializable list."""
    return [serialize_doc(doc) for doc in docs]
