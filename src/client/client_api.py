import json
import aiohttp


async def post(url: str, payload: dict) -> (int, str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=payload) as resp:
            content = await resp.read()
            status = resp.status
            if 200 <= status < 300:
                return json.loads(content)
            else:
                raise Exception(f"POST Request failed. status code: {status}, payload content: {content}")


async def get(url: str, headers: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            content = await resp.read()
            status = resp.status
            if 200 <= status < 300:
                return json.loads(content)
            else:
                raise Exception(f"GET Request failed. status code: {status}, payload content: {content}")

