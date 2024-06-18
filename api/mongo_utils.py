from pymongo import MongoClient

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import MongoDBAtlasVectorSearch

from langchain.text_splitter import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer

import os, certifi

from PIL import Image
import requests
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
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}",
}

def emb_img(obj, type="url"):

    if type == "url":

        response = requests.get(obj)

        img = Image.open(BytesIO(response.content))
        
        return model.encode(img)

    elif type == "file":
        img = Image.open(BytesIO(obj.stream.read()))   
    
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

    MONGO_URI = os.getenv("MONGO_URI")

    client = MongoClient(MONGO_URI, tlsCAFile=ca)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("\nPinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client

def insert_movie(title, client=None):

    cl_db = client[os.getenv("CINELENS_DB")]

    movie = get_details(title, headers)

    movie['name'] = title.lower().replace(' ', '-')

    movie_col = cl_db[os.getenv("MOVIES_COL")]

    movie_col.insert_one(movie)

    return movie_col

def insert_vs(movie, client=None):

    docs = get_docs(movie)

    cl_db = client[os.getenv("CINELENS_DB")]

    vs_col = cl_db[os.getenv("VS_COL")]

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

    cl_db = client[os.getenv("CINELENS_DB")]

    img_col = cl_db[os.getenv("IMGS_COL")]

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

    cl_db = client[os.getenv("CINELENS_DB")]

    movie_col = cl_db[os.getenv("MOVIES_COL")] 

    movie = movie_col.find_one( {"name": f"{title.lower().replace(' ', '-')}"} )

    return movie

def get_vs(client=None):

    cl_db = client[os.getenv("CINELENS_DB")]

    vs_col = cl_db[os.getenv("VS_COL")]

    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    os.getenv("MONGO_URI"),
    cl_db + "." + f"{vs_col}",
    OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), 
                            disallowed_special=()),
    )

    return vector_search

def get_img(query, client=None, type="file"):

    cl_db = client[os.getenv("CINELENS_DB")]

    img_col = cl_db[os.getenv("IMGS_COL")]

    query_emb = emb_img(query, type)

    pipeline = [
    {
        "$vectorSearch": {
            "index": "cl_index",
            "path": "embeddings",
            "queryVector": query_emb.tolist(),
            "numCandidates": 5,
            "limit": 5,
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
    }
    ]

    results = list(img_col.aggregate(pipeline))

    return results
