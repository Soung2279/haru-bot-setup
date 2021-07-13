import re
import requests

# 获取蛛王链接
def getzhuHtml(url):
  html4 = requests.get(url)
  html4.encoding = 'utf-8'
  html4 = html4.text
  return html4

# 获取蛛王图片链接的字符串
def getzhuImg(html4):
  imglist = re.findall(r'(https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.jpg|https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.png)', html4)
  for url4 in imglist:
    return url4

def sethtml4():
  html4 = str(getzhuHtml("https://api.xiaoheihe.cn/wiki/get_article_for_app/?article_id=8829978&wiki_id=1085660&is_share=1"))
  return html4

# print(getzhuImg(sethtml4()))