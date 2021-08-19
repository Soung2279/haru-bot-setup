# -*- coding: utf-8 -*-
import os
import random
import re
from nonebot import get_bot
from nonebot.exceptions import CQHttpError

from hoshino import R, Service, priv, util, config
from hoshino.typing import CQEvent, MessageSegment

from hoshino.util import DailyNumberLimiter
from . import voice_dict

bot = get_bot()

_max = 2  #每日上限次数
_nlmt = DailyNumberLimiter(_max)
bot_name = config.NICKNAME  #从config/__bot__.py里获取设定的bot呢称  
show_name = bot_name[0]  #*仅在 NICKNAME 为 元组(tuple) 的情况下可正常获取呢称，如果不是元组请直接在此处填写你的bot呢称
EXCEED_NOTICE = f"{show_name}今天已经使用了{_max}次爆裂魔法哦~~~明天再使用爆裂魔法吧!"

sv_help = f"“エクスプロージョン（Explosion）！”\n和{show_name}每天练习爆裂魔法吧！\n- [爆裂魔法] 来一发「Explosion」\n- [@bot补魔] 重置次数"

sv = Service(
    name = '爆裂魔法',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True,
    enable_on_default = True, #是否默认启用
    bundle = '娱乐',
    help_ = sv_help
    )

@sv.on_fullmatch(["帮助爆裂魔法", "帮助explosion", "explosion帮助"])
async def bangzhu_explosion(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_fullmatch(('exo', '爆裂魔法', '来一发', '爆烈魔法', '暴烈魔法'))
async def send_explosion(bot, ev) -> MessageSegment:
    uid = ev['user_id']
    voices = voice_dict.EXPLOSION_VOICE  #引入字典
    record_api = await bot.can_send_record()  #检查是否能发送语音
    record_check = record_api.get('yes')
    if record_check is True:
        voice_name = random.choice(list(voices.keys()))  #随机取文件名
        text = voices[voice_name]  #根据文件名获取对应文本
        explosion_rec = R.get('explosion/', voice_name)  # 在此处修改语音文件存放的路径（放置在Hoshinobot的资源路径下）
    else:
        await bot.send(ev, f"{show_name}无法发送语音，原因：can_send_record = {record_check}")
        return

    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return

    _nlmt.increase(uid)

    try:
        final_send = MessageSegment.record(f'file:///{os.path.abspath(explosion_rec.path)}')
        await bot.send(ev, final_send)
        await bot.send(ev, text)
    except CQHttpError:
        sv.logger.error("爆裂魔法语音发送失败。")

@sv.on_fullmatch(('补魔'), only_to_me=True)  #需@bot，可自行修改
async def exexplo(bot, ev: CQEvent):
    uid = ev['user_id']
    _nlmt.reset(uid)
    await bot.send(ev, f"谢谢你的魔力！{show_name}感觉又可以来一发了呢~")















