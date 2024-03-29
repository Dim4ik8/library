import json
import time

import requests
from bs4 import BeautifulSoup
import logging
import re
from functions import check_for_redirect, get_links_to_books, \
    parse_book_page, download_txt, download_image
from urllib.parse import urljoin
import argparse
import os
from pathlib import Path

logger = logging.getLogger()

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
    default='10',
    type=int
)
parser.add_argument(
    '-d',
    '--dest_folder',
    help='Название папки с результатами парсинга',
    nargs='?',
    default='',
)
parser.add_argument(
    '--skip_imgs',
    action='store_true',
    help='Не скачивать картинки',

)
parser.add_argument(
    '--skip_text',
    action='store_true',
    help='Не скачивать книги',
)
parser.add_argument(
    '-j',
    '--json_folder',
    help='Путь к файлу с данными',
    nargs='?',
    default='media',
)
args = parser.parse_args()

start = args.start_page
end = args.end_page
dest_folder = args.dest_folder
skip_imgs = args.skip_imgs
skip_text = args.skip_text
json_folder = args.json_folder


def main():
    base_url = 'https://tululu.org'
    url_to_fantasy_books = 'https://tululu.org/l55/'
    url_with_text = 'https://tululu.org/txt.php'

    books = []
    for page_number in range(start, end + 1):
        try:
            url_to_each_page = urljoin(url_to_fantasy_books, str(page_number))
            response = requests.get(url_to_each_page)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            links_to_books = get_links_to_books(soup, base_url)
            for link in links_to_books:
                try:
                    response = requests.get(link)
                    response.raise_for_status()
                    check_for_redirect(response)
                    soup = BeautifulSoup(response.text, 'lxml')

                    book_id = re.findall(r'\d+', link)[0]
                    params = {'id': book_id}
                    image_tag = soup.select_one('.bookimage img')
                    image = image_tag['src']
                    image_url = urljoin(link, image)
                    image_title = image.split('/')[-1]

                    book_params = parse_book_page(soup)

                    if not skip_imgs:
                        image = download_image(
                            image_url,
                            image_title,
                            dest_folder=dest_folder
                        )

                    if not skip_text:
                        text = download_txt(
                            url_with_text,
                            book_params['title'],
                            dest_folder=dest_folder,
                            params=params
                        )

                    book = book_params | image | text

                    books.append(book)
                except requests.TooManyRedirects:
                    logger.warning('There is no data for one book ..')
                    continue

                except requests.exceptions.HTTPError:
                    logger.warning('Some errors on server.. Try again')
                    continue

                except requests.exceptions.ConnectionError:
                    logger.warning('Please check your internet connection')
                    time.sleep(10)

        except requests.TooManyRedirects:
            logger.warning('There is no data for one book ..')
            continue

        except requests.exceptions.HTTPError:
            logger.warning('Some errors on server.. Try again')
            continue

        except requests.exceptions.ConnectionError:
            logger.warning('Please check your internet connection')
            time.sleep(10)

    Path(json_folder).mkdir(exist_ok=True)
    with open(os.path.join(json_folder, 'books.json'), 'w') as file:
        json.dump(books, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
