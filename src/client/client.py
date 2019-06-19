import aiohttp


async def post(url: str, payload: dict) -> (int, str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            content = await resp.read()
            status = resp.status
            return status, content


async def get(url: str) -> (int, str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            status = resp.status
            return status, content

