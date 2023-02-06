import requests
import os
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.TooManyRedirects


def get_links_to_books(soup, base_url):
    books = soup.select('.d_book')
    links_to_books = [
        urljoin(base_url,
                book.select_one('a')['href']) for book in books
    ]
    return links_to_books


def download_txt(url, filename, folder='books/', dest_folder='', params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    check_for_redirect(response)
    filename = sanitize_filename(filename)

    Path(os.path.join(f'media/{dest_folder}/{folder}')
         ).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join('media', dest_folder, folder, f'{filename}.txt')

    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(response.text)
    book_path = {'book_path': '../' + os.path.relpath(file_path)}
    return book_path


def download_image(url, filename, folder='images', dest_folder=''):
    response = requests.get(url)
    response.raise_for_status()
    Path(os.path.join(f'media/{dest_folder}/{folder}')
         ).mkdir(parents=True, exist_ok=True)
    with open(f'{os.path.join("media", dest_folder, folder, filename)}',
              'wb') as file:
        file.write(response.content)
    image = {'img_src': '../' + os.path.relpath(os.path.join('media',
                                                             dest_folder,
                                                             folder,
                                                             filename
                                                             ))}
    return image


def parse_book_page(soup):
    author_and_title_tag = soup.select_one("div[id='content'] h1")
    title, author = author_and_title_tag.text.split('::')
    comments_tags = soup.select('.texts')
    genre_tags = soup.select('span.d_book a')
    book = {
        'title': title.strip(),
        'author': author.strip(),
        'genres': [tag.text for tag in genre_tags],
        'comments': [tag.span.text for tag in comments_tags],
    }
    return book
