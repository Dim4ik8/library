import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path


def download_txt(url, filename, folder='books/', params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    filename = sanitize_filename(filename)
    Path(folder).mkdir(exist_ok=True)
    with open(f'{os.path.join(folder, filename)}.txt', 'w', encoding='UTF-8') as file:
        file.write(response.text)
    return(f'{os.path.join(folder, filename)}.txt')


def main():
    url = 'https://tululu.org/b1/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')
    title = title_tag.text.split('::')[0].strip()
    author = title_tag.text.split('::')[-1].strip()
    print(f'Название: {title}')
    print(f'Автор: {author}')

    url_book = 'http://tululu.org/txt.php?id=1'
    print(download_txt(url_book, 'Алиби'))

    print(download_txt(url_book, 'Али/би', folder='books/'))

    print(download_txt(url_book, 'Али\\би', folder='txt/'))

if __name__ == '__main__':
    main()