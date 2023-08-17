# 登录b站并爬虫（十分害怕号被封了2333）

# 引用一堆库（我是用pipenv下的，所以要先shell再用
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import time
import os
import re
import platform
from lxml import etree
from datetime import datetime
from bs4 import BeautifulSoup
import json
import csv
import codecs
import time
 
import pandas as pd
import jieba
import jieba.analyse
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


ua = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}


class spider:

    # 设置一些基本参数，以后会用到
    chrome_driver_path = ""
    driver = None
    # driver.get('https://www.bilibili.com/')
    main_page_url = 'https://passport.bilibili.com/login?from_spm_id=333.851.top_bar.login'
    main_page_title = '哔哩哔哩弹幕视频网 - ( ゜- ゜)つロ 乾杯~ - bilibili'
    login_error_mark = '验证码错误'
    login_succeed_title = '哔哩哔哩弹幕视频网 - ( ゜- ゜)つロ 乾杯~ - bilibili'

    # 检查登录界面时会用到
    base_url = 'https://passport.bilibili.com/login?from_spm_id=333.851.top_bar.login'
    portal_url = 'https://passport.bilibili.com/account/security#/home'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/51.0.2704.63 Safari/537.36'}
    cookies = None
    request_session = None

    def __init__(self):
        # 判断系统
        if platform.system() == 'Windows':
            self.chrome_driver_path = "chromedriver.exe"
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.chrome_driver_path = "./chromedriver"
        else:
            print('Unknown System Type. quit...')
            return None

        requests.headers = self.headers

        # 判断网络连接
        try:
            r = requests.get(self.main_page_url)
        except requests.exceptions.RequestException as e:
            print('链接异常，请检查网络')
            print(e)
            quit()

        if(r.status_code != 200):
            print('http状态码错误')
            quit()

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=self.chrome_driver_path)

        return None
    # set cookies when login suceed

    # 登录b站
    def login(self):
        # 打开界面
        self.driver.get(self.main_page_url)
        time.sleep(1)

        # 界面标题判断，判断进入的界面是否准确
        if self.driver.title != self.main_page_title:
            print('不是期望的主页Title，网页改版了？')
            return False

        # 得到输入用户名和密码的部分
        elem_user = self.driver.find_element_by_id("login-username")
        elem_pwd = self.driver.find_element_by_id("login-passwd")

        # 输入用户名和密码
        elem_user.send_keys("17792939796")
        elem_pwd.send_keys("zero123456")
        elem_pwd.send_keys(Keys.RETURN)

        time.sleep(1)

        if(self.driver.find_elements_by_xpath("//*[contains(text(), '"+self.login_error_mark+"')]") != None) \
                and (self.driver.title != self.login_succeed_title):
            print('登录错误')
            return False
        self.cookies = self.driver.get_cookies()
        self.request_session = requests.Session()
        for cookie in self.cookies:
            self.request_session.cookies.set(cookie['name'], cookie['value'])
        time.sleep(11)  # 等一下，怕被封号

# 鼠标点击按钮，来到搜索界面
        self.driver.find_element_by_xpath(
            '//*[@id="internationalHeader"]/div/div/div[1]/ul/li[1]/span/a').click()
        time.sleep(3)
        self.driver.find_element_by_xpath(
            '//*[@id="internationalHeader"]/div[1]/div/div[3]/div[1]/a').click()
        time.sleep(5)
# 更改瞄点
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)
            if self.driver.current_url == 'https://search.bilibili.com/?from_source=webtop_search&spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.10':
                break

        # 在搜索框里输入央视新闻
        elem_search = self.driver.find_element_by_xpath(
            '//*[@id="search-keyword"]')
        elem_search.send_keys("央视新闻")
        time.sleep(5)
        # 点击搜索按钮
        self.driver.find_element_by_xpath(
            '//*[@id="server-search-app"]/div/div/div[2]/a').click()
# 更改瞄点
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)
            if self.driver.current_url == 'https://search.bilibili.com/?from_source=webtop_search&spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.10':
                break
# 等一下，怕被封号
        time.sleep(5)
        # 关闭搜素界面
        self.driver.quit()

        return True


