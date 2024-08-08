import sys, pytest

sys.path.append("../.")

from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env.local")

from concurrent.futures import ThreadPoolExecutor

from utils import *
from mongo_utils import *
from movie_utils import * 

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}",
}


def test_get_titles():
    n = 20
    titles = get_titles(n=n)
    assert titles is not None
    assert len(titles) == n

def test_emb_url():
    obj = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    emb = emb_img(obj, type="url")  
    assert emb is not None
    assert len(emb) == 768

def test_emb_text():
    obj = "A movie about a guy dressed like a bat or something. I don't know, it's got Christian Bale in it."
    emb = emb_img(obj, type="text")  
    assert emb is not None
    assert len(emb) == 768

def test_emb_file():
    emb = emb_img("image.jpg", type="file")  
    assert emb is not None
    assert len(emb) == 768

def test_connect_to_mongo():
    client = connect_to_mongo()
    assert client is not None    

def test_get_movie():
    client = connect_to_mongo()
    titles = get_titles(n=20)
    movie = get_movie(titles[0], client)
    assert movie is not None
    assert type(movie) == dict

def test_get_img():
    client = connect_to_mongo()
    imgs = get_img("image.jpg", client, type="file")
    assert imgs is not None
    assert type(imgs) == list

def test_get_docs():
    client = connect_to_mongo()
    titles = get_titles(n=20)
    movie = get_movie(titles[0], client)
    docs = get_docs(movie)
    assert docs is not None

def test_get_details():
    n = 5
    titles = get_titles(n=n)
    details = get_details(titles[0], headers=headers)
    assert details is not None
    assert type(details) == dict
    assert details['title'] == titles[0]
    
def test_query_rag():
    client = connect_to_mongo()
    titles = get_titles(n=20)
    text = """
    A movie about a guy dressed like a bat or something. I don't know, it's got Christian Bale in it.
    """
    res_text = ""
    with ThreadPoolExecutor(max_workers=6) as executor:  # Adjust max_workers based on your system's capabilities
        futures = []
        futures.append(executor.submit(query_rag_movie, text, client, titles))
        
        for future in futures:
            res_text += future.result()
    
    assert res_text is not None    

if __name__ == "__main__":
    pytest.main()