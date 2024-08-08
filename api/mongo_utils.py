from pymongo import MongoClient

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import MongoDBAtlasVectorSearch

from langchain.text_splitter import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer

import os, certifi

from PIL import Image
import requests, random
from io import BytesIO

from dotenv import load_dotenv
from tqdm import tqdm

from movie_utils import get_details

load_dotenv(dotenv_path=".env.local")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = SentenceTransformer("clip-ViT-L-14")

from langchain_community.document_loaders import WebBaseLoader

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYTBmYmYzYzRmZDdhZWVlMjZiNTc4MGUyOGU4YTdmZiIsInN1YiI6IjY2NmRkMWM5MjA2NGRmMzI3MGRmOTBiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qWFPmYvwpJ4NgJkvlq-3P--69tDxaomyUvSkz8aXdZs",
}

def emb_img(obj, type="url"):

    if type == "url":

        response = requests.get(obj)

        img = Image.open(BytesIO(response.content))
       
        return model.encode(img)

    elif type == "file":
        try:
         img = Image.open(BytesIO(obj.stream.read()))   
        except:
            img = Image.open(obj) 
    
        return model.encode(img)
    
    elif type == "text":
        return model.encode(obj)


def get_docs(movie):

    imdb_url = f"https://www.imdb.com/title/{movie['imdb_id']}"

    tmdb_url = f"https://www.themoviedb.org/movie/{movie['id']}"

    lbxd_name = movie['title'].replace(' ', '-').lower()

    lbxd_url = f"https://letterboxd.com/film/{lbxd_name}/"

    loader = WebBaseLoader(
        [
            imdb_url,
            tmdb_url,
            lbxd_url
        ]
    )

    docs = loader.load()

    return docs


def connect_to_mongo():

    ca = certifi.where()

    MONGO_URI = "mongodb+srv://suneelnadipalli:hPMlZEGwWrHm1hDH@cinelenscluster.gj390ta.mongodb.net/"

    client = MongoClient(MONGO_URI, tlsCAFile=ca)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("\nPinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client

def insert_movie(title, client=None):

    cl_db = client["cinelens"]

    movie = get_details(title, headers)

    movie['name'] = title.lower().replace(' ', '-')

    movie_col = cl_db["movies"]

    movie_col.insert_one(movie)

    return movie_col

def insert_vs(movie, client=None):

    docs = get_docs(movie)

    cl_db = client["cinelens"]

    vs_col = cl_db["vectorstores"]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, 
                                                    chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), 
                            disallowed_special=())

    # Create embeddings in atlas vector store
    vector_search = MongoDBAtlasVectorSearch.from_documents( 
                                    documents=chunks, 
                                    embedding= embeddings, 
                                    collection=vs_col,)
        
    return vector_search

def insert_imgs(title, client=None):

    cl_db = client["cinelens"]

    img_col = cl_db["images"]

    movie = get_movie(title, client)

    image_urls = movie['images']

    for url in tqdm(image_urls):
        try:
            img_col.insert_one(
            {
                "embeddings": emb_img(url, type="url").tolist(),
                "url": url,
                "source": title.lower().replace(' ', '-')
            }
            )
        except:
            continue

def get_movie(title, client=None):

    cl_db = client["cinelens"]

    movie_col = cl_db["movies"] 

    movie = movie_col.find_one( {"name": f"{title.lower().replace(' ', '-')}"} )

    return movie

def get_vs(client=None):

    cl_db = client["cinelens"]

    vs_col = cl_db["vectorstores"]

    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    "mongodb+srv://suneelnadipalli:hPMlZEGwWrHm1hDH@cinelenscluster.gj390ta.mongodb.net/",
    "cinelens" + "." + "vectorstores",
    OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), 
                            disallowed_special=()),
    )

    return vector_search

def get_url(title, client=None):

    cl_db = client["cinelens"]

    movie_col = cl_db["movies"]

    movie = movie_col.find_one({"name": title})

    urls = movie['images']

    return random.choice(urls)

def get_img(query, client=None, type="file"):

    cl_db = client["cinelens"]

    img_col = cl_db["images"]

    query_emb = emb_img(query, type)

    pipeline = [
    {
        "$vectorSearch": {
            "index": "cl_index",
            "path": "embeddings",
            "queryVector": query_emb.tolist(),
            "numCandidates": 250,
            "limit": 250,
        }
    },
    {
        "$project": {
            "_id": 0,
            "url": 1,
            "source": 1,
            "score": {
                "$meta": "vectorSearchScore"
            }
        }
    },
    {
        "$group": {
            "_id": "$source",
            "score": {"$avg": "$score"}
        }
    },
    {
        "$sort": {
            "score": -1
    }
    }
    ]

    results = list(img_col.aggregate(pipeline))

    return results
