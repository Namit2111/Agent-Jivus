from langchain_huggingface import HuggingFaceEmbeddings

def search_embeddings(collection, query):
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    query_embedding = embeddings_model.embed_query(query)
    results = collection.query(query_embeddings=query_embedding, n_results=1,include=["documents","distances","metadatas"])
    return results
