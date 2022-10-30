import requests
from bs4 import BeautifulSoup

url = 'https://tululu.org/b1/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

title_tag = soup.find('h1')
title = title_tag.text.split('::')[0].strip()
author = title_tag.text.split('::')[-1].strip()
print(f'Название: {title}')
print(f'Автор: {author}')
