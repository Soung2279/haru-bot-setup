import re
import requests

# 返回小黑盒百科的源码
def getchallHtml(url):
  html333 = requests.get(url)
  html333.encoding = 'utf-8'
  html333 = html333.text
  html333 = html333.replace('\n','')
  html333 = html333.replace(' ','')
  # print(html333)
  return html333

# 返回试炼周报的链接
def getchall(html333):
  imglist = re.findall(r'tag\_name\"\:\"\\u5468\\u62a5.+?id\=1085660', html333)
  for html30 in imglist:
    imglist = re.findall(r'https\:\\\/\\\/api\.xiaoheihe\.cn\\\/wiki\\\/get\_article\_for\_app.+?id\=1085660', html30)
    for html33 in imglist:
      html33 = html33.replace('\\','')
      # print(html33)
      return html33

# 返回试炼周报的源码
def getchallHtml3(html33):
  html3 = requests.get(html33)
  html3.encoding = 'utf-8'
  html3 = html3.text
  # print(html3)
  return html3

# 字符串格式输出图片链接
def getchallImg(html3):
  imglist = re.findall(r'https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.png|https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.jpg', html3)
  for url3 in imglist:
    return url3

def sethtml3():
  html3 = str(getchallHtml3(str(getchall(str(getchallHtml("https://api.xiaoheihe.cn/wiki/get_homepage_content/?wiki_id=1085660&verison=&is_share=1"))))))
  return html3

# print(getchallImg(sethtml3()))