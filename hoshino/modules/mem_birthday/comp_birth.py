import os
import yaml
import datetime
import http.client
import time

# 获取时间
def get_time():
    time_conn = http.client.HTTPConnection('www.baidu.com')
    time_conn.request("GET", "/")
    r = time_conn.getresponse()
    ts = r.getheader('date')
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime = time.localtime(time.mktime(ltime)+8*60*60)
    dat = datetime.date(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    return dat

# 获取星期
def get_week_day(date):
    week_day = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期日',
    }
    day = date.weekday()
    return week_day[day]

# 祝贺这几个B生日快乐
def get_bir_info(bir_list):
    tod = get_time()
    msg = f'今天是 {str(tod)} {get_week_day(tod)}\n\n让我们祝贺这{len(bir_list)}些hxd生日快乐~：'
    for user_id in bir_list:
        msg = msg + f'\n[CQ:at,qq={user_id}]'
    msg = msg + '\n这是小蛋糕：[CQ:face,id=53][CQ:face,id=53][CQ:face,id=53]'
    return msg

# 判断是否生日
def judge_bir(gid):
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    bir_list = []
    for user in config['Info'][gid]:
        user_id = int(user['member']['user_id'])
        yes_age = int(user['member']['yes_age'])
        tod_age = int(user['member']['tod_age'])
        if tod_age == yes_age + 1:
            # 这说明这个B生日了
            bir_list.append(user_id)
    return bir_list