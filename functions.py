import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path


def check_for_redirect(response):
    if response.history:
        raise requests.TooManyRedirects


def download_txt(url, filename, folder='books/', params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    try:
        check_for_redirect(response)
        filename = sanitize_filename(filename)
        Path(folder).mkdir(exist_ok=True)
        with open(f'{os.path.join(folder, filename)}.txt', 'w', encoding='UTF-8') as file:
            file.write(response.text)
        return (f'{os.path.join(folder, filename)}.txt')
    except requests.TooManyRedirects:
        pass



def download_image(url, filename, folder='images'):
    response = requests.get(url)
    response.raise_for_status()
    Path(folder).mkdir(exist_ok=True)
    with open(f'{os.path.join(folder, filename)}.jpg', 'wb') as file:
        file.write(response.content)

def parse_book_page(soup):

    title_tag = soup.find('h1')
    book_info = {'title': title_tag.text.split('::')[0].strip(),
                'author': title_tag.text.split('::')[-1].strip(),
                'genres': [genre.text for genre in soup.find('span', class_='d_book').find_all('a')]
                 }

    return book_info

def main():
    book_start_url = 'https://tululu.org/b'
    response = requests.get(url)
    response.raise_for_status()


    # soup = BeautifulSoup(response.text, 'lxml')
    for count in range(10):
        url = book_start_url + str(count + 1) + '/'

    # title_tag = soup.find('h1')
    # title = title_tag.text.split('::')[0].strip()
    # author = title_tag.text.split('::')[-1].strip()
    # print(f'Название: {title}')
    # print(f'Автор: {author}')
    #
    # url_book = 'http://tululu.org/txt.php?id=1'
    # print(download_txt(url_book, 'Алиби'))
    #
    # print(download_txt(url_book, 'Али/би', folder='books/'))
    #
    # print(download_txt(url_book, 'Али\\би', folder='txt/'))


if __name__ == '__main__':
    main()
