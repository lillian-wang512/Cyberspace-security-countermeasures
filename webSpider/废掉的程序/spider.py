# -*- coding:utf-8 -*-
 
import requests
import re
from store_mysql import Mysql
import MySQLdb
 
class weiboSpider(object):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    }
    cookies = {
        'TC-Page-G0':'1bbd8b9d418fd852a6ba73de929b3d0c',
        'login_sid_t':'0554454a652ee2a19c672e92ecee3220',
        '_s_tentry':'-',
        'Apache':'8598167916889.414.1493773707704',
        'SINAGLOBAL':'8598167916889.414.1493773707704',
        'ULV':'1493773707718:1:1:1:8598167916889.414.1493773707704:',
        'SCF':'An3a20Qu9caOfsjo36dVvRQh7tKzwKwWXX7CdmypYAwRoCoWM94zrQyZ-5QJPjjDRpp2fBxA_9d6-06C8vLD490.',
        'SUB':'_2A250DV37DeThGeNO7FEX9i3IyziIHXVXe8gzrDV8PUNbmtAKLWbEkW8qBangfcJP4zc_n3aYnbcaf1aVNA..',
        'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WhR6nHCyWoXhugM0PU8VZAu5JpX5K2hUgL.Fo-7S0ecSoeXehB2dJLoI7pX9PiEIgij9gpD9J-t',
        'SUHB':'0jBY7fPNWFbwRJ',
        'ALF':'1494378549',
        'SSOLoginState':'1493773739',
        'wvr':'6',
        'UOR':',www.weibo.com,spr_sinamkt_buy_lhykj_weibo_t111',
        'YF-Page-G0':'19f6802eb103b391998cb31325aed3bc',
        'un':'fengshengjie5 @ live.com'
    }
    def __init__(self):
       field = ['title', 'name', 'id', 'wblevel', 'addr', 'graduate', 'care', 'careurl', 'fans', 'fansurl', 'wbcount',
                'wburl']
       conn = MySQLdb.connect(user='root', passwd='123456', db='zhihu', charset='utf8')
       conn.autocommit(True)
       self.cursor = conn.cursor()
       self.mysql = Mysql('sina', field, len(field) + 1)
    def getUserData(self,id):
        self.cursor.execute('select id from sina where id=%s',(id,))
        data = self.cursor.fetchall()
        if data:
            pass
        else:
            item = {}
            #test = [5321549625,1669879400,1497035431,1265189091,5705874800,5073663404,5850521726,1776845763]
            url = 'http://weibo.com/u/'+id+'?topnav=1&wvr=6&retcode=6102'
            data = requests.get(url,headers=self.headers,cookies=self.cookies).text
            #print data
            id = url.split('?')[0].split('/')[-1]
            try:
                title = re.findall(r'<title>(.*?)</title>',data)[0]
                title = title.split('_')[0]
            except:
                title= u''
            try:
                name = re.findall(r'class=\\"username\\">(.+?)<',data)[0]
            except:
                name = u''
            try:
                totals = re.findall(r'class=\\"W_f\d+\\">(\d*)<',data)
                care = totals[0]
                fans = totals[1]
                wbcount = totals[2]
            except:
                care = u''
                fans = u''
                wbcount = u''
            try:
                urls = re.findall(r'class=\\"t_link S_txt1\\" href=\\"(.*?)\\"',data)
                careUrl = urls[0].replace('\\','').replace('#place','&retcode=6102')
                fansUrl = urls[1].replace('\\','').replace('#place','&retcode=6102')
                wbUrl = urls[2].replace('\\','').replace('#place','&retcode=6102')
            except:
                careUrl = u''
                fansUrl = u''
                wbUrl = u''
            profile = re.findall(r'class=\\"item_text W_fl\\">(.+?)<',data)
            try:
                wblevel = re.findall(r'title=\\"(.*?)\\"',profile[0])[0]
                addr = re.findall(u'[\u4e00-\u9fa5]+', profile[1])[0]# 地址
            except:
                profile1 = re.findall(r'class=\\"icon_group S_line1 W_fl\\">(.+?)<',data)
                try:
                    wblevel = re.findall(r'title=\\"(.*?)\\"', profile1[0])[0]
                except:
                    wblevel = u''
                try:
                    addr = re.findall(u'[\u4e00-\u9fa5]+', profile[0])[0]
                except:
                    addr = u''
            try:
                graduate = re.findall(r'profile&wvr=6\\">(.*?)<',data)[0]
            except:
                graduate = u''
            item[1] = title
            item[2] =name
            item[3] =id
            item[4] =wblevel
            item[5] =addr
            item[6] =graduate
            item[7] =care
            item[8] =careUrl
            item[9] =fans
            item[10] =fansUrl
            item[11] =wbcount
            item[12] =wbUrl
            self.mysql.insert(item)


