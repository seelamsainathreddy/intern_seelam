import os
import requests
from pymongo import MongoClient



s = requests.Session()

api_base = "https://api.endpoints.anyscale.com/v1"
token = "esecret_ihqjgctj2iwceshqxdsrxfypuq"
url = f"{api_base}/chat/completions"


s = requests.Session()
mongo_uri = "mongodb+srv://intern:JeUDstYbGTSczN4r@interntest.i7decv0.mongodb.net/"
client = MongoClient(mongo_uri)

db = client['intern']  # Replace with your actual database name
collection = db['papers']  # Replace with your actual collection name

# Fetch all documents from the 'intern' collection
documents = [document['transcription'] for document in collection.find({}, {'transcription': 1})]

conversation = [
    {"role": "system", "content": "You are a knowledgeable assistant."},
]

for document in documents:
    document_chunks = [document[i:i+350] for i in range(0, len(document), 350)]

    for chunk in document_chunks:
        conversation.append({"role": "user", "content": chunk})

    user_queries = [
        {"role": "user", "content": "what is the number of biotech employees"}
        # Add more user queries as needed
    ]

    # Add user queries to the conversation
    conversation.extend(user_queries)
        

    body = {
    "model": "meta-llama/Llama-2-70b-chat-hf",
    "messages": conversation,
    "temperature": 0.7
    }

    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        print(resp.json())
