#!

import pyautogui
from time import sleep
import pyperclip
import requests
import bs4
import re

test_file = 'news.txt'
news_site_root = '***'
news_site = '***'
news_link = ''
news_article = ''


def news_search():

    global news_link

    res = requests.get(news_site)
    try:
        res.raise_for_status()
    except Exception as exc:
        print(f'There was a problem in connection: {exc}')

    if res.status_code != requests.codes.ok:
        print(f'Request code: {res.status_code}, NG')
        return

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    date_tag = soup.select('.post-list__date')

    news_tag = date_tag[0].find_parent("div").find_next_sibling("div")

    news_link = news_site_root + news_tag.find('a').get('href')


def news_copy():

    global news_article

    if news_link is None:
        return

    res = requests.get(news_link)
    try:
        res.raise_for_status()
    except Exception as exc:
        print(f'There was a problem in connection: {exc}')

    if res.status_code != requests.codes.ok:
        print(f'Request code: {res.status_code}, NG')
        return

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    post = soup.select('.post__body')

    news_article = ''

    for posts in post:
        news_article += posts.getText()

    news_article = re.sub(' +', ' ', news_article)
    news_article = re.sub('\n+', '\n', news_article)


def post_switch():
    pass


def fake_typewriter():

    for c in news_article:
        if c == '\n':
            pyautogui.press('enter')
            pass
        elif not c:
            break
        else:
            pyperclip.copy(c)
            pyautogui.keyDown('alt')
            pyautogui.keyDown('p')
            pyautogui.keyUp('p')
            pyautogui.keyUp('alt')
            sleep(5)

    """
    with open(test_file, 'r', encoding="utf-8") as f:
        while True:
            c = f.read(1)
            if c == '\n':
                pyautogui.press('enter')
                pass
            elif not c:
                break
            else:
                pyperclip.copy(c)
                pyautogui.keyDown('alt')
                pyautogui.keyDown('p')
                pyautogui.keyUp('p')
                pyautogui.keyUp('alt')
                sleep(5)
    """


if __name__ == '__main__':
    sleep(5)
    news_search()
    news_copy()
    post_switch()
    fake_typewriter()



