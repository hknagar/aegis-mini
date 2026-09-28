import chromadb

from app.services.embedding_service import create_embedding


client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="aegis_knowledge"
)


def add_document(
    document_id: str,
    text: str,
    source: str
):


    embedding = create_embedding(text)

    collection.add(
        ids=[document_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[
            {
                "source": source
            }
        ]
    )

def search_documents(
    query: str,
    n_results: int = 3
):

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results

# the previous code below
# import chromadb


# client = chromadb.PersistentClient(
#     path="chroma_db"
# )

# collection = client.get_or_create_collection(
#     name="aegis_knowledge"
# )