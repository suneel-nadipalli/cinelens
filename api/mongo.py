from glob import glob
import os

from PIL import Image

# I'm using MongoDB as my vector database:
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from transformers import ViTFeatureExtractor, ViTModel

from glob import glob

from huggingface_hub import login

import certifi

from dotenv import load_dotenv

import bson.binary

load_dotenv(dotenv_path="../.env.local")

# Load model directly
HF_TOKEN = os.getenv("HF_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

DB_NAME = os.getenv("DB_NAME")

COLLECTION_NAME = os.getenv("COLLECTION_NAME")

ATLAS_INDEX = os.getenv("ATLAS_INDEX")

# Login to the Hugging Face Hub

login(token=HF_TOKEN)

feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")
model = ViTModel.from_pretrained("google/vit-base-patch16-224")

def connect_to_mongo():
    ca = certifi.where()

    client = MongoClient(MONGO_URI, tlsCAFile=ca)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("\nPinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client

def generate_image_embeddings(myImage):
    image = Image.open(myImage).convert('RGB')
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.tolist()
    return embeddings[0][0]

def insert_imaegs(client, path):

    alldata = list()

    images = list()
    for i in glob(f"{path}/*"):
        images.append(i)

    for index, y in enumerate(images): # store images and their corresponding embeddings
        print(y)
        with open(y, "rb") as f:
            image = f.read()
            alldata.append({
                "image_path" : y,
                "image" : bson.binary.Binary(image),
                "embeddings" : generate_image_embeddings(y)
            })

    db = client[DB_NAME]

    # Ensure the collection exists, because otherwise you can't add a search index to it.
    try:
        db.create_collection(COLLECTION_NAME)
    except CollectionInvalid:
        print("\nImages collection already exists")
    
    collection = db[COLLECTION_NAME]

    print(len(alldata))

    print(alldata[0].keys())

    result = collection.insert_many(alldata)

    # result = collection.update_many(filter={}, update=alldata, upsert=True)

    document_ids = result.inserted_ids
    print(f"\n# of documents inserted: {len(document_ids)}")
    #print(f"_id of inserted document: {document_ids}")
    print("\nProcess Completed!")


def get_sim_imgs(query_img, client):

    query_img_embedding = generate_image_embeddings(query_img)

    print("\nQuery image embedding generated")

    db = client[DB_NAME]

    collection = db[COLLECTION_NAME]

    pipeline = [
    {
        "$vectorSearch": {
            "index": f"{ATLAS_INDEX}",
            "path": "embeddings",
            "queryVector": query_img_embedding,
            "numCandidates": 5,
            "limit": 5,
        }
    },
    {
        "$project": {
            "_id": 0,
            "image_path": 1,
            "image": 1,
            "score": {
                "$meta": "vectorSearchScore"
            }
        }
    }
]

    results = collection.aggregate(pipeline)

    print("\nAggregation pipeline executed")

    results = [document for document in results]

    return results


