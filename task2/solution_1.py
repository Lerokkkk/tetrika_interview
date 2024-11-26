import datetime
import json

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
    response_data = list()
    for category_member in query.get('categorymembers'):
        response_data.append(category_member.get('title'))
    return response_data


def fetch_all_animals():
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "formatversion": "2",
        "cmtitle": "Категория:Животные_по_алфавиту",
        "cmlimit": "max"
    }
    all_data = list()
    for i in range(100):
        print(i)
        data = fetch_data(params)
        query = data.get('query')
        all_data.extend(get_animals_title_from_query(query))
        continue_page = get_continue_page(data)
        print(continue_page)

        if continue_page:
            params['cmcontinue'] = continue_page
        else:
            break
    return all_data


start = datetime.datetime.now()
response = fetch_all_animals()
with open('test.json', 'w', encoding='utf-8') as file:
    json.dump(response, file, ensure_ascii=False, indent=4)
finish = datetime.datetime.now()
print(finish - start)
