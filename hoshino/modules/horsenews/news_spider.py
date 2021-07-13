# -*- coding: UTF-8 -*-
import requests
import os
import json
import datetime
import operator

class news_class:
    def __init__(self,news_time,news_url,news_title):
        self.news_time = news_time
        self.news_url = news_url
        self.news_title = news_title

def get_item():
    url = 'https://umamusume.jp/api/ajax/pr_info_index?format=json'
    data = {}
    data['announce_label'] = 0
    data['limit'] = 10
    data['offset'] = 0
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers, timeout=(5,10))
    res_dict = res.json()
    return res_dict

def sort_news():
    res_dict = get_item()
    news_list = []
    for n in range(0, 5):
        if (res_dict['information_list'][n]['update_at'] == None):
            news_time = res_dict['information_list'][n]['post_at']
        else :
            news_time = res_dict['information_list'][n]['update_at']

        news_id = res_dict['information_list'][n]['announce_id']
        news_url = '▲https://umamusume.jp/news/detail.php?id=' + str(news_id)
        news_title = res_dict['information_list'][n]['title']
        news_list.append(news_class(news_time, news_url ,news_title))

    news_key = operator.attrgetter('news_time')
    news_list.sort(key = news_key, reverse = True)
    return news_list

def get_news():
    news_list = sort_news()
    msg = '◎◎ 马娘官网新闻 ◎◎\n'
    for news in news_list:
        msg = msg + '\n' + news.news_time + '\n' + news.news_title + '\n' + news.news_url + '\n'
    return msg

def news_broadcast():
    news_list = sort_news()
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    init_time = str(file.read())
    file.close()
    init_time = datetime.datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    msg = '◎◎ 马娘官网新闻更新 ◎◎\n'
    for news in news_list:
        prev_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        if (init_time >= prev_time):
            break
        else:
            msg = msg + '\n' + news.news_time + '\n' + news.news_title + '\n' + news.news_url + '\n'

    for news in news_list:
        set_time = news.news_time
        break
    file = open(current_dir, 'w', encoding="UTF-8")
    file.write(str(set_time))
    file.close()
    return msg

# 判断一下是否有更新，为什么要单独写一个函数呢
# 函数单独写一个是怎么回事呢？函数相信大家都很熟悉，但是函数单独写一个是怎么回事呢，下面就让小编带大家一起了解吧。
# 函数单独写一个，其实就是我想单独写一个函数，大家可能会很惊讶函数怎么会单独写一个呢？但事实就是这样，小编也感到非常惊讶。
# 这就是关于函数单独写一个的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！
def judge() -> bool:
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    if (os.path.exists(current_dir) == True):
        file = open(current_dir, 'r', encoding="UTF-8")
        init_time = str(file.read())
        file.close()
    else:
        news_list = sort_news()
        for news in news_list:
            init_time = news.news_time
            break
        current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
        file = open(current_dir, 'w', encoding="UTF-8")
        file.write(str(init_time))
        file.close()

    news_list = sort_news()
    for news in news_list:
        prev_time = news.news_time
        break
    
    if (init_time != prev_time):
        return True
    else:
        return False