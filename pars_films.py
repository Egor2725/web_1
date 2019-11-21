import requests
from bs4 import BeautifulSoup

def get_html():
    url = "https://afisha.tut.by/film/"
    r = requests.get(url)
    return r.text

def get_films():
    soup = BeautifulSoup(get_html(), 'html.parser')
    list_films = soup.find('div', id='events-block').find_all('ul')
    films = []
    for f in list_films:
        for article in f.find_all('a', {'class': 'name'}):
            films.append(article.text)
        
    return films
    
    




