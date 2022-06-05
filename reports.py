import os

import pygame
import pygame.font
import requests
from bs4 import BeautifulSoup


class Reports:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('arialunicode', 24)

        # key：每个报告的url value：每个页面的title
        self.text = {}

        self.url = "https://www.mee.gov.cn/"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
        }

    # 爬取的是每个报告的网址 https://www.mee.gov.cn/hjzl/shj/qgdbszlzk
    def pyspider_pages(self, number):
        """爬取每个报告的网址信息"""
        if number == 0:
            s = "hjzl/shj/qgdbszlzk/index.shtml"
        else:
            s = "hjzl/shj/qgdbszlzk/index_" + str(number) + ".shtml"

        page_text = requests.get(url=self.url + s, headers=self.headers)
        response = bytes(page_text.text, page_text.encoding).decode('utf-8', 'ignore')
        soup = BeautifulSoup(response, 'lxml')

        links = soup.select('#div > li')
        for li in links:
            link = self.url + li.a['href'][9:]
            self.text[link] = li.a.text

    def prep_text(self):
        # 总共有三页
        for i in range(3):
            self.pyspider_pages(number=i)

    def save_pictures(self, url_picture):
        res = requests.get(url_picture)
        # 把Reponse对象的内容以二进制数据的形式返回
        pic = res.content
        # 新建了一个文件ppt.jpg，这里的文件没加路径，它会被保存在程序运行的当前目录下。
        photo = open(self.picture_file, 'wb')
        # 获取pic的二进制内容
        photo.write(pic)
        photo.close()

    def pyspider_pictures(self, url_page):
        """根据具体的页面对页面进行爬取，获得图片"""
        print(url_page)
        page_text = requests.get(url=url_page, headers=self.headers)
        response = bytes(page_text.text, page_text.encoding).decode('utf-8', 'ignore')
        soup = BeautifulSoup(response, 'lxml')

        if self.index == 1:
            p_list = soup.select('.Custom_UnionStyle > div > font > img')
        elif self.index == 4:
            p_list = soup.select('.Custom_UnionStyle > p > img')
        elif self.index == 6:
            p_list = soup.select('.TRS_Editor > p > img')
        elif self.index == 7 or self.index == 8 or self.index == 10:
            p_list = soup.select('.TRS_Editor > div > img')
        else:
            p_list = soup.select('.Custom_UnionStyle > div > img')

        url = url_page[:40] + p_list[0]['oldsrc']
        print(url)
        self.save_pictures(url)

    def get_pictures(self, key):
        """根据当前目录下是否有相应的图片文件存在判断是否需要进行爬取"""
        self.picture_file = '/Users/xiaozhu/PycharmProjects/Seva/report/report' + str(self.index) + '.png'

        if not os.path.exists(self.picture_file):
            self.pyspider_pictures(key)
        self.image_bg = pygame.image.load(self.picture_file)

        self.image_rect = self.image_bg.get_rect()
        self.image_rect.midtop = (self.screen.get_rect().width / 2, self.screen.get_rect().height / 4)

        self.screen.blit(self.image_bg, self.image_rect)

    def show_text(self, index):
        """页面上方绘制图片和title"""
        self.index = index

        item = self.text.items()
        if self.index < len(self.text):
            key, value = list(item)[self.index - 1]
            self.get_pictures(key)
        else:
            value = "error"

        self.report_text = self.font.render(value, True, self.text_color, (255, 255, 255))

        self.report_rect = self.report_text.get_rect()
        self.report_rect.midtop = (self.screen.get_rect().width / 2, 50)

        self.screen.blit(self.report_text, self.report_rect)
