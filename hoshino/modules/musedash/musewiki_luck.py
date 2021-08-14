# -*- coding: utf-8 -*-
from time import time
import os, random, time
import hoshino
from nonebot.exceptions import CQHttpError
from datetime import datetime
import pytz
from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.typing import CQEvent, MessageSegment
from . import _song_data

tz = pytz.timezone('Asia/Shanghai')

_max = 2
_nlmt = DailyNumberLimiter(_max)

tips_tuple = _song_data.Muse_Tips  #从_song_data.py里获取MuseDash的小提示

sv_help = '''
    ※MuseDash百科-运势※
这是百科自带的小功能啦
- [md运势]  查看今天的md运势吧！
'''.strip()

sv = Service(
    name = 'MuseDash百科-运势',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助百科运势"])
async def bangzhu_wiki_lucky(bot, ev):
    await bot.send(ev, sv_help)


head_info = '今天的运势是：'
GradeA_img = R.img(f"musewiki/daily/GradeA.png").cqcode
sendA = str(GradeA_img)
lucky_word_A = '还不错？可以试着尝试一些没有尝试过的事情(*^▽^*)'
lucky_a = head_info + sendA + lucky_word_A

GradeB_img = R.img(f"musewiki/daily/GradeB.png").cqcode
sendB = str(GradeB_img)
lucky_word_B = '一般般吧，暂时不要做太依赖运气的事哦(o゜▽゜)o☆'
lucky_b = head_info + sendB + lucky_word_B

GradeC_img = R.img(f"musewiki/daily/GradeC.png").cqcode
sendC = str(GradeC_img)
lucky_word_C = '别灰心别灰心，一定会慢慢好起来的=￣ω￣='
lucky_c = head_info + sendC + lucky_word_C

GradeD_img = R.img(f"musewiki/daily/GradeD.png").cqcode
sendD = str(GradeD_img)
lucky_word_D = '呜哇...看来今天运气不佳呢ヽ(ﾟ∀ﾟ*)ﾉ'
lucky_d = head_info + sendD + lucky_word_D

GradeS_img = R.img(f"musewiki/daily/GradeS.png").cqcode
sendS = str(GradeS_img)
lucky_word_S = '今天运气爆棚！适合买彩票，抽卡等一切和运气有关的事情哦ㄟ(≧◇≦)ㄏ'
lucky_s = head_info + sendS + lucky_word_S

GradeGoldS_img = R.img(f"musewiki/daily/GradeGoldS.png").cqcode
sendGS = str(GradeGoldS_img)
lucky_word_GS = 'MD幸运之神的光芒照耀着你*★,°*:.☆(￣▽￣)/$:*.°★* 。'
lucky_gs = head_info + sendGS + lucky_word_GS

GradeSilverS_img = R.img(f"musewiki/daily/GradeSilverS.png").cqcode
sendSS = str(GradeSilverS_img)
lucky_word_SS = '哇嗷~~试着拿下新的FullCombo吧！ヽ(✿ﾟ▽ﾟ)ノ'
lucky_ss = head_info + sendSS + lucky_word_SS

lucky_all = (lucky_a,lucky_b,lucky_c,lucky_d,lucky_s,lucky_gs,lucky_ss)

faces_folder = R.img('musewiki/daily/faces/').path

def faces_gener():
    while True:
        filelist = os.listdir(faces_folder)
        random.shuffle(filelist)
        for filename in filelist:
            if os.path.isfile(os.path.join(faces_folder, filename)):
                yield R.img('musewiki/daily/faces/', filename)
faces_gener = faces_gener()
def get_faces():
    return faces_gener.__next__()

@sv.on_fullmatch(["md运势", "md抽签"])
async def wiki_lucky(bot, ev):
    uid = ev['user_id']
    now_hour = datetime.now(tz).hour
    now_date = time.strftime("%Y-%m-%d", time.localtime())
    if not _nlmt.check(uid):
        await bot.send(ev, f"欸！今天已经看过{_max}次了哦", at_sender=True)
        return
    _nlmt.increase(uid)
    if 0<=now_hour<6:  #凌晨
        greetings = f'(｡･∀･)ﾉﾞ凌晨好！今天是{now_date}哦'
        await bot.send(ev, greetings)
    elif 8<=now_hour<12:  #上午
        greetings = f'(((o(*ﾟ▽ﾟ*)o)))上午好！今天是{now_date}哦'
        await bot.send(ev, greetings)
    elif 12<=now_hour<14:  #中午
        greetings = f'(o゜▽゜)o☆中午好！今天是{now_date}哦'
        await bot.send(ev, greetings)
    elif 14<=now_hour<18:  #下午
        greetings = f'o(^▽^)o下午好！今天是{now_date}哦'
        await bot.send(ev, greetings)
    elif 18<=now_hour<21:  #晚上
        greetings = f'♪(´∇`*)晚上好！今天是{now_date}哦'
        await bot.send(ev, greetings)
    elif 21<=now_hour<24:  #深夜
        greetings = f'✧(≖ ◡ ≖✿)深夜好！今天是{now_date}哦'
        await bot.send(ev, greetings)
    else:
        greetings = f'\(@^０^@)/★你好！今天是{now_date}哦'
        await bot.send(ev, greetings)

    pic = get_faces()
    daily_luck = random.choice(lucky_all)
    tips = random.choice(tips_tuple)

    await bot.send(ev, daily_luck)
    await bot.send(ev, pic.cqcode + tips)