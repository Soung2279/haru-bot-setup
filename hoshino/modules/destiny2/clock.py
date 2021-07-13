import datetime
import http.client
import time
import sys
import hoshino
import os,base64
import requests as req
from PIL import Image
from io import BytesIO
from hoshino import Service, R, priv
from .get_zhoubao_info import *
from .get_xur_info import *
from .get_chall_info import *
from .get_zhu_info import *



def get_time():
    time_conn = http.client.HTTPConnection('www.baidu.com')
    time_conn.request("GET", "/")
    r = time_conn.getresponse()
    ts = r.getheader('date')
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime = time.localtime(time.mktime(ltime)+8*60*60)
    dat = datetime.date(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    # 下方用于测试用
    # global testtime
    # test1 = "%u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    # test2 = "%02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    # currenttime=test1+" "+test2
    # testtime = str(currenttime)
    return dat

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

svzb = Service(
    name = '周报更新提醒',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '命运2', #属于哪一类
    help_='周报更新提醒' #帮助文本
    )

svlj = Service(
    name = '老九更新提醒',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '命运2', #属于哪一类
    help_='周报更新提醒' #帮助文本
    )

svsl = Service(
    name = '试炼更新提醒',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '命运2', #属于哪一类
    help_='周报更新提醒' #帮助文本
    )

svzw = Service(
    name = '蛛王更新提醒',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '命运2', #属于哪一类
    help_='周报更新提醒' #帮助文本
    )


@svzb.scheduled_job('cron', hour='03', minute='00')
async def zhoubaoreminder():
    sys.stdout.flush()
    if get_week_day(get_time()) == '星期三':
        response = req.get(getzhoubaoImg(sethtml1()))
        ls_f = base64.b64encode(BytesIO(response.content).read())
        imgdata = base64.b64decode(ls_f)
        save_dir = R.img('destiny2').path
        path_dir = os.path.join(save_dir,'zhoubao.jpg')
        file = open(path_dir,'wb')
        file.write(imgdata)
        file.close()
        pzhoubao = ' '.join(map(str, [
            R.img(f'destiny2/zhoubao.jpg').cqcode,
        ]))
        msg = '今天是' + get_week_day(get_time()) + '\n周报已更新\n' + f'命运2 周报：\n图片作者：seanalpha\n{pzhoubao}'
        await svzb.broadcast(msg, 'zhoubao-reminder', 0.2)

@svlj.scheduled_job('cron', hour='03', minute='00')
async def laojiureminder():
    sys.stdout.flush()
    if get_week_day(get_time()) == '星期六':
        response = req.get(getxurImg(sethtml2()))
        ls_f = base64.b64encode(BytesIO(response.content).read())
        imgdata = base64.b64decode(ls_f)
        save_dir = R.img('destiny2').path
        path_dir = os.path.join(save_dir,'xur.jpg')
        file = open(path_dir,'wb')
        file.write(imgdata)
        file.close()
        pxur = ' '.join(map(str, [
            R.img(f'destiny2/xur.jpg').cqcode,
        ]))
        msg = '今天是' + get_week_day(get_time()) + '\n老九信息已更新\n' + f'命运2 仄：\n图片作者：seanalpha\n{pxur}'
        await svlj.broadcast(msg, 'laojiu-reminder', 0.2)

@svsl.scheduled_job('cron', hour='03', minute='00')
async def shilianreminder():
    sys.stdout.flush()
    if get_week_day(get_time()) == '星期六':
        response = req.get(getchallImg(sethtml3()))
        ls_f = base64.b64encode(BytesIO(response.content).read())
        imgdata = base64.b64decode(ls_f)
        save_dir = R.img('destiny2').path
        path_dir = os.path.join(save_dir,'shilian.jpg')
        file = open(path_dir,'wb')
        file.write(imgdata)
        file.close()
        pshilian = ' '.join(map(str, [
            R.img(f'destiny2/shilian.jpg').cqcode,
        ]))
        msg = '今天是' + get_week_day(get_time()) + '\n试炼周报已更新\n' + f'命运2 试炼周报：\n图片作者：seanalpha\n{pshilian}'
        await svsl.broadcast(msg, 'shilian-reminder', 0.2)

@svzw.scheduled_job('cron', hour='03', minute='00')
async def zhuwangreminder():
    sys.stdout.flush()
    response = req.get(getzhuImg(sethtml4()))
    ls_f = base64.b64encode(BytesIO(response.content).read())
    imgdata = base64.b64decode(ls_f)
    save_dir = R.img('destiny2').path
    path_dir = os.path.join(save_dir,'zhuwang.jpg')
    file = open(path_dir,'wb')
    file.write(imgdata)
    file.close()
    pzhuwang = ' '.join(map(str, [
        R.img(f'destiny2/zhuwang.jpg').cqcode,
    ]))
    msg = '今天是' + get_week_day(get_time()) + '\n蛛王商店已刷新\n注意小黑盒蛛王信息可能更新较慢\n' + f'命运2 蛛王：\n图片来源：小黑盒百科\n{pzhuwang}'
    await svzw.broadcast(msg, 'zhuwang-reminder', 0.2)
