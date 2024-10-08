from flask import Flask, request

from dotenv import load_dotenv

import os

from flask_cors import CORS

from mongo_utils import *

from movie_utils import *

from utils import *

from concurrent.futures import ThreadPoolExecutor

load_dotenv(dotenv_path="./.env.local")

DEBUG = bool(os.environ.get("DEBUG", False))

app = Flask(__name__)

CORS(app)

app.config["DEBUG"] = DEBUG

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}",
}

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/img_rag", methods=["POST"])
def img_rag():

    client = connect_to_mongo()

    print("\nRequest received\n")

    image = request.files['image']

    print(type(image))

    results = get_img(image, client=client, type="file")

    img_results = []

    for doc in results:

        movie = get_movie(doc["_id"], client=client)

        # url = get_url(doc["_id"], client=client)

        # image = b64encode(requests.get(url, headers=headers).content).decode('utf-8')
            
        img_results.append(
            {
                'poster': get_poster(movie['title'], headers=headers),
                'name': doc['_id'],
                'score': doc['score'],
                'title': movie['title'],
                'overview': movie['overview'],
                'release_date': movie['release_date'],
                'rating': round(movie['rating'] / 2, 1),
                'tagline': movie['tagline'],
                'runtime': movie['runtime'],
                'genres': (movie['genres']),
                'providers': get_new_providers(movie['providers']),
            }
        )

    client.close()

    return img_results[:5]

@app.route("/text_rag", methods=["POST"])
def text_rag():

    client = connect_to_mongo()

    print("\nRequest received\n")

    text = request.json['text']

    print(text)

    titles = get_titles(n=20) 

    res_text = ""
    with ThreadPoolExecutor(max_workers=6) as executor:  # Adjust max_workers based on your system's capabilities
        futures = []
        futures.append(executor.submit(query_rag_movie, text, client, titles))
        
        for future in futures:
            res_text += future.result()
    
    results = []

    for title in titles:
        if title.lower() in res_text.lower():
            results.append(title)
    
    results = results[:5]

    # results = (query_rag_movie(text, client=client, movies=titles))

    text_results = []

    for doc in results:

        name = doc.lower().replace(" ", "-")

        movie = get_movie(name, client=client)

        if movie:

            text_results.append(
                {
                    'poster': get_poster(movie['title'], headers=headers),
                    'name': name,
                    'title': movie['title'],
                    'overview': movie['overview'],
                    'release_date': movie['release_date'],
                    'rating': round(movie['rating'] / 2, 1),
                    'tagline': movie['tagline'],
                    'runtime': movie['runtime'],
                    'genres': (movie['genres']),
                    'providers': get_new_providers(movie['providers']),
                }
            )
        else:
            pass    

    client.close()

    return text_results[:5]


if __name__ == "__main__":
    app.run(host='0.0.0.0')