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

    main_url = "https://tululu.org/"
    book_start_url = 'https://tululu.org/b'

    for count in range(start, end):

        try:
            url = f'{book_start_url}{str(count)}/'
            response = requests.get(url)
            response.raise_for_status()

            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')

            book = parse_book_page(soup)
            print(book)

            print(book)
            print('======================')

            print('Заголовок: ', book['title'])
            print('Автор: ', book['author'])
            print('Жанр: ', book['genres'])
            print('=' * 120)

            image = soup.find('div', class_='bookimage').find('img')['src']
            image_url = urljoin(main_url, image)
            image_title = image.split('/')[-1]
            print(image_url)
            download_image(image_url, image_title)

            comments = soup.find_all('div', class_='texts')
            com = [comment.find('span', class_='black') for comment in comments]
            for text in com:
                print(text.text)

            genres = [genre.text for genre in soup.find('span', class_='d_book').find_all('a')]
            print(genres)
            print('=' * 120)

            time.sleep(5)
        except requests.TooManyRedirects:
            continue

        except requests.exceptions.HTTPError:
            print('Some errors on server.. Try again')

        except requests.exceptions.ConnectionError:
            print('Please check your internet connection')
            time.sleep(10)


if __name__ == '__main__':
    main()
