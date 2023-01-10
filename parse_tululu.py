import time
from urllib.parse import urljoin
import logging
import requests
from bs4 import BeautifulSoup
from functions import check_for_redirect, download_image, download_txt, parse_book_page
import argparse

logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(
        description='Парсим библиотеку'
    )
    parser.add_argument(
        '-s', '--start_id',
        help='С какой страницы качать',
        nargs='?',
        default='1',
        type=int
    )
    parser.add_argument(
        '-e',
        '--end_id',
        help='По какую страницу качать',
        nargs='?',
        default='10',
        type=int
    )
    args = parser.parse_args()

    start = args.start_id
    end = args.end_id

    book_start_url = 'https://tululu.org/b'
    url_with_text = 'https://tululu.org/txt.php'
    for count in range(start, end):
        params = {'id': count}
        try:
            url = f'{book_start_url}{str(count)}/'

            response = requests.get(url)
            response.raise_for_status()

            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')

            book = parse_book_page(soup)

            image_url = urljoin(url, book['image'])
            image_title = book['image'].split('/')[-1]

            download_image(image_url, image_title)

            download_txt(url_with_text, book['title'], params=params)

        except requests.TooManyRedirects:
            logger.warning(f'There is no data for book number {count}..')
            continue

        except requests.exceptions.HTTPError:
            logger.warning('Some errors on server.. Try again')
            continue

        except requests.exceptions.ConnectionError:

            logger.warning('Please check your internet connection')
            time.sleep(10)


if __name__ == '__main__':
    main()
