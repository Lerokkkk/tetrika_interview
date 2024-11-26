import json
import datetime

import requests


def fetch_data(params: dict):
    url = "https://ru.wikipedia.org/w/api.php"
    response = requests.get(url, params)
    return response.json()


def get_continue_page(data: dict[str: dict | str | int]):
    _continue = data.get('continue')
    if _continue:
        return _continue.get('cmcontinue')
    else:
        return None


def get_animals_title_from_query(query: dict):
    # for category_member in query.get('categorymembers'):
    #     title = category_member.get('title')
    #     yield title
    return [category_member.get('title') for category_member in query.get('categorymembers')]


def fetch_all_animals():
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "formatversion": "2",
        "cmtitle": "Категория:Животные_по_алфавиту",
        "cmlimit": "max"
    }
    for i in range(100):
        print(i)
        data = fetch_data(params)
        continue_page = get_continue_page(data)
        print(continue_page)
        query = data.get('query')
        yield from get_animals_title_from_query(query)

        if continue_page:
            params['cmcontinue'] = continue_page
        else:
            break


def app():
    for title in fetch_all_animals():
        pass
    

start = datetime.datetime.now()
with open('test.json', 'w', encoding='utf-8') as file:
    file.write('[\n')
    first = True
    for title in fetch_all_animals():
        if not first:
            file.write(', \n')
        else:
            first = False

        json.dump(title, file, ensure_ascii=False, indent=4)
    file.write('\n]')
finish = datetime.datetime.now()
print(finish - start)
