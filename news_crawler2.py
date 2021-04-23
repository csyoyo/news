#!

import requests
import bs4
import re
import shelve
from news_common import NewsCrawler
from news_common import get_digit_list

news_site_root = ''
news_site = '***'
news_data_log = 'news_crawler2_date_log'


def news_search(self):

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
    date_tag = soup.select('.home-news-primary-item-date')
    news_date = get_digit_list(str(date_tag[0].getText()))
    # print(news_date)

    # Check if News have been posted
    shelve_file = shelve.open(news_data_log)

    try:
        latest_date = shelve_file[news_data_log]
        if news_date > latest_date:
            shelve_file[news_data_log] = news_date
        else:
            print(f'news_search info: no updated news')
            shelve_file.close()
            return False
    except KeyError:
        shelve_file[news_data_log] = news_date

    shelve_file.close()

    # Get News Link
    news_tag = date_tag[0].find_parent("div").find_parent("div")

    self.news_link = news_site_root + news_tag.find('a').get('href')
    # print(self.news_link)

    # Get News Title
    self.news_title = str(news_tag.find('a').find('img').get('alt')).strip('\n').strip('\u200b')

    # print(self.news_title)

    return True


def news_copy(self):

    if self.news_link is None:
        return False

    res = requests.get(self.news_link)
    try:
        res.raise_for_status()
    except Exception as exc:
        print(f'news_copy error: problem in connection: {exc}')
        return False

    if res.status_code != requests.codes.ok:
        print(f'news_copy error: request code: {res.status_code}')
        return False

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    post = soup.select('.text-module')

    self.news_article = ''

    for posts in post:
        self.news_article += posts.getText()

    self.news_article = re.sub(' +', ' ', self.news_article)
    self.news_article = re.sub('\n+', '\n', self.news_article)

    # print(self.news_article)

    return True


class NewsCrawler2(NewsCrawler):
    def search(self):
        return news_search(self)

    def copy(self):
        return news_copy(self)


if __name__ == '__main__':
    pass
