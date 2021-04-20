#!

import pyautogui
import pyperclip
import requests
import bs4
import re
import subprocess
import win32gui
import win32con
import shelve
from time import sleep

test_file = 'news.txt'

news_site_root = '***'
news_site = '***'
news_link = ''
news_title = ''
news_article = ''

post_app = '***'
post_site = '***'
post_user = '***'
post_pwd = '***'
post_clear_default_lines = 10
post_line_max_width = 50

post_condition = {
    'double_connect': './asset/double_connection.png',
    'article_exists': './asset/article_exists.png'
}


def get_digit_list(s_in):
    s_temp = ''
    s_new = []

    for s in s_in:
        if s.isdigit():
            s_temp += s
        else:
            if s_temp != '':
                s_new.append(int(s_temp))
            s_temp = ''
    return s_new


def news_search():

    global news_link, news_title

    res = requests.get(news_site)
    try:
        res.raise_for_status()
    except Exception as exc:
        print(f'news_search error: problem in connection: {exc}')
        return False

    if res.status_code != requests.codes.ok:
        print(f'news_search error: request code: {res.status_code}')
        return False

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get News Date
    date_tag = soup.select('.post-list__date')
    news_date = get_digit_list(str(date_tag[0].getText()))
    # print(news_date)

    # Check if News have been posted
    shelve_file = shelve.open('news_date_log')

    try:
        latest_date = shelve_file['latest_date']
        if news_date > latest_date:
            shelve_file['latest_date'] = news_date
        else:
            print(f'news_search info: no updated news')
            shelve_file.close()
            return False
    except KeyError:
        shelve_file['latest_date'] = news_date

    shelve_file.close()

    # Get News Link
    news_tag = date_tag[0].find_parent("div").find_next_sibling("div")

    news_link = news_site_root + news_tag.find('a').get('href')

    # Get News Title
    news_title = news_tag.find('a').getText()

    return True


def news_copy():

    global news_article

    if news_link is None:
        return False

    res = requests.get(news_link)
    try:
        res.raise_for_status()
    except Exception as exc:
        print(f'news_copy error: problem in connection: {exc}')
        return False

    if res.status_code != requests.codes.ok:
        print(f'news_copy error: request code: {res.status_code}')
        return False

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    post = soup.select('.post__body')

    news_article = ''

    for posts in post:
        news_article += posts.getText()

    news_article = re.sub(' +', ' ', news_article)
    news_article = re.sub('\n+', '\n', news_article)

    # print(news_article)

    return True


def post_switch(board_order, post_type):

    # Launch App
    subprocess.Popen([post_app])

    sleep(5)

    # Maximize Window
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    # Connection Interface
    pyautogui.keyDown('alt')
    pyautogui.keyDown('q')
    pyautogui.keyUp('q')
    pyautogui.keyUp('alt')
    sleep(1)

    # Enter Site Address
    pyautogui.typewrite(post_site)
    pyautogui.press('enter')
    sleep(5)

    # Enter User Name
    pyautogui.typewrite(post_user)
    pyautogui.press('enter')
    sleep(3)

    # Enter User Password
    pyautogui.typewrite(post_pwd)
    pyautogui.press('enter')
    sleep(3)

    # Check if double connection
    try:
        pyautogui.locateOnScreen(post_condition['double_connect'], confidence=0.9)
        pyautogui.typewrite('y')
        sleep(1)
        pyautogui.press('enter')
        sleep(10)
    except ImageNotFoundException:
        pass

    pyautogui.press('enter')
    sleep(5)

    # Check if article exists
    try:
        pyautogui.locateOnScreen(post_condition['article_exists'], confidence=0.9)
        pyautogui.typewrite('Q')
        sleep(1)
        pyautogui.press('enter')
        sleep(10)
    except ImageNotFoundException:
        pass

    # Switch to favorite
    pyautogui.press('f')
    pyautogui.press('enter')
    sleep(1)

    # Switch to post board
    pyautogui.press(board_order)
    pyautogui.press('enter')
    sleep(1)
    pyautogui.press('enter')
    sleep(1)
    pyautogui.press('enter')
    sleep(1)

    # New Post
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('p')
    pyautogui.keyUp('p')
    pyautogui.keyUp('ctrl')
    sleep(1)

    # Select Post Type
    pyautogui.press(post_type)
    pyautogui.press('enter')
    sleep(1)

    # Select Post Type
    pyperclip.copy(news_title)
    pyautogui.keyDown('alt')
    pyautogui.keyDown('p')
    pyautogui.keyUp('p')
    pyautogui.keyUp('alt')
    pyautogui.press('enter')
    sleep(1)

    # Clear Default Notifications
    for i in range(post_clear_default_lines):
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('y')
        pyautogui.keyUp('y')
        pyautogui.keyUp('ctrl')
        sleep(0.1)

    sleep(1)


def fake_typewriter():

    """
    with open(test_file, 'r', encoding="utf-8") as f:
        while True:
            c = f.read(1)
    """

    c_cnt = 0

    for c in news_article:
        if c == '\n':
            pyautogui.press('enter')
            c_cnt = 0
            pass
        elif not c:
            break
        else:
            pyperclip.copy(c)
            pyautogui.keyDown('alt')
            pyautogui.keyDown('p')
            pyautogui.keyUp('p')
            pyautogui.keyUp('alt')

            try:
                c_cnt += len(c.encode('Big5'))
            except UnicodeEncodeError:
                c_cnt += 1
            if c_cnt >= post_line_max_width:
                pyautogui.press('enter')
                c_cnt = 0
            sleep(0.1)

    pyautogui.typewrite(f'\n Reference: \n {news_link}')

    # Post News
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    pyautogui.keyUp('ctrl')
    pyautogui.press('s')
    pyautogui.press('enter')
    pyautogui.press('enter')

    # Exit Application
    x, y = pyautogui.size()
    pyautogui.click(x=x-5, y=5)
    pyautogui.press('enter')


if __name__ == '__main__':

    while True:
        if news_search():
            if news_copy():
                post_switch('3', '5')
                # post_switch('6', '1')  # Test board
                fake_typewriter()
        sleep(600)
