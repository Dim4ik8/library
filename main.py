import requests
from bs4_tutorial import download_image
from bs4 import BeautifulSoup
from bs4_tutorial import check_for_redirect
from urllib.parse import urljoin


def main():
    main_url = "https://tululu.org/"
    book_url = "https://tululu.org/txt.php"
    book_start_url = 'https://tululu.org/b'

    for count in range(10):
        params = {'id': count + 1}
        url = book_start_url + str(count + 1) + '/'
        response = requests.get(url)
        response.raise_for_status()

        try:
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.find('h1')
            filename = title_tag.text.split('::')[0].strip()
            image = soup.find('div', class_='bookimage').find('img')['src']
            image_url = urljoin(main_url, image)
            image_title = image.split('/')[-1]

            download_image(image_url, image_title)

        except requests.TooManyRedirects:
            continue


if __name__ == '__main__':
    main()
