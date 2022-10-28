import requests
from pathlib import Path

def check_for_redirect(response):
    if response.history:
        raise requests.TooManyRedirects


def main():
    book_url = "https://tululu.org/txt.php"

    Path("books").mkdir(exist_ok=True)

    for count in range(10):
        params = {'id': count + 1}
        response = requests.get(book_url, params=params)
        response.raise_for_status()

        try:
            check_for_redirect(response)
            filename = Path.cwd() / 'books' / f'id{count+1}.txt'
            with open(filename, 'w', encoding='UTF-8') as file:
                file.write(response.text)
        except requests.TooManyRedirects:
            continue


if __name__ == '__main__':
    main()
