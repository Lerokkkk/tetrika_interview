import csv
from collections import Counter

import aiohttp
import aiofiles
import asyncio
import json
import datetime


async def fetch_page(session, url, params):
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


def get_next_page(data: dict):
    _continue = data.get('continue', None)
    if _continue:
        return _continue.get('cmcontinue', None)
    return _continue


def get_titles(data):
    query = data.get('query')
    return [category_member.get('title') for category_member in query.get('categorymembers')]


async def fetch_and_yield(session, url, start_params):
    params = start_params
    while True:
        data = await fetch_page(session, url, params)
        titles, next_page = get_titles(data), get_next_page(data)
        for title in titles:
            yield title

        if not next_page:
            break
        params["cmcontinue"] = next_page


def get_russian_letters():
    rus_letters = {chr(i) for i in range(1040, 1072)}
    rus_letters.add(chr(1025))
    return rus_letters


async def save_to_json(file_path, generator):
    letter_count = dict()
    letters = get_russian_letters()

    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        first = True
        await f.write('[')
        async for title in generator:
            if ":" in title:
                continue

            first_letter = title[0].upper()
            if first_letter in letters:
                letter_count[first_letter] = letter_count.setdefault(first_letter, 0) + 1

            if not first:
                await f.write(',\n')
            first = False
            await f.write(json.dumps(title, indent=4, ensure_ascii=False))
        await f.write(']')
    return letter_count


def save_to_csv(file_path, data_dict):
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Буква', 'Количество'])

        for key, value in data_dict.items():
            writer.writerow([key, value])


async def main():
    url = "https://ru.wikipedia.org/w/api.php"
    start_params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "formatversion": "2",
        "cmtitle": "Категория:Животные_по_алфавиту",
        "cmlimit": "max"
    }

    async with aiohttp.ClientSession() as session:
        generator = fetch_and_yield(session, url, start_params)
        letters = await save_to_json("titles.json", generator)

    save_to_csv("beasts.csv", letters)


if __name__ == "__main__":
    asyncio.run(main())
