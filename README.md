# MemorAI

MemorAI is a conversational AI chatbot that uses its memory to provide more context-aware and personalized responses. By leveraging OpenAI's GPT-4, MemorAI can store and recall information from previous interactions to enhance the user experience.

## Features

- Context-aware conversation using stored memory
- Utilizes GPT-4 for natural language understanding and generation
- Extensible memory storage system with support for Pinecone and Weaviate databases
- Easy to use and interact with through a simple command-line interface

## Getting Started

### Prerequisites

- Python 3.8 or higher
- An API key for OpenAI's GPT-4
- Either a local Weaviate DB or a Pinecone API key

### Installation

1. Clone the repository:

```
git clone https://github.com/your-username/MemorAI.git
```

2. Change to the MemorAI directory: 
```
cd MemorAI
```

3. Install the required dependencies: 
```
pip install -r requirements.txt
```

4. Rename `Config.example.py` to `Config.py` and configure API keys:

```python
OPENAI_API_KEY = "your_openai_api_key"
PINECONE_API_KEY = "your_pinecone_api_key" # Only required for BRAIN_TYPE="Pinecone"

# Choose between 'Pinecone' and 'Weaviate'
BRAIN_TYPE = "Pinecone"

# Pinecone settings
PINECONE_ENVIRONMENT = "your_pinecone_environment" # Only required for BRAIN_TYPE="Pinecone"

# Weaviate settings
WEAVIATE_URL = "your_weaviate_url"
```

## Usage
1. Run the main script:
```
python Main.py
```

2. Interact with MemorAI using the command-line interface:
```
User: Hi, my name is Christopher. Nice to meet you!
MemorAI: Hello Christopher, it's nice to meet you too! How may I assist you today?
```

3. MemorAI will learn from conversation and will remember details between sessions.


## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
OpenAI for providing the GPT API
Weaviate and Pinecone for their vector database software and services.