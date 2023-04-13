import os
import pinecone
import openai
from Config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, DEBUG_MODE
PINECONE_INDEX_NAME= "memory"

class PineconeDatabase:
    def __init__(self):
        self.connect()
        self.index = pinecone.Index(PINECONE_INDEX_NAME)

    def connect(self):
        print(f"### Connecting to pinecone environment: {PINECONE_ENVIRONMENT}")
        pinecone.init(environment=PINECONE_ENVIRONMENT, api_key=PINECONE_API_KEY)
        if PINECONE_INDEX_NAME not in pinecone.list_indexes():
            print(f"### Creating index: {PINECONE_INDEX_NAME}")
            pinecone.create_index(name=PINECONE_INDEX_NAME, metric="cosine", dimension=1536)

    def generate_embedding(self, text):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        return embeddings

    def store_fact(self, fact):
        fact_str = str(fact)
        vector = self.generate_embedding(fact_str)
        self.index.upsert([(fact_str, vector)])

    def fetch_related_data(self, prompt):
        vector = self.generate_embedding(prompt)
        results = self.index.query(vector=vector, top_k=3)

        related_data = []
        for match in results["matches"]:
            stored_data = match["id"]
            response = self.decode_data(stored_data)

            if DEBUG_MODE:
                print("\t###Memory: " + response)
                print("\n")
            related_data.append({"role": "system", "content": "MEMORY: " + response})

        return related_data

    @staticmethod
    def decode_data(encoded_data):
        key, value = encoded_data.split(": ", 1)
        data = f"Fact: '{key}' has the value '{value}'"
        return data
