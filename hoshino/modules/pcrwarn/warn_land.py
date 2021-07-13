import os
import re
from datetime import datetime

import hoshino
from hoshino import Service, priv, R

svbl_help = '''
国服/台服买药提醒
'''.strip()

svbl = Service(
    name = '国台买药提醒',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = False, #是否默认启用
    bundle = '订阅', #属于哪一类
    help_ = svbl_help #帮助文本
    )

@svbl.on_fullmatch(["帮助国台买药提醒"])
async def bangzhu_pcrwanr(bot, ev):
    await bot.send(ev, svbl_help, at_sender=True)

@svbl.scheduled_job('cron', hour='6')
async def day1_reminder():
    msgs = [
        f'游戏商店内可以买经验药水了哦！\n快和我一起速速升级成为本群最强的骑士君吧！\n(1/4){R.img("yao.jpg").cqcode}\n', 
    ]
    await svbl.broadcast(msgs, 'day1_reminder')

@svbl.scheduled_job('cron', hour='12')
async def day2_reminder():
    msgs = [
        f'游戏商店内可以买经验药水了哦！\n快和我一起速速升级成为本群最强的骑士君吧！\n(2/4){R.img("yao.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'day2_reminder')

@svbl.scheduled_job('cron', hour='18')
async def day3_reminder():
    msgs = [
        f'游戏商店内可以买经验药水了哦！\n快和我一起速速升级成为本群最强的骑士君吧！\n(3/4){R.img("yao.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'day3_reminder')
    
@svbl.scheduled_job('cron', hour='23', minute='59')
async def day4_reminder():
    msgs = [
        f'游戏商店内可以买经验药水了哦！\n快和我一起速速升级成为本群最强的骑士君吧！\n(4/4){R.img("yao.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'day4_reminder')  

@svbl.scheduled_job('cron', hour='14', minute='40')
async def beici():
    msgs = [
        f'现在是北京时间14点40，距离竞技场结算还有20分钟哦！请注意！{R.img("randomimg/ma/ma5.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'beici')
    
@svbl.scheduled_job('cron', hour='5')
async def wakeup():
    msgs = [
        f'你醒了么~~我这就为您准备早餐！{R.img("randomimg/ma/ma2.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'wakeup') 

@svbl.scheduled_job('cron', hour='12')
async def tili1():
    msgs = [
        f'中午的游戏体力可以领取了哦！{R.img("randomimg/ma/ma17.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'tili1')     
    
@svbl.scheduled_job('cron', hour='18')
async def tili2():
    msgs = [
        f'下午的游戏体力可以领取了哦！{R.img("randomimg/ma/ma1.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'tili2') 
    
@svbl.scheduled_job('cron', hour='0', minute='30')
async def sleep():
    msgs = [
        f'已经12点半了哦~你也要早点休息！{R.img("randomimg/ma/ma13.jpg").cqcode}\n',
    ]
    await svbl.broadcast(msgs, 'sleep') 