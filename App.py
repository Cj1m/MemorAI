import os
from flask import Flask, request, jsonify
from AIChatBot import AIChatBot
from Brain.BrainSelector import BrainSelector

from Config import OPENAI_API_KEY, PINECONE_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
app = Flask(__name__)

brain = BrainSelector().select()
chatbot = AIChatBot(brain)

@app.route('/interact', methods=['POST'])
def interact():
    data = request.get_json()
    message = data.get('message', '')
    
    if message:
        response = chatbot.interact(message)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "No message provided"}), 400


if __name__ == '__main__':
    app.run(debug=True)
