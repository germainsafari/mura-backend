import openai
from app import db
from models import KnowledgeBase, Embeddings  # Model for storing embeddings

openai.api_key = ''

def generate_embeddings(text):
    """Generate embeddings for the given text using OpenAI's embedding API."""
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']

def embed_documents():
    """Generate and store embeddings for all documents in the KnowledgeBase."""
    documents = KnowledgeBase.query.all()
    for doc in documents:
        embedding = generate_embeddings(doc.content)
        db.session.add(Embeddings(content_id=doc.id, embedding=embedding))
    db.session.commit()

embed_documents()
