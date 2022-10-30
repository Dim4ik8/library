import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

url = 'https://tululu.org/b1/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

title_tag = soup.find('h1')
title = title_tag.text.split('::')[0].strip()
author = title_tag.text.split('::')[-1].strip()
print(f'Название: {title}')
print(f'Автор: {author}')


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()

    filename = sanitize_filename(filename)
    os.makedirs(folder, exist_ok=True)
    with open(f'{os.path.join(folder, filename)}.txt', 'w') as file:
        file.write(response.text)
    return(f'{os.path.join(folder, filename)}.txt')


url_book = 'http://tululu.org/txt.php?id=1'
print(download_txt(url_book, 'Алиби'))

print(download_txt(url_book, 'Али/би', folder='books/'))

print(download_txt(url_book, 'Али\\би', folder='txt/'))