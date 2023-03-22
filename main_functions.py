import json
import os.path
from nltk.corpus import stopwords

import requests


def _get_nyt_key():
    with open('JSON_Files/api_keys.json', 'r') as file:
        data = json.load(file)
    return data['nyt_key']


def get_top_stories(topic: str = 'arts'):
    return get_articles(
        f'https://api.nytimes.com/svc/topstories/v2/{topic}.json',
        f'JSON_Files/top_stories_{topic}.json'
    )


def get_most_popular(topic: str = 'viewed', age: int = 1):
    return get_articles(
        f'https://api.nytimes.com/svc/mostpopular/v2/{topic}/{age}.json',
        f'JSON_Files/most_popular_{topic}_{age}.json'
    )


def filter_words(words: list, max_words: int):
    stopwords_english = stopwords.words('english')
    filtered_words = []

    for word in words:
        if not word.isalpha():
            continue

        if word.lower() in stopwords_english:
            continue

        filtered_words.append(word)

        if len(filtered_words) >= max_words:
            break

    return filtered_words


def get_articles(url, json_file):
    api_key = _get_nyt_key()

    if os.path.exists(json_file):
        print(f'Articles found in file! Loading... (file: f"{json_file}')

        with open(json_file, 'r') as file:
            data = json.load(file)
        return data

    print(f'Articles not found in file, downloading... (file: f"{json_file}')

    response = requests.get(url, params={'api-key': api_key})
    response.raise_for_status()

    data = response.json()

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)

    return data