# 爬虫央视新闻搜索界面
# 爬视频名字和url
def url_element_get(video, video_info):
    url_element = video.select('div.info > div.headline.clearfix > a')
    video_info['title'] = url_element[0].text
    video_info['url'] = url_element[0]['href']  # 标签
    return video_info

# 爬播放量


def play_count_element_get(video, video_info):
    play_count_element = video.select('div.info > div.tags > span.watch-num')
    video_info['play_count'] = play_count_element[0].text.strip()  # strip函数移除空格
    return video_info

# 爬弹幕数


def danmu_element_get(video, video_info):
    danmu_element = video.select('div.info > div.tags > span.hide')
    video_info['danmu_count'] = danmu_element[0].text.strip()
    return video_info

# 爬上传时间


def upload_time_element(video, video_info):
    upload_time_element = video.select('div.info > div.tags > span.time')
    video_info['upload_date'] = upload_time_element[0].text.strip()
    return video_info

# 爬up主的url


def up_url_element_get(video, video_info):
    up_url_element = video.select('div.info > div.tags > span > a.up-name')
    video_info['author'] = up_url_element[0].text
    video_info['author_url'] = up_url_element[0]['href']
    return video_info


def main():

    # 爬虫央视新闻搜索界面的主函数
    header = ['题目(title)', '网址(url)', '播放量(play_count)', '弹幕(danmu)',
              '上传时间(upload_date)', '作者UP主(author)', 'UP主个人界面(author_url)']
    # 打开新的文件，CSV格式
    with open('./yangshixinwen_bilibili.csv', 'w', encoding='utf_8_sig', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(header)

    # 爬4页
        for i in range(1, 5):
            r = requests.get(
                f'https://search.bilibili.com/all?keyword=%E5%A4%AE%E8%A7%86%E6%96%B0%E9%97%BB&from_source=web_search&page={i}', headers=ua)
        # 改格式
            html = BeautifulSoup(r.text, 'html.parser')
        # 要爬的视频们
            video_list = html.select('li.video-item.matrix')

            result = []

            for video in video_list:
                video_info = {}
                # 引入一堆函数
                url_element_get(video, video_info)

                play_count_element_get(video, video_info)

                danmu_element_get(video, video_info)

                upload_time_element(video, video_info)

                up_url_element_get(video, video_info)

                result.append(video_info)
            # 写一下爬到哪了，怕忘了
            for i, element in enumerate(result):
                print(f'处理第{i + 1}条, 共{len(result)}条')
                row = element.values()  # 获得所要的值
                print(row)  # 打印出来
                writer.writerow(row)  # 写入csv文件里
                time.sleep(0.5)  # 等一下，怕被封号


# 从回答 csv 文件中提取出回答的文本并转化成列表
def get_answers(file):
    df = pd.read_csv(file)

    answers = df['题目(title)']
    # answers =','.join( df.values.tolist()
    return list(answers)


# 结巴分词的 TD-IDF 接口直接提取关键词和其权重
def get_keywords(content, topK):
    keywords = jieba.analyse.extract_tags(content, topK=topK, withWeight=True)
    df = pd.DataFrame(keywords, columns=['keyword', 'weight'])
    return df


# 生成词云，注意这里的参数是一个字典 {'关键词': 12.123123} 后面的浮点数是权重
def generate_cloud(frequencies):
    wordcloud = WordCloud(
        'simfang.ttf',
        width=1920,
        height=1080,
        background_color='white',
        stopwords=STOPWORDS).generate_from_frequencies(frequencies)

    fig = plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud)
    plt.axis('off')  # 不显示坐标轴
    plt.tight_layout(pad=0)  # 不留空白
    plt.show()



if __name__ == "__main__":
    located = spider()
    located.login()  # b站密码登录函数
    main()  # 爬虫代码函数

    time.sleep(4)
    answers = get_answers('yangshixinwen_bilibili.csv')

    jieba.analyse.set_stop_words(r'stopwords.txt')

    df = pd.DataFrame(columns=['keyword', 'weight'])
    for answer in answers:
        answer_keyword = get_keywords(answer, 10)
        df = df.append(answer_keyword)

    grouped = df.groupby('keyword').sum()

    keywords = grouped.sort_values('weight', ascending=False)

    top_100 = keywords[0:100]
    generate_cloud(top_100.weight.to_dict())


