import json
import pathlib

import requests
from bs4 import BeautifulSoup
import logging
import re
from functions import check_for_redirect, download_the_book, get_links_to_books
from urllib.parse import urljoin
import argparse
import os

logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(
        description='Парсим библиотеку'
    )
    parser.add_argument(
        '-s', '--start_page',
        help='С какой страницы качать',
        nargs='?',
        default='0',
        type=int
    )
    parser.add_argument(
        '-e',
        '--end_page',
        help='По какую страницу качать',
        nargs='?',
        default='701',
        type=int
    )
    parser.add_argument(
        '-d',
        '--dest_folder',
        help='Название папки с результатами парсинга',
        nargs='?',
        default=pathlib.Path.cwd(),
    )
    args = parser.parse_args()

    start = args.start_page
    end = args.end_page
    dest_folder = args.dest_folder

    base_url = 'https://tululu.org'
    url_to_fantasy_books = 'https://tululu.org/l55/'
    url_with_text = 'https://tululu.org/txt.php'

    books = []

    for page in range(start, end + 1):
        url_to_each_page = urljoin(url_to_fantasy_books, str(page))
        response = requests.get(url_to_each_page)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        links_to_books = get_links_to_books(soup, base_url)
        for link in links_to_books:
            try:
                id = re.findall('\d+', link)[0]
                params = {'id': id}
                response = requests.get(link)
                response.raise_for_status()

                check_for_redirect(response)
                soup = BeautifulSoup(response.text, 'lxml')

                book = download_the_book(soup, link, url_with_text, params, dest_folder=dest_folder)

                books.append(book)

            except requests.TooManyRedirects:
                logger.warning(f'There is no data for one book ..')
                continue

            except requests.exceptions.HTTPError:
                logger.warning('Some errors on server.. Try again')
                continue

            except requests.exceptions.ConnectionError:

                logger.warning('Please check your internet connection')
                time.sleep(10)
    with open(os.path.join(dest_folder, 'books.json'), 'w') as file:
        json.dump(books, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
