# -*- coding: utf-8 -*-
import ujson
import os
import random
import hoshino
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter, DailyNumberLimiter

_nlmt = DailyNumberLimiter(6)  #上限次数
_cd = 10  #调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)

sv_help = '''
土味情话
- [cp a b]  生成土味情话，a是攻，b是受
'''.strip()

sv = Service(
    name = '土味情话',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )
    
@sv.on_fullmatch(["帮助土味情话"])
async def bangzhu_cp(bot, ev):
    await bot.send(ev, sv_help)

path = os.path.dirname(__file__)

def readInfo(file):
    with open(os.path.join(path,file), 'r', encoding='utf-8') as f:
        return ujson.loads((f.read()).strip())

def getMessage(bot, userGroup):
    content = readInfo('content.json')
    content = random.choice(content['data']).replace('<攻>', userGroup[0]).replace('<受>', userGroup[1])
    return content

@sv.on_prefix(('cp', '土味情话'))
async def entranceFunction(bot, ev):
    non = ev.message.extract_plain_text()
    s = non.split(' ')
    uid = ev['user_id']
    if not uid in hoshino.config.SUPERUSERS:
        if not _flmt.check(uid):
            await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
            return
        if not _nlmt.check(uid):
            await bot.send(ev, f"避免重复使用导致刷屏，此消息已忽略")
            return
    if not non:
        await bot.send(ev, "要告诉我生成的对象名字哦！例如：[cp a b]")
        return
    try:
        name = s[0]
        name = s[1]
    except:
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    await bot.send(ev, getMessage(bot, s))