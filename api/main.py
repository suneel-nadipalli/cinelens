from mongo_utils import *

from movie_utils import *

from utils import *

from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

import os, time

load_dotenv(dotenv_path=".env.local")

client = connect_to_mongo()

print("\nRequest received\n")

titles = get_titles(n=20) 

text = """
A movie about a guy dressed like a bat or something. I don't know, it's got Christian Bale in it.
"""

# results = timed_function(query_rag_movie, text, client, titles)

# print(results)

start_time = time.time()

res_text = ""
with ThreadPoolExecutor(max_workers=6) as executor:  # Adjust max_workers based on your system's capabilities
    futures = []
    futures.append(executor.submit(query_rag_movie, text, client, titles))
    
    for future in futures:
        res_text += future.result()

end_time = time.time()

elapsed_time = end_time - start_time
formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

print(f"Execution time: {formatted_time}")

print(res_text)
# n = 1

# titles = get_titles(n)

# titles = ['The Dark Knight Rises', 'Batman Begins', 'Batman vs Teenage Mutant Ninja Turtles']

# print(titles)

# client = connect_to_mongo()

# cl_db = client[os.getenv("CINELENS_DB")]

# movie_col = cl_db[os.getenv("MOVIES_COL")]

# insert_all_movies(titles, n)

# insert_all_vs(titles, n)

# insert_all_imgs(titles, n, client=client)

client.close()