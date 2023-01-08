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
    links_to_books = [urljoin(base_url, book.select_one('a')['href']) for book in books]
    return links_to_books

def download_txt(url, filename, folder='books/', dest_folder='', params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    check_for_redirect(response)
    filename = sanitize_filename(filename)
    Path(os.path.join(f'{dest_folder}/{folder}')).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(dest_folder, folder, f'{filename}.txt')
    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(response.text)
    return file_path


def download_image(url, filename, folder='images', dest_folder=''):
    response = requests.get(url)
    response.raise_for_status()
    Path(os.path.join(f'{dest_folder}/{folder}')).mkdir(parents=True, exist_ok=True)
    with open(f'{os.path.join(dest_folder, folder, filename)}', 'wb') as file:
        file.write(response.content)


def parse_book_page(soup):
    author_and_title_tag = soup.select_one("div[id='content'] h1")
    title, author = author_and_title_tag.text.split('::')
    comments_tags = soup.select('.texts')
    genre_tags = soup.select('span.d_book a')
    image_tag = soup.select_one('.bookimage img')

    book = {
        'title': title.strip(),
        'author': author.strip(),
        'genres': [tag.text for tag in genre_tags],
        'comments': [tag.span.text for tag in comments_tags],
        'image': image_tag['src']
    }

    return book

def download_the_book(soup, link_to_book, url_with_text, params, skip_imgs, dest_folder=''):
    author_and_title_tag = soup.select_one("div[id='content'] h1")
    title, author = author_and_title_tag.text.split('::')
    comments_tags = soup.select('.texts')
    genre_tags = soup.select('span.d_book a')
    image_tag = soup.select_one('.bookimage img')
    image = image_tag['src']

    image_url = urljoin(link_to_book, image)
    image_title = image.split('/')[-1]
    if not skip_imgs:
        download_image(image_url, image_title, dest_folder=dest_folder)
    download_txt(url_with_text, title.strip(), dest_folder=dest_folder, params=params)

    book = {
        'title': title.strip(),
        'author': author.strip(),
        'img_src': os.path.join('images', image_title),
        'book_path': os.path.join('books', f'{title.strip()}.txt'),
        'genres': [tag.text for tag in genre_tags],
        'comments': [tag.span.text for tag in comments_tags],
    }

    return book
def main():
    url_book = 'http://tululu.org/txt.php?id=1'
    print(download_txt(url_book, 'Алиби'))

    print(download_txt(url_book, 'Али/би', folder='books/'))

    print(download_txt(url_book, 'Али\\би', folder='txt/'))


if __name__ == '__main__':
    main()
