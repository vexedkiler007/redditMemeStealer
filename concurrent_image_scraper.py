import asyncio


from arsenic import get_session, keys, browsers, services


async def hello_word():
    """
    """
    service = services.Chromedriver(binary="./chromedriver")
    browser = browsers.Chrome(chromeOptions={
        #'args': ['--proxy-server=167.99.230.196:3128']
    })
    print("yolo")
    async with get_session(service, browser) as session:
        await session.get('https://www.reddit.com/')
        # search_box = await session.wait_for_element(5, 'input[name=q]')
        # await search_box.send_keys("Cats")
        # await search_box.send_keys(keys.ENTER)
        await asyncio.sleep(100)

async def gather():
    coro_list = []
    for _ in range(0,10):
        coro_list.append(hello_word())
    await asyncio.gather(*coro_list)

def main():

    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather())
    print("yolo")


if __name__ == '__main__':
    main()
