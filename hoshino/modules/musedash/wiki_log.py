# -*- coding: utf-8 -*-
from time import time
import re, os
import asyncio
import hoshino
import time
from nonebot import get_bot
from  datetime import datetime
from nonebot import on_command
from hoshino import Service, priv, config
from hoshino.typing import CQEvent
from . import _song_data, _chip_data

bot = get_bot()

SONG_DATA_LEN = _song_data.SONG_DATA
TIPS_DATA_LEN = _song_data.Muse_Tips
CHIP_DATA_LEN = _chip_data.CHIP_DATA
CHARA_DATA_LEN = _chip_data.CHARA_DATA

wiki_ver = '1.0.1'

sv = Service(
    name = '_MDWIKI_LOG_',
    use_priv = priv.NORMAL,
    manage_priv = priv.SUPERUSER,
    visible = False, #False隐藏
    enable_on_default = True,
    bundle = 'musedash',
    help_ = 'MD百科更新日志'
    )

MD_WIKI_LOG = '''
2021.8.15 bot更新日志
=====================
百科正常运行
版本：V1.0.1
=====================
'''.strip()

@sv.on_fullmatch(["查看百科更新", "检查百科更新", "百科github"])
async def check_github_wiki(bot, ev):
    now = datetime.now()  #获取当前时间
    hour = now.hour  #获取当前时间小时数
    minute = now.minute  #获取当前时间分钟数
    hour_str = f' {hour}' if hour<10 else str(hour)
    minute_str = f' {minute}' if minute<10 else str(minute)
    if not priv.check_priv(ev, priv.ADMIN):
        sv.logger.warning(f"非管理者：{ev.user_id}尝试于{hour_str}点{minute_str}分检查百科更新")
    account = await bot.get_login_info()
    accid = account.get('user_id')
    check = str(accid)
    data = {
        "type": "share",
        "data": {
            "url": "http://github.com/Soung2279",
            "title": "MuseDash百科@Github",
            "content": "HoshinoBot插件：MuseDash百科",
            }
        }
    if check == '756160433':
        await bot.send(ev, f"{MD_WIKI_LOG}")
    else:
        await bot.send(ev, data)


def countFile(dir):
    tmp = 0
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, item)):
            tmp += 1
        else:
            tmp += countFile(os.path.join(dir, item))
    return tmp

@sv.on_fullmatch(["检查百科文件", "查看百科文件"])
async def check_main_wiki(bot, ev):
    gid = ev['group_id']
    now = datetime.now()  #获取当前时间
    hour = now.hour  #获取当前时间小时数
    minute = now.minute  #获取当前时间分钟数
    now_date = time.strftime("%Y-%m-%d", time.localtime()) #获取当前日期
    hour_str = f' {hour}' if hour<10 else str(hour)
    minute_str = f' {minute}' if minute<10 else str(minute)
    image_api = await bot.can_send_image()
    record_api = await bot.can_send_record()
    image_check = image_api.get('yes')
    record_check = record_api.get('yes')
    all_songs = len(SONG_DATA_LEN)
    all_tips = len(TIPS_DATA_LEN)
    all_chips = len(CHIP_DATA_LEN)
    all_charas = len(CHARA_DATA_LEN)
    image_all_num = countFile("C:/Resources/img/musewiki/")
    image_artwork_num = countFile("C:/Resources/img/musewiki/artwork/")
    image_songcover_num = countFile("C:/Resources/img/musewiki/songcover/")
    record_all_num = countFile("C:/Resources/record/musewiki/")
    record_song_demos_num = countFile("C:/Resources/record/musewiki/song_demos/")
    record_title_num = countFile("C:/Resources/record/musewiki/title/")

    text1 = f"【发送权限检查】：\n是否能发送图片:{image_check}\n是否能发送语音:{record_check}"
    text2 = f"【数据存储检查】：\n已录入的歌曲数量:{all_songs}\n已录入的TIPS数量:{all_tips}\n已录入的角色数量:{all_chips}\n已录入的精灵数量:{all_charas}"
    text3 = f"截止{now_date}，百科存储的图片总数量:{image_all_num}\n其中插画有{image_artwork_num}张，歌曲封面有{image_songcover_num}张"
    text4 = f"截止{now_date}，百科存储的语音总数量:{record_all_num}\n其中试听歌曲有{record_song_demos_num}条，标题语音有{record_title_num}条"

    dict_len = text1 + '\n' + text2
    resources_len = text3 + '\n' + text4

    if not priv.check_priv(ev, priv.ADMIN):
        sv.logger.warning(f"来自群：{gid}的非管理者：{ev.user_id}尝试于{now_date}{hour_str}点{minute_str}分检查百科文件")
        await bot.send(ev, '一般通过群友不需要看这个啦，让管理员来试试看吧')
    await bot.send(ev, dict_len)
    await bot.send(ev, resources_len)
    if not image_songcover_num == all_songs:
        await bot.send(ev, '歌曲封面图片[songcover]缺失。请联系bot管理员补充资源')
    if not record_song_demos_num == all_songs:
        await bot.send(ev, '试听歌曲语音[song_demos]缺失。请联系bot管理员补充资源')