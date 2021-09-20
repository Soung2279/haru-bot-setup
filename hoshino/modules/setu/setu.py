# -*- coding: utf-8 -*-
from time import time
from asyncio import events
import re, os, shutil
from os.path import join, getsize
import sys
import random
import asyncio
import time
from  datetime import datetime
from PIL import Image

from nonebot import get_bot
from nonebot.exceptions import CQHttpError

import hoshino
from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.typing import CQEvent

bot = get_bot()

_max = 50  #每人日调用上限(次)
_nlmt = DailyNumberLimiter(_max)

_cd = 3  #调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)

recall_pic = True  #是否撤回图片
PIC_SHOW_TIME = 40  #多少秒后撤回图片
circle_pic = True  #是否翻转图片

setu_path = "C:/Resources/img/setu/"  #填写你的本地涩图文件夹路径

sv_help = '''
本地涩图，基础版的涩图。图库质量高
- [来点好看的/来点好康的]
- [换弹夹]
- [检查本地涩图]
'''.strip()

sv = Service(
    name = '本地涩图',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助本地涩图"])
async def bangzhu_setu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

# 清理文件目录
def RemoveDir(filepath):
    '''
    如果文件夹不存在就创建，如果文件存在就清空！
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

# 获取文件目录大小
def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size

def countFile(dir):
    tmp = 0
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, item)):
            tmp += 1
        else:
            tmp += countFile(os.path.join(dir, item))
    return tmp

calltime = 0  #初始化调用次数

def set_callact(func):
    global calltime  #作为全局变量使用
    calltime = 0
    def count_callact():
        func()
        global calltime
        calltime += 1
    return count_callact

@set_callact
def callact_mark():  #调用次数记录
    pass

@sv.on_fullmatch(('检查本地setu', '检查本地涩图', '检查本地色图'))
async def check_setu_local(bot, ev):
    gid = ev['group_id']
    now = datetime.now()  #获取当前时间
    hour = now.hour  #获取当前时间小时数
    minute = now.minute  #获取当前时间分钟数
    now_date = time.strftime("%Y-%m-%d", time.localtime()) #获取当前日期
    hour_str = f' {hour}' if hour<10 else str(hour)
    minute_str = f' {minute}' if minute<10 else str(minute)
    image_api = await bot.can_send_image()  #检查是否能发送图片
    image_check = image_api.get('yes')
    image_all_num = countFile(setu_path)   #获取涩图路径下所有文件数量
    if not priv.check_priv(ev, priv.ADMIN):
        sv.logger.warning(f"来自群：{gid}的非管理者：{ev.user_id}尝试于{now_date}{hour_str}点{minute_str}分检查本地色图")
        await bot.send(ev, '一般通过群友不需要看这个啦，让管理员来试试看吧')
        return

    text1 = f"【发送权限检查】：\n是否能发送图片:{image_check}"
    text2 = f"【数据存储检查】：\n截止{now_date}，本地涩图的存量为:{image_all_num}张"
    SETU_SETUP_TEXT = f"【涩图设定情况】：\n当前bot主人设置的日上限为：{_max}次\n调用冷却为：{_cd}s\n是否撤回图片：{recall_pic}\n{PIC_SHOW_TIME}s后撤回图片\n是否启用图片翻转：{circle_pic}"
    CALLACT_TEXT = f"监测函数名：setu\n当前时间{now_date}{now}\n自HoshinoBot上次启动以来，setu已被调用{calltime}次。\n#注意：此调用次数非本群次数，是bot所有使用者的公共次数"
    
    checkfile = text1 + '\n' + text2
    checksetu = SETU_SETUP_TEXT + '\n' + CALLACT_TEXT

    await bot.send(ev, checkfile)
    time.sleep(2)
    await bot.send(ev, checksetu)

setu_folder = R.img('setu/').path

def setu_gener():
    dir_save = f"{setu_path}cache/"
    while True:
        filelist = os.listdir(setu_folder)
        random.shuffle(filelist)
        for filename in filelist:
            if os.path.isfile(os.path.join(setu_folder, filename)):
                if circle_pic is True:
                    pri_image = Image.open(f"{setu_path}{filename}")
                    tmppath = dir_save + filename
                    pri_image.rotate(180).save(tmppath)  #图片翻转180°
                    yield R.img('setu/cache/', filename)
                else:
                    yield R.img('setu/', filename)

setu_gener = setu_gener()

def get_setu():
    return setu_gener.__next__()

@sv.on_fullmatch(('来点好看的', '来点好康的'))
async def setu(bot, ev):
    uid = ev['user_id']
    now = datetime.now()  #获取当前时间
    hour = now.hour  #获取当前时间小时数
    minute = now.minute  #获取当前时间分钟数
    hour_str = f' {hour}' if hour<10 else str(hour)
    minute_str = f' {minute}' if minute<10 else str(minute)
    if not _nlmt.check(uid):
        EXCEED_NOTICE = f'截止{hour_str}点{minute_str}分，您已经冲过{_max}次了，请明日再来或请求群管重置次数哦！'
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, f"您冲得太快了，有{_cd}秒冷却哦", at_sender=True)
        return
    
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    pic = get_setu()

    try:
        if recall_pic == True:  #简陋的是否撤回判断
            callact_mark()  #引入记录
            msg = await bot.send(ev, pic.cqcode)
            recall = await bot.send(ev, f"{PIC_SHOW_TIME}s后将撤回图片")

            await asyncio.sleep(PIC_SHOW_TIME)

            await bot.delete_msg(message_id=msg['message_id'])
            await bot.delete_msg(message_id=recall['message_id'])
        else:
            await bot.send(ev, pic.cqcode)
    
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ev, '涩图太涩，发不出去勒...')
        except:
            pass

@sv.on_fullmatch(["清理涩图缓存", "清除setu", "清理本地涩图缓存", "清理setu", "清除涩图缓存"])
async def remove_setucache(bot, ev):
    path = f"{setu_path}cache/"
    shots_all_num = countFile(str(setu_path+"cache/"))  #同上
    shots_all_size = getdirsize(f"{setu_path}cache/")  #同上
    all_size_num = '%.3f' % (shots_all_size / 1024 / 1024)
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    hour_str = f' {hour}' if hour<10 else str(hour)
    minute_str = f' {minute}' if minute<10 else str(minute)
    if not priv.check_priv(ev, priv.SUPERUSER):   #建议使用priv.SUPERUSER
        sv.logger.warning(f"{ev.user_id}尝试于{hour_str}点{minute_str}分清除服务器全屏截图, 已拒绝")
        not_allowed_msg = f"权限不足。"  #权限不足时回复的消息
        await bot.send(ev, not_allowed_msg, at_sender=True)
        return
    else:
        info_before = f"当前翻转处理过的涩图有{shots_all_num}张，占用{all_size_num}Mb\n即将进行清理。"
        await bot.send(ev, info_before)

        RemoveDir(path)  #清理文件目录

        after_size = getdirsize(f"{setu_path}cache/")  #同上
        after_num = '%.3f' % (after_size / 1024 / 1024)
        info_after = f"清理完成。当前占用{after_num}Mb"
        sv.logger.warning(f"超级用户{ev.user_id}于{hour_str}点{minute_str}分清空涩图缓存")
        await bot.send(ev, info_after)

svsc = Service(name = '_setu_cache_',use_priv = priv.NORMAL,manage_priv = priv.SUPERUSER,visible = False,enable_on_default = True,bundle = 'advance',help_ = '定时清理涩图缓存')
@svsc.scheduled_job('cron', hour='20', minute='00')  #每天20点定时清理
async def clean_cache_auto():
    path = f"{setu_path}cache/"
    RemoveDir(path)
    sv.logger.error(f"定时清理本地涩图缓存已执行")


#群管理自助重置日上限（可以给自己重置，可以@多人）
@sv.on_prefix(('换肾', '补肾', '换弹夹', '换蛋夹'))
async def resetsetu(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):  #权限：ADMIN, 可以改成SUPERUSER防止滥用
        await bot.send(ev, '您的权限不足！请联系群管哦~')
        return
    count = 0
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            uid = int(m.data['qq'])
            _nlmt.reset(uid)
            count += 1
    if count:
        await bot.send(ev, f"已为{count}位用户重置次数！注意身体哦～")