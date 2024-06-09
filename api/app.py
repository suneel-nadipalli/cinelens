from flask import Flask, request, jsonify

import requests

from dotenv import load_dotenv

import os

from flask_cors import CORS

from utils import send_image_get_stream

from mongo import *

import base64

load_dotenv(dotenv_path="./.env.local")

DEBUG = bool(os.environ.get("DEBUG", False))

app = Flask(__name__)

CORS(app)

app.config["DEBUG"] = DEBUG

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/sim_img", methods=["POST"])
def sim_img():
    
    print("\nRequest received")

    image = request.files["image"]

    print("\nImage received")

    image_name = image.filename

    image_path = f"../misc/temp/{image_name}"

    image.save(image_path)

    print("\nImage saved")

    client = connect_to_mongo()

    results = get_sim_imgs(image_path, client)

    print("\nResults fetched")

    sim_imgs = []

    for document in results:
        
        image = base64.b64encode(document['image']).decode('utf-8')

        sim_imgs.append(
            {
                "image": image,
                "score": document['score'],
                "name": document['image_path'].split("/")[-1].split(".")[0].split("\\")[-1]
            }
        )

    print("\nResults processed")

    client.close()

    print("\nConnection closed")

    return sim_imgs

@app.route("/describe_img", methods=["POST"])
def describe_img():

    image = request.files["image"]

    print(type(image))

    image_name = image.filename

    image_path = f"../misc/images/{image_name}"

    image.save(image_path)

    # return {"resp": f"Image {image_name} saved successfully"}

    _input = "Describe this image in detail"
    
    response = send_image_get_stream(image_path, input=_input)

    if response.status_code == 200:
        data = response.json()['content']

        status = response.status_code
    
    else:
        data = "Error"

        status = response.status_code

    return jsonify({"desc": data, "status": status})    



if __name__ == "__main__":
    app.run(debug=True, port=5050)