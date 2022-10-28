import requests

def main():
    book_url = "https://tululu.org/txt.php?id=32168"

    response = requests.get(book_url, verify=False)
    response.raise_for_status()

    filename = 'mars.txt'
    with open(filename, 'w', encoding='UTF-8') as file:
        file.write(response.text)


if __name__ == '__main__':
    main()