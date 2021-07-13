import re
import requests

# 返回小黑盒百科的源码
def getxurHtml(url):
  html222 = requests.get(url)
  html222.encoding = 'utf-8'
  html222 = html222.text
  html222 = html222.replace('\n','')
  html222 = html222.replace(' ','')
  # print(html222)
  return html222

# 返回老九的链接
def getxur(html222):
  imglist = re.findall(r'tag\_name\"\:\"\\u5149\\u5c18\\u5546\\u5e97.+?id\=1085660', html222)
  for html20 in imglist:
    imglist = re.findall(r'https\:\\\/\\\/api\.xiaoheihe\.cn\\\/wiki\\\/get\_article\_for\_app.+?id\=1085660', html20)
    for html22 in imglist:
      html22 = html22.replace('\\','')
      # print(html22)
      return html22

# 返回老九的源码
def getxurHtml2(html22):
  html2 = requests.get(html22)
  html2.encoding = 'utf-8'
  html2 = html2.text
  # print(html2)
  return html2

# 字符串格式输出图片链接
def getxurImg(html2):
  imglist = re.findall(r'https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.png|https\:\/\/cdn\.max\-c\.com\/heybox\/dailynews\/img\/(?!c4f5035d1b8053c400c72c0656c12d97).+?\.jpg', html2)
  for url2 in imglist:
    return url2

def sethtml2():
  html2 = str(getxurHtml2(str(getxur(str(getxurHtml("https://api.xiaoheihe.cn/wiki/get_homepage_content/?wiki_id=1085660&verison=&is_share=1"))))))
  return html2

# print(getxurImg(sethtml2()))