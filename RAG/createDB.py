from data import data 
from createEmbeddings import create_embeddings
from storeEmbeddings import initialize_chromadb,store_embeddings,get_or_create_collection
from searchEmbeddings import search_embeddings

# -------------------------------- store embeddings of product details ----------------------------------------
document_list , embeddings_list , ids_list , metadata_list = create_embeddings(data.productDetails)
chroma_client = initialize_chromadb()
collection = get_or_create_collection(chroma_client,collection_name="product")
store_embeddings(collection, document_list, embeddings_list, ids_list, metadata_list)
# ---------------------------------------------------------------------------------------------------------------


# -------------------------------- store embeddings of Prompts ----------------------------------------
document_list , embeddings_list , ids_list , metadata_list = create_embeddings(data.allPrompts)
chroma_client = initialize_chromadb()
collection = get_or_create_collection(chroma_client,collection_name="prompts")
store_embeddings(collection, document_list, embeddings_list, ids_list, metadata_list)
# ---------------------------------------------------------------------------------------------------------------