#-*- coding:utf-8 -*-
import requests
import re
import random
from proxy import Proxy
from getCookie import COOKIE
from time import sleep
from store_mysql import Mysql
from weibo_spider import weiboSpider
class fansSpider(object):
 
    headers = [
        {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"},
        {"user-agent": "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"},
        {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3"},
        {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"},
        {"user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
    ]
    def __init__(self):
        self.wbspider = weiboSpider()
        self.proxie = Proxy()
        self.cookie = COOKIE()
        self.cookies = self.cookie.getcookie()
        field = ['id']
        self.mysql = Mysql('sinaid', field, len(field) + 1)
        self.key = 1
    def getData(self,url):
        self.url = url
        proxies = self.proxie.popip()
        print self.cookies
        print proxies
        r = requests.get("https://www.baidu.com", headers=random.choice(self.headers), proxies=proxies)
        while r.status_code != requests.codes.ok:
            proxies = self.proxie.popip()
            r = requests.get("https://www.baidu.com", headers=random.choice(self.headers), proxies=proxies)
        data = requests.get(self.url,headers=random.choice(self.headers), cookies=self.cookies, proxies=proxies,timeout=20).text
        #print data
        infos = re.findall(r'fnick=(.+?)&f=1\\',data)
        if infos is None:
            self.cookies = self.cookie.getcookie()
            data = requests.get(self.url, headers=random.choice(self.headers), cookies=self.cookies, proxies=proxies,
                                timeout=20).text
            infos = re.findall(r'fnick=(.+?)&f=1\\', data)
        fans = []
        for info in infos:
            fans.append(info.split('&')[0])
        try:
            totalpage = re.findall(r'Pl_Official_HisRelation__6\d+\\">(\d+)<',data)[-1]
            print totalpage
        except:
            totalpage = 1
        # totalpage = re.findall(r'Pl_Official_HisRelation__\d+\\">(\d+)<', data)[-1]
        Id = [one for one in re.findall(r'usercard=\\"id=(\d+)&',data)]
        self.totalid = [Id[i] for i in range(1,len(fans)*2+1,2)]
        if int(totalpage) == 1:
             for one in self.totalid:
                 self.wbspider.getUserData(one)
             item = {}
             for one in self.totalid:
                 item[1] = one
                 self.mysql.insert(item)
                 fansurl = 'http://weibo.com/p/100505' + one + '/follow?from=page_100505&wvr=6&mod=headfollow&retcode=6102'
                 # fansurl = 'http://weibo.com/p/100505' + one + '/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans&retcode=6102'
                 fan.getData(fansurl)
        elif int(totalpage) >= 5:
            totalpage=5
        self.mulpage(totalpage)
        # if self.key == 1:
        #      self.mulpage(totalpage)
        # else:
        #     self.carepage(totalpage)
    # def carepage(self,pages):
    #     #self.key=1
    #     urls = ['http://weibo.com/p/1005051497035431/follow?page={}&retcode=6102'.format(i) for i in range(2, int(pages) + 1)]
    #     for url in urls:
    #         sleep(2)
    #         print url.split('&')[-2]
    #         proxies = self.proxie.popip()
    #         r = requests.get("https://www.baidu.com", headers=random.choice(self.headers), proxies=proxies)
    #         print r.status_code
    #         while r.status_code != requests.codes.ok:
    #             proxies = self.proxie.popip()
    #             r = requests.get("https://www.baidu.com", headers=random.choice(self.headers), proxies=proxies)
    #         data = requests.get(url, headers=random.choice(self.headers), cookies=self.cookies, proxies=proxies,
    #                             timeout=20).text
    #         # print data
    #         infos = re.findall(r'fnick=(.+?)&f=1\\', data)
    #         if infos is None:
    #             self.cookies = self.cookie.getcookie()
    #             data = requests.get(self.url, headers=random.choice(self.headers), cookies=self.cookies,
    #                                 proxies=proxies,
    #                                 timeout=20).text
    #             infos = re.findall(r'fnick=(.+?)&f=1\\', data)
    #         fans = []
    #         for info in infos:
    #             fans.append(info.split('&')[0])
    #         Id = [one for one in re.findall(r'usercard=\\"id=(\d+)&', data)]
    #         totalid = [Id[i] for i in range(1, len(fans) * 2 + 1, 2)]
    #         for one in totalid:
    #             # print one
    #             self.totalid.append(one)
    #     for one in self.totalid:
    #         sleep(1)
    #         self.wbspider.getUserData(one)
    #     item = {}
    #     for one in self.totalid:
    #         item[1] = one
    #         self.mysql.insert(item)
    #         fansurl = 'http://weibo.com/p/100505'+one+'/follow?from=page_100505&wvr=6&mod=headfollow&retcode=6102'
    #         #fansurl = 'http://weibo.com/p/100505' + one + '/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans&retcode=6102'
    #         fan.getData(fansurl)
    def mulpage(self,pages):
        #self.key=2
        urls = ['http://weibo.com/p/1005051497035431/follow?relate=fans&page={}&retcode=6102'.format(i) for i in range(2,int(pages)+1)]
        for url in urls:
            sleep(2)
            print url.split('&')[-2]
            proxies = self.proxie.popip()
            r = requests.get("https://www.baidu.com", headers=random.choice(self.headers), proxies=proxies)
            print r.status_code
            while r.status_code != requests.codes.ok:
                proxies = self.proxie.popip()
                r = requests.get("https://www.baidu.com", headers=random.choice(self.headers), proxies=proxies)
            data = requests.get(url, headers=random.choice(self.headers), cookies=self.cookies, proxies=proxies,
                                timeout=20).text
            # print data
            infos = re.findall(r'fnick=(.+?)&f=1\\', data)
            if infos is None:
                self.cookies = self.cookie.getcookie()
                data = requests.get(self.url, headers=random.choice(self.headers), cookies=self.cookies,
                                    proxies=proxies,
                                    timeout=20).text
                infos = re.findall(r'fnick=(.+?)&f=1\\', data)
            fans = []
            for info in infos:
                fans.append(info.split('&')[0])
            Id = [one for one in re.findall(r'usercard=\\"id=(\d+)&', data)]
            totalid = [Id[i] for i in range(1, len(fans) * 2 + 1, 2)]
            for one in totalid:
                #print one
                self.totalid.append(one)
        for one in self.totalid:
            sleep(1)
            self.wbspider.getUserData(one)
        item ={}
        for one in self.totalid:
            item[1]=one
            self.mysql.insert(item)
            #fansurl = 'http://weibo.com/p/1005055847228592/follow?from=page_100505&wvr=6&mod=headfollow&retcode=6102'
            fansurl = 'http://weibo.com/p/100505'+one+'/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans&retcode=6102'
            fan.getData(fansurl)
if __name__ == "__main__":
    url = 'http://weibo.com/p/1005051497035431/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans&retcode=6102'
    fan = fansSpider()
    fan.getData(url)