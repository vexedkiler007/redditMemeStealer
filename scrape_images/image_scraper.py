from typing import Union
from bs4 import BeautifulSoup
from selenium import webdriver
from os.path import basename
import requests
import os


def _save_meme(link: Union[str, bytes], file_name: str) -> None:
    with open(file_name_ := f'Memes/{file_name}', 'wb') as file:
        img = requests.get(link)
        # 11074 is the animated png that has the highest number of bytes
        if int(img.headers['Content-Length']) > 11074:
            file.write(img.content)
        else:
            os.remove(file_name_)


def _extract_image(img: object) -> None:
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
        _save_meme(link, file_name)
    except KeyError as e:
        print(str(e) + " image")


def _extract_video(video: object) -> None:
    endings = ["mp4", "MP4",'gif']
    try:

        link = video.source['src']
        file_name = basename(link)
        file_name_list = file_name.split('.')
        if file_name_list[-1] not in endings:
            if "gif" in file_name_list[-1]:
                file_name_list[-1] = '.mp4'
                file_name = "".join(file_name_list)
        _save_meme(link, file_name)

    except KeyError as e:
        print(str(e) + " video")


def extract_all(container: object, list_search: list) -> None:
    for search_term in list_search:
        if search_term == 'img':
            for img in container.find_all(search_term):
                _extract_image(img)
        if search_term == 'video':
            for vid in container.find_all(search_term):
                _extract_video(vid)


def url_extract(driverlocation: str, url: str)-> None:
    """
    @:param driverlocation
    @:param url must be a reddit page url (not old)
    """

    # class="rpBJOHq2PR60pnwJlUyP0" the div where all of the data is located
    driver = webdriver.Chrome(driverlocation)
    driver.get(url)
    driver.find_element_by_class_name("rpBJOHq2PR60pnwJlUyP0")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    container = soup.find(class_="rpBJOHq2PR60pnwJlUyP0")
    extract_all(container, ['img', 'video'])
    driver.close()

if __name__ == '__main__':
    urls = ['https://www.reddit.com/r/dankmemes/', 'https://www.reddit.com/r/memes/']
    for url_ in urls:
        print(url_)
        url_extract("/home/newuser/PycharmProjects/redditMemeStealer/chromedriver", url=url_)