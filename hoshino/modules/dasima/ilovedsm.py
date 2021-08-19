import os
import random
import re
import urllib
import requests

from nonebot import on_command
from nonebot.exceptions import CQHttpError

from hoshino import R, Service, priv, util
from hoshino.typing import CQEvent

from hoshino.util import FreqLimiter, DailyNumberLimiter
from . import dasima_list

_max = 20
EXCEED_NOTICE = f'今天已经发病了{_max}次了~明天再来吧!'
_nlmt = DailyNumberLimiter(_max)

sv_help = '''
大司马发病评论
- [发病] 随机一条
- [注入金轮] 重置发病次数
'''.strip()

sv = Service(
    name = '发病评论',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助发病评论", "帮助dasima", "dasima帮助"])
async def bangzhu_dasima(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_fullmatch(('注入金轮'))
async def dsmpowerup(bot, ev: CQEvent):
    uid = ev['user_id']
    _nlmt.reset(uid)
    await bot.send(ev, f"好耶!")

@sv.on_fullmatch(('发病', '大司马'))
async def dsmmylove(bot, ev):
    text = dasima_list.Dasima_Comments
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    final = random.choice(text)
    await bot.send(ev, final)
