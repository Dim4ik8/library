import json
import os
from pathlib import Path

from more_itertools import chunked
from parse_tululu_category import args
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

def on_reload():
    json_path = os.path.join(args.json_folder, 'books.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        books_descriptions = json.load(file)

    book_cards_per_page = 10
    book_cards_on_page = list(chunked(books_descriptions, book_cards_per_page))

    for page, books in enumerate(book_cards_on_page, start=1):
        page_title = f'index{page}.html'
        template = env.get_template('template.html')
        rendered_page = template.render(
            books_catalog=books,
            total_pages=len(book_cards_on_page),
            current_page=page,
        )
        with open(f'pages/{page_title}', 'w', encoding='utf8') as file:
            file.write(rendered_page)
    print('Site rebuild')


def main():

    Path('pages').mkdir(exist_ok=True)

    on_reload()

    server = Server()
    server.watch('template.html', on_reload())
    server.serve(root='.')


if __name__ == '__main__':
    main()
