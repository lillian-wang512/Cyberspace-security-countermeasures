# # -*- coding:utf-8 -*-
# # Author: Suummmmer
# # Date: 2019-05-17

# import requests
# import random

# headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
#     "like Gecko) Chrome/69.0.3497.100 Safari/537.36",
# }


# def get_tid():

#     """获取tid,c,w:return:tid"""
#     tid_url = "https://passport.weibo.com/visitor/genvisitor"
#     data = {
#         "cb": "gen_callback",
#         "fp": {
#             "os": "3",
#             "browser": "Chrome69,0,3497,100",
#             "fonts": "undefined",
#             "screenInfo": "1920*1080*24",
#             "plugins": "Portable Document Format::internal-pdf-viewer::Chrome PDF Plugin|::mhjfbmdgcfjbbpaeojofohoefgiehjai::Chrome PDF Viewer|::internal-nacl-plugin::Native Client"
#         }
#     }
#     req = requests.post(url=tid_url, data=data, headers=headers)

#     if req.status_code == 200:
#         ret = eval(req.text.replace("window.gen_callback && gen_callback(",
#            "").replace(");", "").replace("true", "1"))
#         return ret.get('data').get('tid')
#     return None


# def get_cookie():

#     """获取完整的cookie:return: cookie"""
#     tid = get_tid()
#     if not tid:
#         return None

#     cookies = {
#         "tid": tid + "__095"  # + tid_c_w[1]
#     }
#     url = "https://passport.weibo.com/visitor/visitor?a=incarnate&t={tid}"
#     "&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand={rand}"
#     req = requests.get(url.format(tid=tid, rand=random.random()),
#                    cookies=cookies, headers=headers)
#     if req.status_code != 200:
#         return None

#     ret = eval(req.text.replace("window.cross_domain && cross_domain(",
#            "").replace(");", "").replace("null", "1"))

#     try:
#         sub = ret['data']['sub']
#         if sub == 1:
#             return None
#         subp = ret['data']['subp']
#     except KeyError:
#         return None
#     return sub, subp



#coding=utf-8 

from selenium import webdriver 
import time

driver = webdriver.Chrome() 
driver.maximize_window() 
driver.implicitly_wait(6) 

driver.get("https://www.baidu.com") 
driver.find_element_by_id("kw").send_keys("Selenium")
driver.find_element_by_id("su").click()
time.sleep(3)

# 后退
driver.back()
time.sleep(3)

# 前进
driver.forward()
time.sleep(3)

ele_string = driver.find_element_by_xpath("//*[@id='1']/h3/a/em").text 
if (ele_string == "Selenium"): 
    print ("测试成功，结果和预期结果匹配！")

print(driver.capabilities['version'])

# 在搜索结果页面点击新闻类别 
driver.find_element_by_xpath("//*[@id='s_tab']/a[text()='新闻']").click() 

time.sleep(1) 

# current_url 方法可以得到当前页面的URL 
print (driver.current_url)  

# title方法可以获取当前页面的标题显示的字段 
print (driver.title)          

driver.quit()
 