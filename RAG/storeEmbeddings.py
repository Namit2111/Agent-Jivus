import chromadb
from chromadb.config import Settings
import uuid
def initialize_chromadb():
    """Initialize the ChromaDB client."""
    # settings = Settings()  # Ensure only valid fields are passed
    # chroma_client = chromadb.Client(settings)
    client = chromadb.PersistentClient(path="./db")
    return client

def get_or_create_collection(chroma_client, collection_name="document_embeddings"):
    """Get or create a collection in ChromaDB."""
    # if collection_name not in chroma_client.list_collections():
    #     collection = chroma_client.create_collection(collection_name)
    # else:
    #     collection = chroma_client.get_collection(collection_name)
    collection = chroma_client.get_or_create_collection(
        name=collection_name
    )
    return collection

def store_embeddings(collection, document_list,embeddings_list,ids_list,metadata_list):
    """Store the document embeddings in ChromaDB."""
    collection.add(
        ids=ids_list,
        documents=document_list,
        embeddings=embeddings_list,
        metadatas=metadata_list
    )


if __name__ == "__main__":
    chroma_client = initialize_chromadb()