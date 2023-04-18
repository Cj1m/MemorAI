import weaviate
import openai
from Brain.Brain import Brain
from Config import WEAVIATE_URL

class WeaviateBrain(Brain):
    def __init__(self):
        self.client = weaviate.Client(WEAVIATE_URL)
        self.class_name = "Fact"

        if not self._class_exists():
            self._create_fact_class()

    def _class_exists(self):
        return any(schema_class["class"] == self.class_name for schema_class in self.client.schema.get()["classes"])

    def _create_fact_class(self):
        print(f"Creating Weaviate class {self.class_name}")
        fact_class = {
            "class": self.class_name,
            "properties": [
                {
                    "name": "key",
                    "dataType": ["string"],
                },
                {
                    "name": "value",
                    "dataType": ["string"],
                },
                {
                    "name": "timestamp",
                    "dataType": ["number"],
                },
            ],
        }
        self.client.schema.create_class(fact_class)

    def _generate_embedding(self, text):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        return embeddings

    def fetch_related_data(self, prompt):
        vector = self._generate_embedding(prompt)

        nearVector = {
            "vector": vector
        }
        query = {
            "class_name": "Fact",
            "properties": ["key", "value", "timestamp"]
        }
        result = self.client.query.get(**query).with_near_vector(nearVector).with_limit(10).do()
        related_data = []
        for item in result["data"]["Get"]["Fact"]:
            key = item["key"]
            value = item["value"]
            timestamp = item["timestamp"]
            related_data.append({"role": "system", "content": f"MEMORY: '{key}' has the value '{value}'. (timestamp: {timestamp})."})
        
        return related_data

    def store_fact(self, fact):
        fact_str = str(fact)
        vector = self._generate_embedding(fact_str)

        fact_object = {
            "key": fact.key,
            "value": fact.value,
            "timestamp": fact.timestamp
        }

        try:
            self.client.data_object.create(data_object=fact_object, vector=vector, class_name="Fact")
        except weaviate.exceptions.ObjectAlreadyExistsException:
            # If the fact already exists, update it instead
            fact_id = self._get_fact_id(fact.key)
            if fact_id:
                self.client.data_object.update(data_object_id=fact_id, data_object=fact_object)

    def _get_fact_id(self, fact_key):
        query = {
            "path": ["Fact", "key"],
            "operator": weaviate.ComparisonOperators.Equal,
            "value": fact_key,
            "properties": ["id"],
        }
        result = self.client.query.get(**query)

        if result:
            return result[0]["id"]
        else:
            return None


