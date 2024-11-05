from flask import Flask, render_template, request
from storeEmbeddings import initialize_chromadb, get_or_create_collection
from searchEmbeddings import search_embeddings

app = Flask(__name__)

chroma_client = initialize_chromadb()

# Create collections for product and prompt
collection_product = get_or_create_collection(chroma_client, collection_name="product")
collection_prompt = get_or_create_collection(chroma_client, collection_name="prompts")

@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = None
    ans_product = None
    ans_prompt = None
    
    if request.method == 'POST':
        user_query = request.form['user_input']
        ans_product = search_embeddings(collection_product, query=user_query)
        ans_prompt = search_embeddings(collection_prompt, query=user_query)

    return render_template('index.html', 
                           user_input=user_input, 
                           ans_product=ans_product, 
                           ans_prompt=ans_prompt)

if __name__ == '__main__':
    app.run(debug=True)
