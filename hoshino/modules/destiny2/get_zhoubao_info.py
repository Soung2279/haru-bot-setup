import re
import requests

# 返回小黑盒百科的源码
def getzhoubaoHtml(url):
  html111 = requests.get(url)
  html111.encoding = 'utf-8'
  html111 = html111.text
  html111 = html111.replace('\n','')
  html111 = html111.replace(' ','')
  # print(html111)
  return html111

# 返回周报的链接
def getzhoubao(html111):
  imglist = re.findall(r'tag\_name\"\:\"\\u5168\\u90e8.+?id\=1085660', html111)
  for html10 in imglist:
    imglist = re.findall(r'https\:\\\/\\\/api\.xiaoheihe\.cn\\\/wiki\\\/get\_article\_for\_app.+?id\=1085660', html10)
    for html11 in imglist:
      html11 = html11.replace('\\','')
      # print(html11)
      return html11

# 返回周报的源码
def getzhoubaoHtml1(html11):
  html1 = requests.get(html11)
  html1.encoding = 'utf-8'
  html1 = html1.text
  # print(html1)
  return html1

# 字符串格式输出图片链接
def getzhoubaoImg(html1):
  imglist = re.findall(r'https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.png|https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.jpg', html1)
  for url1 in imglist:
    return url1

def sethtml1():
  html1 = str(getzhoubaoHtml1(str(getzhoubao(str(getzhoubaoHtml("https://api.xiaoheihe.cn/wiki/get_homepage_content/?wiki_id=1085660&verison=&is_share=1"))))))
  return html1

# print(getzhoubaoImg(sethtml1()))