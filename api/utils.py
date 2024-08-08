from langchain_openai.chat_models import ChatOpenAI

from langchain_core.prompts import PromptTemplate

from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from mongo_utils import *

import openai

from dotenv import load_dotenv

from tqdm import tqdm

import os, requests, time 

from pathlib import Path

load_dotenv(dotenv_path=".env.local")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYTBmYmYzYzRmZDdhZWVlMjZiNTc4MGUyOGU4YTdmZiIsInN1YiI6IjY2NmRkMWM5MjA2NGRmMzI3MGRmOTBiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qWFPmYvwpJ4NgJkvlq-3P--69tDxaomyUvSkz8aXdZs",
}

model = ChatOpenAI(api_key="sk-no-key-required", 
        model_name = 'LLaMA_CPP',
        base_url="http://127.0.0.1:8080/v1",
        temperature=0.3)

# model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), 
#         model_name = 'gpt-4',
#         temperature=0.3)

def get_titles(n=500):

    titles_path = Path('movies.txt')

    if titles_path.is_file():
        print("Using existing file")
        with open('movies.txt', 'r', encoding="utf-8") as f:
            titles = [x.strip() for x in f.readlines()]
    else:
        cnt = 500

        titles = []

        for idx in tqdm(range(1, cnt+1)):
            url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={idx}"

            response = requests.get(url, headers=headers)

            data = response.json()

            titles.extend(
            [movie['title'] for movie in data['results'] if movie['original_language'] == 'en']
            )
        
        with open('movies.txt', 'w', encoding="utf-8") as f:
            for title in titles:
                f.write(f"{title}\n")
    
    return titles[:n]

def insert_all_movies(titles=None, n=500, client=None):
    
    if not titles:
        titles = get_titles(n)

    for title in tqdm(titles):
        title = title.strip()
        insert_movie(title, client=client)

def insert_all_vs(titles=None, n=500, client=None):
    
    if not titles:
        titles = get_titles(n)

    titles = titles[:n]

    for title in tqdm(titles):
        movie = get_movie(title)
        if movie:
            insert_vs(movie, client=client)

def insert_all_imgs(titles=None, n=500, client=None):
    
    if not titles:
        titles = get_titles(n)

    titles = titles[:n]

    for title in tqdm(titles):
        insert_imgs(title, client=client)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def query_rag_movie(text, client, movies):

    if client is None:
        client = connect_to_mongo()
    
    vs = get_vs(client=client)

    retriever = vs.as_retriever(
                search_type = "similarity",
                search_kwargs = {"k": 3}
                )
    
    template = """Answer the question: {question} based only on the following context:
    context: {context}
    """

    output_parser = JsonOutputParser()

    prompt = PromptTemplate.from_template(template = template,
                        input_varaibles = ["context", "question"],
                        output_variables = ["answer"],)

    output_parser = StrOutputParser()

    retrieval_chain = (
    {"context": retriever | format_docs,  "question": RunnablePassthrough()}
    | prompt 
    | model 
    | output_parser
    )


    system_prompt = """
    [INST] <<SYS>>
    You are part of an intelligent movie search engine.
    I will provide you with a description of a movie based on a given text.
    Based on the provided description, you will have to answer a question.  
    <</SYS>>

    """
    
    query = f"""

    {system_prompt}

    Here's my description of the movie:

    {text}

    Return at least 5 movies that are similar to the movie described above among the following: {movies} .

    Return just the titles of the movies in a Python list. 

    [/INST]
    
    """

    response = retrieval_chain.invoke(query)

    return response

def query_movie(text):

    client = openai.OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="sk-no-key-required"
    )
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": text}
        ]
    )
    
    return completion.choices[0].message.content            
    


def timed_function(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()

    elapsed_time = end_time - start_time
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    
    print(f"Execution time: {formatted_time}")
    return result