import re
import requests as r
import os

pattern = r'^[a-z]{2}(-[a-z]{2})?\.[a-z]+$'

lang = '/'
wiki = input('wiki: ')
page = input('page: ')

if re.match(pattern, wiki):
    wiki = wiki.split('.')
    lang += wiki[0]
    wiki = wiki[1]

url = f'https://{wiki}.fandom.com{lang}/rest.php/v1/page/{page}/links/media'

response = r.get(url)
json = response.json()
files = [{'title': file['title'], 'url': file['original']['url']} for file in json['files']]

file_dir = os.path.join('files', '.'.join([lang[1:], wiki]), page)
if not os.path.exists(file_dir):
    os.makedirs(file_dir)

for file in files:
    response = r.get(file['url'])
    file_name = os.path.join(file_dir, file['title'])
    if response.status_code == 200:
        with open(file_name, 'wb') as file_:
            file_.write(response.content)
        print(f'{file["title"]} ✅')
    else:
        print(f'{file["title"]} ❌')
