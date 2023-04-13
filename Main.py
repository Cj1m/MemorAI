import os
from AIChatBot import AIChatBot
from PineconeDatabase import PineconeDatabase
from Config import OPENAI_API_KEY, PINECONE_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

database = PineconeDatabase()
chatbot = AIChatBot(database)
print("### Start up complete")
print("### Enter your prompt")
while True:
    user_input = input("User: ")

    if user_input.lower() == 'exit':
        break

    response = chatbot.interact(user_input)
    print("AI Response:", response)
