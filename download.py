import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urlparse, urlsplit, urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, filename, folder='books/'):

    response = requests.get(url)
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return
    response.raise_for_status()
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = '{}.txt'.format(sanitize_filename(filename))
    with open(Path(folder) / filename, 'wb') as file:
        file.write(response.content)
    filepath = Path(folder) / filename
    
    return filepath


def download_image(url, folder='images'):

    response = requests.get(url)
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return
    response.raise_for_status()
    Path(folder).mkdir(parents=True, exist_ok=True)
    url_path = urlparse(url).path
    filename = url_path.rsplit('/', 1)[-1]
    filename = sanitize_filename(filename)
    with open(Path(folder) / filename, 'wb') as file:
        file.write(response.content)
    filepath = Path(folder) / filename
    
    return filepath

for i in range(1, 11):
    url = 'https://tululu.org/b{}/'.format(i)
    response = requests.get(url)
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        continue
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    info_text = soup.find('h1').text
    filename = info_text.split('::')[0].strip()
    img_url = soup.find(class_='bookimage').find('img')['src']
    img_abs_url = urljoin(url, img_url)
    print('Заголовок:', filename)
    print()

    comments = soup.find_all('div', class_='texts')
    for comment in comments:
        comment_text = comment.find('span', class_='black').text
        print(comment_text)


    '''info_text = soup.find('h1').text
    filename = info_text.split('::')[0].strip()

    img_url = soup.find(class_='bookimage').find('img')['src']
    img_abs_url = urljoin(url, img_url)

    print('Заголовок:', filename)
    print(img_abs_url)
    print(download_image(img_abs_url))
    print()'''

    '''url = 'https://tululu.org/txt.php?id={}'.format(i)
    download_txt(url, filename=filename)'''
