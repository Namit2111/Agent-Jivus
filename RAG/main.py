from storeEmbeddings import initialize_chromadb,get_or_create_collection
from searchEmbeddings import search_embeddings


chroma_client = initialize_chromadb()
collection_product = get_or_create_collection(chroma_client,collection_name="product")
collection_prompt = get_or_create_collection(chroma_client,collection_name="prompts")

user_query = "Can you explain how the performance review is conducted for employees in PeopleHub?"

ans_product = search_embeddings(collection_product, query=user_query)
ans_prompt = search_embeddings(collection_prompt, query=user_query)


'''
currently returning only 1 result can be changed in searchEmbeddings.py 


Distance represents similarity 
0 to 0.5: High similarity (good match)
0.5 to 1.0: Moderate similarity (relevant but not exact match)
1.0 to 1.5: Low similarity (partial match)
Above 1.5: Very low similarity (likely unrelated)

Longer the context better the result
'''
print(ans_product)
print("*"*50)
print(ans_prompt)