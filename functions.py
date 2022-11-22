import requests
import os
from pathvalidate import sanitize_filename
from pathlib import Path


def check_for_redirect(response):
    if response.history:
        raise requests.TooManyRedirects


def download_txt(url, filename, folder='books/', params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    check_for_redirect(response)
    filename = sanitize_filename(filename)
    Path(folder).mkdir(exist_ok=True)
    with open(f'{os.path.join(folder, filename)}.txt', 'w', encoding='UTF-8') as file:
        file.write(response.text)
    return (f'{os.path.join(folder, filename)}.txt')


def download_image(url, filename, folder='images'):
    response = requests.get(url)
    response.raise_for_status()
    Path(folder).mkdir(exist_ok=True)
    with open(f'{os.path.join(folder, filename)}', 'wb') as file:
        file.write(response.content)


def parse_book_page(soup):
    title_tag = soup.find('h1')
    title, author = title_tag.text.split(' :: ')
    comments = soup.find_all('div', class_='texts')

    book = {
        'title': title.strip(),
        'author': author.strip(),
        'genres': [genre.text for genre in soup.find('span', class_='d_book').find_all('a')],
        'comments': [comment.find('span', class_='black').text for comment in comments]
    }

    return book


def main():
    url_book = 'http://tululu.org/txt.php?id=1'
    print(download_txt(url_book, 'Алиби'))

    print(download_txt(url_book, 'Али/би', folder='books/'))

    print(download_txt(url_book, 'Али\\би', folder='txt/'))


if __name__ == '__main__':
    main()
