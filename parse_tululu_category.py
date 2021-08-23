import argparse
import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from download import (check_for_redirect, download_image, download_txt,
                      parse_book_page)


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Download fantasy books')
    parser.add_argument(
        '--start_page',
        help='set start page',
        type=int,
        default=1
    )
    parser.add_argument(
        '--end_page',
        help='set end page',
        type=int,
        default=701
    )
    parser.add_argument(
        '--dest_folder',
        help='set folder to download',
        type=str,
        default='.'
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Булевое значение True или False'
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Булевое значение True или False'
    )
    parser.add_argument(
        '--json_path',
        help='set path to json with info',
        type=str,
        default='.'
    )
    args = parser.parse_args()

    return args


def fantasy_urls(start, end):
    fantasy_book_ids = []
    for page_id in range(start, end):
        url = 'https://tululu.org/l55/{}'.format(page_id)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        book_hrefs = [tag['href'] for tag in soup.select('.d_book .bookimage a')]
        book_ids = [book_href[2:] for book_href in book_hrefs]
        fantasy_book_ids.extend(book_ids)
    return fantasy_book_ids


def download_category():
    args = parse_cli_args()
    book_ids = fantasy_urls(args.start_page, args.end_page)
    books_info = []
    for book_id in book_ids:
        url = 'https://tululu.org/b{}'.format(book_id)
        response = requests.get(url)
        try:
            check_for_redirect(response)
            response.raise_for_status()
        except requests.HTTPError:
            continue

        book_info = parse_book_page(response.text)
        img_url = urljoin(url, book_info['img_url'])
        book_url = 'https://tululu.org/txt.php'
        payload = {'id': book_id}
        try:
            if not args.skip_txt:
                book_info['book_path'] = str(download_txt(
                    book_url,
                    payload,
                    filename=book_info['title'],
                    folder=Path(args.dest_folder, 'books')
                ))
            if not args.skip_imgs:
                download_image(
                    img_url,
                    folder=Path(args.dest_folder, 'images')
                )
            books_info.append(book_info)
        except requests.HTTPError:
            print('Unable to download book')
    
    json_path =  args.json_path if args.json_path != '.' else args.dest_folder
    with open(Path(json_path, 'fantasy_books_info.json'), mode="a") as file:
        json.dump(books_info, file, ensure_ascii=False, indent=4)


download_category()
