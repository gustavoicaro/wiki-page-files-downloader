from argparse import ArgumentParser
from operator import itemgetter
import requests as req
import os

parser = ArgumentParser(description='Downloads all files from a specified wiki page.')
parser.add_argument('wiki', help='enter the wiki subdomain', type=str)
parser.add_argument('page', help='enter the wiki page to get the files', type=str)
parser.add_argument('-l', '--lang', help='enter the wiki language path', type=str, default='')
parser.add_argument('-r', '--replace', help='replace existing files if specified', action='store_true')
args = parser.parse_args()
wiki, page, lang, replace = itemgetter('wiki', 'page', 'lang', 'replace')(vars(args))

def get_json():
    url = f'https://{wiki}.fandom.com/{lang}/rest.php/v1/page/{page}/links/media'
    res = req.get(url)
    return res.json()

def get_files():
    files = get_json()['files']
    filtered_list = []
    for file in files:
        filtered_list.append({
            'name': file['title'],
            'url': file['original']['url']
        })
    return filtered_list

def download_files():
    wiki_dir = '.'.join([lang, wiki]) if lang else wiki
    file_dir = os.path.join('files', wiki_dir, page)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    for i in get_files():
        name, url = itemgetter('name', 'url')(i)
        res = req.get(url)
        file_path = os.path.join(file_dir, name)
        if os.path.exists(file_path) and not replace:
            print(f'{name} ⏭️')
            continue
        if res.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(res.content)
            print(f'{name} ✅')
        else:
            print(f'{name} ❌')

download_files()
