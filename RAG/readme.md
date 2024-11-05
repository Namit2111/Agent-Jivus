# steps to run ti flask app 
```bash
pip install -r requirements.txt
python flask_app.py
```

# info

- data folder contains synthetic data used to create db
- use createDB.py to create new embeddings on new data 
- use main.py to search in the embeddings 
- db folder contains embeddings 

* leaderboard 
- https://huggingface.co/spaces/mteb/leaderboard leaderbord for open source embeddings models
 

| Feature                | Pinecone | Weaviate | Milvus | Qdrant | Chroma | Elasticsearch | PGvector |
|------------------------|----------|----------|--------|--------|--------|----------------|----------|
| Open Source            | ❌       | ✅       | ✅     | ✅     | ✅     | ❌             | ✅       |
| Self-host              | ❌       | ✅       | ✅     | ✅     | ✅     | ✅             | ✅       |
| Cloud Management       | ✅       | ✅       | ✅     | ✅     | ❌     | ✅             | ✔️       |
| Queries Per Second     | 150      | 791      | 2406   | 326    | ?      | 700-100        | 141      |
| Latency (ms)          | 1        | 2        | 1      | 4      | ?      | ?              | 8        |
| Free Hosted Tier       | ✅       | ✅       | ✅     | ✅     | ✅     | Varied         | Varied   |

### Feature Descriptions
- **Open Source**: Indicates whether the vector database is available as open-source software, allowing users to modify and distribute it.
- **Self-host**: Indicates whether the database can be hosted on a user’s own infrastructure rather than relying on a cloud service.
- **Cloud Management**: Indicates if the service provides cloud management options for easy deployment and scaling.
- **Queries Per Second**: The number of queries the database can handle in a second, reflecting its performance capabilities.
- **Latency (ms)**: The average time it takes to return search results, with lower values indicating better performance.
- **Free Hosted Tier**: Indicates if a free tier is available for users to test and use the database with limited features or capacity.
