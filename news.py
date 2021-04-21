#!

import pyautogui
import pyperclip
import subprocess
import win32gui
import win32con
from time import sleep
from news_crawler1 import NewsCrawler1

test_file = 'news.txt'

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

news_seekers = []


def post_switch(crawler):

    # Launch App
    subprocess.Popen([post_app])

    sleep(3)

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
    sleep(2)

    # Enter User Password
    pyautogui.typewrite(post_pwd)
    pyautogui.press('enter')
    sleep(2)

    # Check if double connection
    """
        try:
        pyautogui.locateOnScreen(post_condition['double_connect'], confidence=0.9)
        pyautogui.locateOnScreen(post_condition['double_connect'], confidence=0.9)
        pyautogui.locateOnScreen(post_condition['double_connect'], confidence=0.9)
        pyautogui.locateOnScreen(post_condition['double_connect'], confidence=0.9)
        pyautogui.locateOnScreen(post_condition['double_connect'], confidence=0.9)

        pyautogui.typewrite('y')
        sleep(1)
        pyautogui.press('enter')
        print('double_connect')
    except:
        print('normal_connect')
        pass
    """


    sleep(5)
    pyautogui.press('enter')
    sleep(5)

    # Check if article exists
    """
    try:
        pyautogui.locateOnScreen(post_condition['article_exists'], confidence=0.9)

        pyautogui.typewrite('Q')
        sleep(1)
        pyautogui.press('enter')
        sleep(5)
        print('article_exists')
    except:
        print('normal_article_status')
        pass
    """

    # Switch to favorite
    sleep(2)
    pyautogui.typewrite('F')
    sleep(2)
    pyautogui.press('enter')
    sleep(2)

    # Switch to post board
    pyautogui.press(crawler.board_order)
    pyautogui.press('enter')
    sleep(2)
    pyautogui.press('enter')
    sleep(2)
    pyautogui.press('enter')
    sleep(2)

    # New Post
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('p')
    pyautogui.keyUp('p')
    pyautogui.keyUp('ctrl')
    sleep(3)

    # Select Post Type
    pyautogui.press(crawler.post_type)
    sleep(2)
    pyautogui.press('enter')
    sleep(2)

    # Select Post Type
    pyperclip.copy(crawler.news_title)
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


def fake_typewriter(crawler):

    """
    with open(test_file, 'r', encoding="utf-8") as f:
        while True:
            c = f.read(1)
    """

    pyautogui.typewrite(f'\n News Reference: \n {crawler.news_link} \n \n ')

    c_cnt = 0

    for c in crawler.news_article:
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

            """
            try:
                c_cnt += len(c.encode('Big5'))
            except UnicodeEncodeError:
                c_cnt += 1
            if c_cnt >= post_line_max_width:
                pyautogui.press('enter')
                c_cnt = 0
            """

            sleep(1.5)

    pyautogui.typewrite(f'\n News Reference: \n {crawler.news_link} \n \n ')

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

    news_seekers.append(NewsCrawler1('3', '5'))

    while True:
        for seekers in news_seekers:
            if seekers.search() and seekers.copy():
                post_switch(seekers)
                fake_typewriter(seekers)
        sleep(600)
