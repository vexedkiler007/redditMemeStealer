import asyncio
import os
import aiohttp
from aiofile import AIOFile
from bs4 import BeautifulSoup
import random
from arsenic import get_session, keys, browsers, services


def check_file_exist(file_name):
    path = f'Memes/{file_name}'
    return os.path.isfile(path)


def is_meme(response_header_length, img_size=15_000):
    # 15,000 refers to the size of the file since memes tend to be larger pictures
    return int(response_header_length) > img_size


async def save_meme(link, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if is_meme(response.headers['Content-Length']):
                async with AIOFile(f'Memes/{file_name}', 'wb') as afp:
                    await afp.write(await response.read())
                    await afp.fsync()


async def extract_image(img: object):
    endings = ['jpg', 'png']
    try:
        link = img['src']
        file_name = os.path.basename(link)
        file_name_list = file_name.split('.')
        if file_name_list[-1] not in endings:
            if 'png' in file_name_list[-1]:
                file_name_list[-1] = '.png'
                file_name = "".join(file_name_list)
            if 'jpg' in file_name_list[-1]:
                file_name_list[-1] = '.jpg'
                file_name = "".join(file_name_list)
        if not check_file_exist(file_name):
            await save_meme(link, file_name)
        else:
            print("Already Exists")
    except KeyError as e:
        print(str(e) + " image")


async def extract_images_video(source):
    soup = BeautifulSoup(source, 'html.parser')
    container = soup.find(class_="rpBJOHq2PR60pnwJlUyP0")
    for img in container.find_all('img'):
        await extract_image(img)


async def create_source_selenium(url: str, proxy_list: list = None):
    service = services.Chromedriver(binary="./chromedriver")
    if proxy_list is not None:
        browser = browsers.Chrome(chromeOptions={
            'args': ['--headless', f"--proxy-server={random.choice(proxy_list)}"]
        })
    else:
        browser = browsers.Chrome(chromeOptions={'args': ['--headless']})
    async with get_session(service, browser) as session:
        await session.get(url)
        return await session.get_page_source()


async def gather(url_list: list, proxy_list=None):
    coro_list = []
    for url in url_list:
        source = await create_source_selenium(url, proxy_list)
        coro_list.append(extract_images_video(source))
    await asyncio.gather(*coro_list)


def main():
    urls = ["https://www.reddit.com/", "https://www.reddit.com/r/dankmemes/", 'https://www.reddit.com/r/memes/']
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather(urls))


if __name__ == '__main__':
    main()
