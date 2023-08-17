import requests
from bs4 import BeautifulSoup


def img():
    url = 'http://www.tfent.cn/Audio/single'  # 需要访问的地址
    res = requests.get(url)  # 访问地址
   
    soup = BeautifulSoup(res.text, "lxml")  # 定义一个Soup对象，lxml 解析器
    label = soup.select("a")  # 搜索页面中所有的img标签，以列表的形式展示
    # label = soup.select("")  #
    print(label)
    for i in label:
        # print("zxcvbn")
        src = i['data-lyric']  # 获取图片下载地址
        print(src.text)  # 循环打印图片下载地址


if __name__ == "__main__":
    img()


# from selenium import webdriver
# import time
# import requests
# from bs4 import BeautifulSoup
# import json
# import csv
# import codecs
# import time

# driver=webdriver.Chrome()
# driver.get('http://www.tfent.cn/Audio/single')

# # driver.find_element_by_xpath('//*[@id="s-top-left"]/a[3]').click()


# # for handle in driver.window_handles:
# #             driver.switch_to_window(handle)
# #             if driver.current_url=='https://map.baidu.com/@12978768,4829766,13z':
# #                 break   

# # 


# # class="title-content-title"

# # print(driver.find_element_by_xpath('//*[@id="singleMusicList"]/li[1]/div[2]/div/a[4]').text)
# print(driver.find_element_by_link_text('//*[@id="singleMusicList"]/li[1]/div[2]/div/a[4]'))