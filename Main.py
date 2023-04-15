import os
from AIChatBot import AIChatBot
from Brain.BrainSelector import BrainSelector

from Config import OPENAI_API_KEY, PINECONE_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

database = BrainSelector().select()
chatbot = AIChatBot(database)
print("### Start up complete")
print("### Enter your prompt")
while True:
    user_input = input("User: ")

    if user_input.lower() == 'exit':
        break

    response = chatbot.interact(user_input)
    print("MemorAI:", response)
