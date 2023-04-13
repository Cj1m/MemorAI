import os
import openai
import pinecone
import numpy as np
from Fact import Fact
from Config import OPENAI_API_KEY, PINECONE_API_KEY, OPENAI_MODEL, OPENAI_SYSTEM_PROMPT, PINECONE_ENVIRONMENT, DEBUG_MODE, OPENAI_SUMMARIZATION_MODEL

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

PINECONE_INDEX_NAME= "memory"

print(f"### Connecting to pinecone environment: {PINECONE_ENVIRONMENT}")
pinecone.init(environment= PINECONE_ENVIRONMENT, api_key=PINECONE_API_KEY)
if PINECONE_INDEX_NAME not in pinecone.list_indexes():
    print(f"### Creating index: {PINECONE_INDEX_NAME}")
    pinecone.create_index(name=PINECONE_INDEX_NAME, metric="cosine", dimension=1536)

index = pinecone.Index(PINECONE_INDEX_NAME)


def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

def encode_data(prompt, response):
    return f"{prompt} <|> {response}"

def decode_data(encoded_data):
    key, value = encoded_data.split(": ", 1)
    data = f"Fact: '{key}' has the value '{value}'"
    return data

def store_in_pinecone(fact):
    fact_str = str(fact)
    vector = generate_embedding(fact_str)
    index.upsert([(fact_str, vector)])

def fetch_related_data_from_pinecone(prompt):
    vector = generate_embedding(prompt)
    results = index.query(vector=vector, top_k=3)

    related_data = []
    for match in results["matches"]:
        stored_data = match["id"]
        response = decode_data(stored_data)

        if DEBUG_MODE:
            print("\t###Memory: " + response)
            print("\n")
        related_data.append({"role": "system", "content": "MEMORY: " + response})

    return related_data


def extract_facts_with_openai(prompt, response):
    facts = []

    conversation = f"User: {prompt}\nAI: {response}"
    
    openai_result = openai.Completion.create(
        engine=OPENAI_SUMMARIZATION_MODEL,
        prompt=f"Summarize the following conversation into a list of semicolon separated key facts:\n{conversation}\n\nKey Facts (e.g FACT A KEY: FACT A VALUE; etc):",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = openai_result.choices[0].text.strip()

    if DEBUG_MODE:
        print("\n")
        print(f"\t###Summary: {summary}")
        print("\n")

    fact_strings = summary.split(';')

    for fact_string in fact_strings:
        key_value = fact_string.split(':', 1)
        if len(key_value) == 2:
            key, value = key_value
            key, value = key.strip(), value.strip()

            facts.append(Fact(key, value))

    return facts

def interact(prompt):
    stored_data = fetch_related_data_from_pinecone(prompt)

    context = [{"role": "system", "content": OPENAI_SYSTEM_PROMPT}] + stored_data
    openai_result = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=context + [{"role": "user", "content": prompt}]
    )

    response = openai_result.choices[0].message.content.strip()

    facts = extract_facts_with_openai(prompt, response)
    for fact in facts:
        store_in_pinecone(fact)

    return response


print("### Start up complete")
print("### Enter your prompt")
while True:
    user_input = input("User: ")

    if user_input.lower() == 'exit':
        break

    response = interact(user_input)
    print("AI Response:", response)
