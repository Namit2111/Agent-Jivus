from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings(documents, filename="test", doc_type="product_info"):
    """
    Creates embeddings for a list of documents (either product info or prompt templates).
    
    Args:
    - documents (list): List of documents where each document has `page_content` and `metadata`.
    - filename (str): Base filename to use for ID generation.
    - doc_type (str): Type of document, either 'product_info' or 'prompt_templates'.
    
    Returns:
    - document_list (list): List of document texts.
    - embeddings_list (list): List of embeddings for each document.
    - ids_list (list): List of IDs for each document.
    - metadata_list (list): List of metadata dictionaries for each document.
    """
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    document_list = []
    embeddings_list = []
    ids_list = []
    metadata_list = []
    
    # Loop through each document to create embeddings
    for i, doc in enumerate(documents):
        embedding = embeddings_model.embed_query(doc["page_content"])
        
        # Append document info based on type and provided filename
        document_list.append(doc["page_content"])
        embeddings_list.append(embedding)
        ids_list.append(f"{filename}_{doc_type}_{i}")  # Generate ID with type tag
        metadata_list.append(doc["metadata"])
    
    return document_list, embeddings_list, ids_list, metadata_list
