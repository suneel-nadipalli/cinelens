from mongo_utils import *

from movie_utils import *

from utils import *

from dotenv import load_dotenv

import os

load_dotenv(dotenv_path=".env.local")

n = 10

titles = get_titles(n)

print(titles)

client = connect_to_mongo()

# insert_all_movies(titles, n)

# insert_all_vs(titles, n)

insert_all_imgs(titles, n, client=client)

client.close()