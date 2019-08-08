import json
import logging

import aiohttp


async def post(url: str, payload: dict) -> (int, str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=payload) as resp:
            content = await resp.read()
            if 200 <= resp.status < 300:
                json_content = json.loads(content)
                return json_content
            else:
                logging.error(f"POST Request failed. status code: {resp.status}, payload content: {content}")
                raise Exception(f"POST Request failed. status code: {resp.status}, payload content: {content}")


async def get(url: str, headers: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            content = await resp.read()
            if 200 <= resp.status < 300:
                json_content = json.loads(content)
                return json_content
            else:
                logging.error(f"GET Request failed. status code: {resp.status}, payload content: {content}")
                raise Exception(f"GET Request failed. status code: {resp.status}, payload content: {content}")


