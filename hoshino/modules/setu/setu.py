from asyncio import events
import os
import random
import asyncio

from nonebot.exceptions import CQHttpError

import hoshino
from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.typing import CQEvent

_max = 99
_nlmt = DailyNumberLimiter(_max)
#每人日调用上限
_cd = 3
_flmt = FreqLimiter(_cd)
#调用冷却
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明日再来或请求群管重置次数哦！'

recall_pic = True
#是否撤回图片

PIC_SHOW_TIME = 30
#多少秒后撤回图片

sv_help = '''
本地涩图，基础版的涩图。图库质量高
- [来点好看的/来点好康的]
- [查看本地涩图配置]  查看提供方配置设定
- [申请修改配置+描述]  向bot提供方申请修改配置
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

@sv.on_fullmatch(["查看本地涩图配置"])
async def setu_setup_notice(bot, ev):
    text_all = []
    text1 = '每日每人上限{_max}次'
    text2 = '调用冷却{_cd}s'
    text3 = '是否撤回图片{recall_pic}'
    text4 = '{PIC_SHOW_TIME}s后撤回图片'
    text_all = [text1, text2, text3, text4]
    await bot.send(ev, text_all)

_up_max = 3
lmt = DailyNumberLimiter(_up_max)
LIMIT_NOTICE = f'今天已经提交{_up_max}次，请勿滥用。'

@sv.on_prefix('申请修改配置')
async def setu_advice(bot, ev: CQEvent):
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.finish(LIMIT_NOTICE, at_sender=True)
    coffee = hoshino.config.SUPERUSERS[0]
    text = str(ev.message).strip()
    if not text:
        await bot.send(ev, f"请简述需要修改的配置", at_sender=True)
    else:
        await bot.send_private_msg(self_id=ev.self_id, user_id=coffee, message=f'本地涩图配置修改申请：{text}\n来自Q{uid}')
        await bot.send(ev, f'已上报给bot主人。\n======\n{text}')
        lmt.increase(uid)

setu_folder = R.img('setu/').path

def setu_gener():
    while True:
        filelist = os.listdir(setu_folder)
        random.shuffle(filelist)
        for filename in filelist:
            if os.path.isfile(os.path.join(setu_folder, filename)):
                yield R.img('setu/', filename)

setu_gener = setu_gener()

def get_setu():
    return setu_gener.__next__()


@sv.on_fullmatch(('来点好看的', '来点好康的'))
async def setu(bot, ev):
    """随机叫一份涩图，对每个用户有冷却时间"""
    uid = ev['user_id']
    if not _nlmt.check(uid):
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
            msg = await bot.send(ev, pic.cqcode)
            await bot.send(ev, f"{PIC_SHOW_TIME}后将撤回图片")
            await asyncio.sleep(PIC_SHOW_TIME)
            await bot.delete_msg(message_id=msg['message_id'])
        else:
            await bot.send(ev, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ev, '涩图太涩，发不出去勒...')
        except:
            pass


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