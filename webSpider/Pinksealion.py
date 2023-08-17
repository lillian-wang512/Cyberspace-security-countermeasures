# 引入库
from bs4 import BeautifulSoup
import requests
import pandas as pd
import jieba
import jieba.analyse
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
exclude = {'download', 'detail', 'class download', 'data lyric', 'Javascript', 'href', 'a', 'class', 'Studio','so','I','add', 'data', 'lyric', 'wow', 'beautiful','编曲','词','曲','制作人', '素颜随意', '娃娃','歌词'}

# BeautifulSoup4已被移植至bs4，通过bs4导入

# 用户代理，即用户所用软件（浏览器）
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/51.0.2704.63 Safari/537.36'}

# get页面并获得返回的requests
# 用户代理改为浏览器形态，对抗反爬机制
r = requests.get('http://www.tfent.cn/Audio/single', headers=ua)

# 检测所抓取的内容是否与网络源代码相同
# print(r.text)

# 分析html结构
html = BeautifulSoup(r.text, 'html.parser')

# 选择所需部分
# song对应整个<Li></Li>元素
song_list = html.select('li.clearfix')

# 检测抓取内容是否为所需
# print(len(song_list))

result = []
for song in song_list:
    song_info = {}

    Name = song.select('p.musicName')
    # 保证所有p标签分开存放至列表，取出文本部分赋给title
    song_info['title'] = Name[0].text

    # 检测是否存放成功
    print(song_info['title'])

    Singer = song.select('p.singer')
    # 保证所有p标签分开存放至列表，取出文本部分赋给singer
    song_info['singer'] = Singer[0].text

    # 检测是否存放成功
    print(song_info['singer'])

    # 搜索页面中所有的a标签，以列表的形式展示
    label = song.select("a")
    # 检测歌词是否成功写入
    # print(label)

    with open("tf.txt", "a", encoding="utf-8")as c:
        c.write(str(label))


f = open('tf.txt', encoding="utf-8")

txt = f.read()

f.close()

w = WordCloud(width=1000, height=600, font_path='msyh.ttc',
              max_words=100, background_color='white', stopwords=exclude)
# jieba.analyse.set_stop_words(r'stopwords.txt')
w.generate(txt)

w.to_file("tf.png")
