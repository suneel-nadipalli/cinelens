from langchain_openai.chat_models import ChatOpenAI

from langchain_core.prompts import PromptTemplate

from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from mongo_utils import *

from dotenv import load_dotenv

from tqdm import tqdm

import os, requests

from pathlib import Path

load_dotenv(dotenv_path=".env.local")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}",
}

model = ChatOpenAI(api_key="sk-no-key-required", 
        model_name = 'LLaMA_CPP',
        base_url="http://127.0.0.1:8080/v1",
        temperature=0.3)

def get_titles(n=500):

    titles_path = Path('movies.txt')

    if titles_path.is_file():
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

def query_rag_movie(query):
    vs = get_vs()

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


    query = f"""
    Which movie is being described with the following details: 

    {query}

    """

    response = retrieval_chain.invoke(query)

    return response

