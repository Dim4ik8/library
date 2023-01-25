import json
import math
import os
import pathlib
from pprint import pprint

from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


json_path = find('books.json', pathlib.Path.cwd())

with open(json_path, 'r') as file:
    books = json.load(file)

by_10_books_on_page = list(chunked(books, 10))


os.makedirs('pages', exist_ok=True)


for count, books in enumerate(by_10_books_on_page):
    num_of_page = count + 1
    books_for_two_columns = list(chunked(books, 2))

    page_title = f'index{num_of_page}.html'
    template = env.get_template('template.html')
    rendered_page = template.render(
        books=books_for_two_columns,
        total_pages=len(by_10_books_on_page),
        current_page=count + 1,
    )

    for two_books in books_for_two_columns:
        print(two_books[0]['img_src'])
        print('='*50)

    with open(f'pages/{page_title}', 'w', encoding="utf8") as file:
        file.write(rendered_page)




    # def on_reload():
    #     template = env.get_template('template.html')
    #     rendered_page = template.render(
    #         books=books,
    #     )
    #     with open(f'pages/{page_title}', 'w', encoding="utf8") as file:
    #         file.write(rendered_page)
    #
    #     print("Site rebuiled")
    #
    #
    # on_reload()

# server = Server()
#
# server.watch('template.html', on_reload)
#
# server.serve(root='.')
