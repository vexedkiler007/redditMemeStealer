import asyncio
from os.path import basename
from typing import Awaitable, Coroutine
import aiohttp
from aiofile import AIOFile
from bs4 import BeautifulSoup

from arsenic import get_session, keys, browsers, services


async def save_meme(link, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if int(response.headers['Content-Length']) > 15_000:
                async with AIOFile(f'Memes/{file_name}', 'wb') as afp:
                    await afp.write(await response.read())
                    await afp.fsync()


async def extract_image(img: object):
    endings = ['jpg', 'png']
    try:
        link = img['src']
        file_name = basename(link)
        file_name_list = file_name.split('.')
        if file_name_list[-1] not in endings:
            if 'png' in file_name_list[-1]:
                file_name_list[-1] = '.png'
                file_name = "".join(file_name_list)
            if 'jpg' in file_name_list[-1]:
                file_name_list[-1] = '.jpg'
                file_name = "".join(file_name_list)
        await save_meme(link, file_name)
    except KeyError as e:
        print(str(e) + " image")


async def extract_images_video():
    """
    """
    # --proxy-server=167.99.230.196:3128
    # '--headless'
    service = services.Chromedriver(binary="./chromedriver")
    browser = browsers.Chrome(chromeOptions={
        'args': ['--headless']
    })

    async with get_session(service, browser) as session:
        await session.get('https://www.reddit.com/')
        source = await session.get_page_source()
        soup = BeautifulSoup(source, 'html.parser')
        container = soup.find(class_="rpBJOHq2PR60pnwJlUyP0")
        for img in container.find_all('img'):
            await extract_image(img)


async def gather():
    coro_list = []
    for _ in range(0, 2):
        coro_list.append(extract_images_video())
    await asyncio.gather(*coro_list)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather())


if __name__ == '__main__':
    main()
