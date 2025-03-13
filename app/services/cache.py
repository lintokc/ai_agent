import uuid  # Import UUID module
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np
import json
from together import Together
from app.config import config

qdrant_client = QdrantClient(config.QDRANT_HOST)

client = Together(api_key=config.TOGETHER_AI_API_KEY)

COLLECTION_NAME = config.QDRANT_COLLECTION

EMBEDDING_DIM = 768


def create_collection():
    """
    Creates the Qdrant collection with a fixed vector dimension of 768.
    """
    existing_collections = qdrant_client.get_collections().collections
    if COLLECTION_NAME not in [col.name for col in existing_collections]:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


create_collection()


def get_embedding(text: str):
    """
    Fetches a 768-dimensional embedding vector using Together AI.
    """
    response = client.embeddings.create(
        model="togethercomputer/m2-bert-80M-2k-retrieval",
        input=[text],
    )

    embedding = np.array(response.data[0].embedding)

    return embedding


def cache_response(user_query: str, response: str):
    """
    Stores the query & response in Qdrant for future retrieval.
    """
    embedding = get_embedding(user_query)

    if embedding.shape[0] != EMBEDDING_DIM:
        return 

    unique_id = str(uuid.uuid4())

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=unique_id,
                vector=embedding.tolist(),
                payload={"response": json.dumps(response)},
            )
        ],
    )


def find_similar_query(user_query: str, threshold: float = 0.9):
    """
    Searches for a similar query in Qdrant.
    """
    embedding = get_embedding(user_query)

    if embedding.shape[0] != EMBEDDING_DIM:
        return None

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME, query_vector=embedding.tolist(), limit=1
    )

    if search_result and search_result[0].score >= threshold:

        return json.loads(search_result[0].payload["response"])

    return None
