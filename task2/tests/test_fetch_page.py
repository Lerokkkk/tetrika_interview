import pytest
import asyncio
from task2.solution import fetch_page


@pytest.mark.asyncio
async def test_fetch_page():
    url = 'https://something_example.com'
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "formatversion": "2",
        "cmtitle": "Категория:Животные_по_алфавиту",
        "cmlimit": "max"
    }

    mock_response = {
        
    }

