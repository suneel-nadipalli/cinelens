import requests, re, os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def get_cast(cast_list):
    cast = []

    for member in cast_list:
        cast.append(
            {
                "name": member['name'].strip(),
                "role": member['character'].strip(),
                "department": member['known_for_department'].strip()
            }
        )

    return cast    


def get_providers(watch_providers):
    
    providers = []

    keys = watch_providers.keys()

    for key in keys:

        temp = watch_providers[key]

        if 'flatrate' in temp.keys():
            for provider in temp['flatrate']:
                providers.append(provider['provider_name'])

        elif 'buy' in temp.keys():
            for provider in temp['buy']:
                providers.append(provider['provider_name'])

        elif 'rent' in temp.keys():
            for provider in temp['rent']:
                providers.append(provider['provider_name'])

        else:
            pass                
    

    providers = [provider.strip() for provider in providers]

    providers = list(set(providers))

    substrings = ["prime", "max", "netflix", "hulu", "peacock", "youtube", "disney"]

    def contains_substring(element):
        return any(re.search(sub, element, re.IGNORECASE) for sub in substrings)

    providers = [element for element in providers if contains_substring(element)]

    providers = [provider for provider in providers if len(provider.split()) <= 3 ] 

    return providers   


def get_details(title, headers):

    base_url = "https://api.themoviedb.org/3/movie/"

    details = {}

    title_url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true&language=en-US&page=1"

    resp = requests.get(title_url, headers=headers)

    if resp.status_code == 200:

        data = resp.json()

        if data['results']:
            movie_id = data['results'][0]['id']

            details['id'] = movie_id

            details_url = f"{base_url}{movie_id}?language=en-US"

            resp = requests.get(details_url, headers=headers)

            if resp.status_code == 200:
                data = resp.json()

                details['title'] = data['title']
                
                details['release_date'] = data['release_date']
                
                details['runtime'] = data['runtime']
                                
                details['rating'] = data['vote_average']
                
                details['overview'] = data['overview']
                
                details['tagline'] = data['tagline']

                details['genres'] = [genre['name'] for genre in data['genres']]

                details['imdb_id'] = data['imdb_id']

            cast_url = f"{base_url}{movie_id}/credits?language=en-US"

            resp = requests.get(cast_url, headers=headers)

            if resp.status_code == 200:
                data = resp.json()

                cast = data['cast']

                details['cast'] = get_cast(cast)

            keywords_url = f"{base_url}{movie_id}/keywords"

            resp = requests.get(keywords_url, headers=headers)

            if resp.status_code == 200:

                data = resp.json()

                details['keywords'] = [keyword['name'] for keyword in data['keywords']]    

            providers_url = f"{base_url}{movie_id}/watch/providers"

            resp = requests.get(providers_url, headers=headers)

            if resp.status_code == 200:

                data = resp.json()

                details['providers'] = get_providers(data['results'])  

            images_url = f"{base_url}{movie_id}/images"

            base_image_url = "https://image.tmdb.org/t/p/w500"

            resp = requests.get(images_url, headers=headers)

            if resp.status_code == 200:

                data = resp.json()

                keys = ['posters', 'backdrops']

                details['images'] = []

                for key in keys:

                    if data[key]:

                        urls = [ f"{base_image_url}{image['file_path']}" for image in data[key]]

                        details['images'].extend(urls)
                
                details['images'] = details['images'][:50]

                details['poster'] = f"{base_image_url}{data['posters'][0]['file_path']}"

                details['backdrop'] = f"{base_image_url}{data['backdrops'][0]['file_path']}"

    return details

def get_poster(title, headers):
    base_url = "https://api.themoviedb.org/3/movie/"

    details = {}

    title_url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true&language=en-US&page=1"

    resp = requests.get(title_url, headers=headers)

    if resp.status_code == 200:

        data = resp.json()

        if data['results']:
            movie_id = data['results'][0]['id']

            images_url = f"{base_url}{movie_id}/images"

            base_image_url = "https://image.tmdb.org/t/p/w500"

            resp = requests.get(images_url, headers=headers)

            if resp.status_code == 200:

                data = resp.json()

                details['poster'] = f"{base_image_url}{data['posters'][0]['file_path']}"

    return details['poster']


def get_new_providers(providers):

    providers = [provider.lower() for provider in providers]

    providers_new = []

    for provider in providers:
        if 'prime' in provider:
            providers_new.append('prime')
        
        if 'disney' in provider:
            providers_new.append('disney')

        if 'netflix' in provider:
            providers_new.append('netflix')
        
        if 'max' in provider:
            providers_new.append('max')
        
        if 'youtube' in provider:
            providers_new.append('youtube')
    
    return list(set(providers_new))