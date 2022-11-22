import time
from urllib.parse import urljoin

import requests
from functions import parse_book_page
from bs4 import BeautifulSoup
from functions import check_for_redirect, download_image
import argparse


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
    url_with_image = "https://tululu.org/b1/"

    for count in range(start, end):

        try:
            url = f'{book_start_url}{str(count)}/'
            response = requests.get(url)
            response.raise_for_status()

            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')

            book = parse_book_page(soup)
            print(book)

            image = soup.find('div', class_='bookimage').find('img')['src']
            image_url = urljoin(url_with_image, image)
            image_title = image.split('/')[-1]
            print(image)
            print(image_url)
            download_image(image_url, image_title)


            time.sleep(1)
        except requests.TooManyRedirects:
            continue

        except requests.exceptions.HTTPError:
            print('Some errors on server.. Try again')

        except requests.exceptions.ConnectionError:
            print('Please check your internet connection')
            time.sleep(10)


if __name__ == '__main__':
    main()
