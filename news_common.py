#!


class NewsCrawler:
    def __init__(self, board_order, post_type):
        self.board_order = board_order
        self.post_type = post_type
        self.news_article = ''
        self.news_link = ''
        self.news_title = ''


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


if __name__ == '__main__':
    pass
