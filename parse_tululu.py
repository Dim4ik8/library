import requests
from functions import parse_book_page
from bs4 import BeautifulSoup
from functions import check_for_redirect
import argparse


def main():

    parser = argparse.ArgumentParser(
        description='Парсим библиотеку'
    )
    parser.add_argument('-s', '--start_id', help='С какой страницы качать', nargs='?', default='1', type=int)
    parser.add_argument('-e', '--end_id', help='По какую страницу качать', nargs='?', default='10', type=int)
    args = parser.parse_args()

    start = args.start_id
    end = args.end_id

    main_url = "https://tululu.org/"
    book_url = "https://tululu.org/txt.php"
    book_start_url = 'https://tululu.org/b'

    for count in range(start, end):

        url = f'{book_start_url}{str(count)}/'
        response = requests.get(url)
        response.raise_for_status()

        try:
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')

            book_info = parse_book_page(soup)
            print('Заголовок: ', book_info['title'])
            print('Автор: ', book_info['author'])
            print('Жанр: ', book_info['genres'])
            print('='*120)


            # title_tag = soup.find('h1')
            # filename = title_tag.text.split('::')[0].strip()
            # image = soup.find('div', class_='bookimage').find('img')['src']
            # image_url = urljoin(main_url, image)
            # image_title = image.split('/')[-1]

            # comments = soup.find_all('div', class_='texts')
            # com = [comment.find('span', class_='black') for comment in comments]
            # print(filename)
            # for text in com:
            #     print(text.text)


            # genres = [genre.text for genre in soup.find('span', class_='d_book').find_all('a')]
            # print(genres)
            # print('=' * 120)

        except requests.TooManyRedirects:
            continue


if __name__ == '__main__':
    main()
