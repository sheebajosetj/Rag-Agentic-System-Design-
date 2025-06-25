# fetch_data/downloader.py
import aiohttp
from datetime import date
from typing import List

BASE_URL = "https://www.federalregister.gov/api/v1/documents.json"

async def fetch_documents(start_date: str, end_date: str) -> List[dict]:
    params = {
        "per_page": 1000,
        "order": "newest",
        "conditions[publication_date][gte]": start_date,
        "conditions[publication_date][lte]": end_date
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch data: {response.status}")
            data = await response.json()
            return data.get("results", [])
