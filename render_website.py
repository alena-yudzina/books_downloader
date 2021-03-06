import json
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open("fantasy_books_info.json", "r") as file:
        books = json.load(file)
    books_per_page = 10
    books_pages = list(chunked(books, books_per_page))
    pages_amount = len(books_pages)
    Path('pages').mkdir(parents=True, exist_ok=True)

    for page_num, books in enumerate(books_pages, start=1):
        books_rows = list(chunked(books, 2))
        rendered_page = template.render(books_rows=books_rows, pages_amount=pages_amount, page_num=page_num)
        with open('pages/index{}.html'.format(page_num), 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
