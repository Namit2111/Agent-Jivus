from createEmbeddings import create_embeddings
from storeEmbeddings import initialize_chromadb,store_embeddings,get_or_create_collection
from searchEmbeddings import search_embeddings
from loadData import load_data_from_json
# -------------------------------- store embeddings of product details ----------------------------------------
document_list , embeddings_list , ids_list , metadata_list = create_embeddings(load_data_from_json(file_path="./data/productDetails.json"))
chroma_client = initialize_chromadb()
collection = get_or_create_collection(chroma_client,collection_name="product")
store_embeddings(collection, document_list, embeddings_list, ids_list, metadata_list)
# ---------------------------------------------------------------------------------------------------------------


# -------------------------------- store embeddings of Prompts ----------------------------------------
document_list , embeddings_list , ids_list , metadata_list = create_embeddings(load_data_from_json(file_path="./data/convoDetails.json"))
chroma_client = initialize_chromadb()
collection = get_or_create_collection(chroma_client,collection_name="prompts")
store_embeddings(collection, document_list, embeddings_list, ids_list, metadata_list)
# ---------------------------------------------------------------------------------------------------------------

