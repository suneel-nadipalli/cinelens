from flask import Flask, request

from dotenv import load_dotenv

import os

from flask_cors import CORS

from PIL import Image

from mongo_utils import *

from io import BytesIO

from base64 import b64encode

load_dotenv(dotenv_path="./.env.local")

DEBUG = bool(os.environ.get("DEBUG", False))

app = Flask(__name__)

CORS(app)

app.config["DEBUG"] = DEBUG

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/img_rag", methods=["POST"])
def img_rag():

    client = connect_to_mongo()

    print("\nRequest received\n")

    image = request.files['image']

    results = get_img(image, client=client, type="file")

    img_results = []

    for doc in results:

        image = b64encode(requests.get(doc['url'], headers=headers).content).decode('utf-8')
            
        img_results.append(
            {
                "url": doc["url"],
                "score": doc["score"],
                "source": doc["source"],
                "image": image
            }
        )

    client.close()

    return img_results


if __name__ == "__main__":
    app.run(debug=True, port=5050)