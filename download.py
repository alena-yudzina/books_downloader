import requests
from pathlib import Path


Path('books').mkdir(parents=True, exist_ok=True)

for i in range(1, 11):
    url = 'https://tululu.org/txt.php?id={}'.format(i)
    response = requests.get(url)
    response.raise_for_status() 
    filename = 'id{}.txt'.format(i)
    with open(Path('books') / filename, 'wb') as file:
        file.write(response.content)
