from mongo_utils import *

from movie_utils import *

from utils import *

from dotenv import load_dotenv

import os

load_dotenv(dotenv_path=".env.local")

n = 1

# titles = get_titles(n)

titles = ['The Dark Knight Rises', 'Batman Begins', 'Batman vs Teenage Mutant Ninja Turtles']

print(titles)

client = connect_to_mongo()

cl_db = client[os.getenv("CINELENS_DB")]

movie_col = cl_db[os.getenv("MOVIES_COL")]

# insert_all_movies(titles, n)

# insert_all_vs(titles, n)

# insert_all_imgs(titles, n, client=client)

client.close()