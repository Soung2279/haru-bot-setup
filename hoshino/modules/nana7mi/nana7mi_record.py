# -*- coding: utf-8 -*-
from time import time
import requests, asyncio, os, random, time
from nonebot.exceptions import CQHttpError
import string
import hoshino
from hoshino import Service, priv, aiorequests, R, config
from hoshino.typing import CQEvent, MessageSegment

from operator import __iadd__

from hoshino.util import FreqLimiter, DailyNumberLimiter

from . import nana7mi_recore_data


_max = 30  #每日上限次数
_nlmt = DailyNumberLimiter(_max)
_cd = 5 # 调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)
MAX_WARN = f"今天已经听了{_max}条nana7mi了哦~~~建议直接去nana7mi直播间哦~"
CD_WARN = f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧"

SONG_LIST = nana7mi_recore_data.NANA7MI_SONGS_DATA
SEXY_LIST = nana7mi_recore_data.SEXY_NANA7MI_RECORD_DATA
TRAIN_LIST = nana7mi_recore_data.TRAIN_SONGS_DATA
OTTO_LIST = nana7mi_recore_data.OTTOLANGUAGE_NANA7MI_DATA

forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID

USE_BILIURL = True  #发送语音（优质二创）时是否附带发送原曲链接，True为附带False为不附带

sv_help = '''
♥~是可爱小七海捏~♥

- [来点不能转的/来点优质二创 + 编号（当前1-19）]   发一首娜娜米的优质二创，如果不加编号则随机发送

- [不能转的列表/娜娜米单曲列表]   查看优质二创列表

- [来点滑了/来点烧0娜娜米]   发一点娜娜米的怪叫合集（滑了~~嘿嘿~~嘿嘿） ##慎用！

- [来点小火车/来点铁轨难题]   发经典小火车，包括小火车的其它版本

- [来点古神语/]   发点娜娜米台词回古神语

- [来点可爱小七海]   随机发送语音，选取范围不含小火车/怪叫/二创/古神语

- [来点可爱大七海]   随机发送语音，选取范围包含所有项目

七海Nana7mi 主页：https://space.bilibili.com/434334701
'''.strip()

sv = Service(
    name = '可爱小七海',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'nana7mi', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助可爱小七海", "帮助小七海",])
async def bangzhu_nnm(bot, ev):
    await bot.send(ev, sv_help)

nana7mi_songs_folder = R.rec('nana7mi/精品单曲/').path   #鬼畜歌曲的文件路径
sexy_nana7mi_folder = R.rec('nana7mi/怪叫/').path    #怪叫合集的文件路径
train_folder = R.rec('nana7mi/小火车/').path     #各种小火车的文件路径
ottolanguage_nana7mi_folder = R.rec('nana7mi/古神语特辑/').path  #七海nana7mi特供古神语
record_nnm_folder = R.rec('nana7mi/切片语音').path  #各种切片语音
allnnm_folder = (nana7mi_songs_folder,sexy_nana7mi_folder,train_folder,ottolanguage_nana7mi_folder,record_nnm_folder)


@sv.on_prefix(("来点不能转的", "来点优质二创", "发点不能转的"))
async def send_nnmsongs(bot, ev: CQEvent):
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, CD_WARN, at_sender=True)
        return
    _flmt.start_cd(uid)
    input = ev.message.extract_plain_text()
    all_songs_count = int(len(SONG_LIST))
    search_range = range(1, all_songs_count)

    if not _nlmt.check(uid):
        data = {
            "type": "share",
            "data": {
                "url": "https://live.bilibili.com/21452505",
                "title": "七海Nana7mi的直播间 - 哔哩哔哩直播",
                "content": "每天晚上21:00开播 除了周一是24:00开播！"
                }
            }
        await bot.send(ev, MAX_WARN, at_sender=True)
        await bot.send(ev, data)
        return
    _nlmt.increase(uid)

    if input == '':  #不接参数时随机发送
        await bot.send(ev, "需要指定发送，请使用【不能转的列表】查看编号后，输入编号选取。例如：【来点不能转的2】", at_sender=True)
        songs_num = random.randint(1, all_songs_count)
        Song_name = SONG_LIST[songs_num][0]  #获取文件名
        Url = SONG_LIST[songs_num][1]  #获取原曲链接
        Title = SONG_LIST[songs_num][2]  #获取原视频标题    
        Content = SONG_LIST[songs_num][3]  #获取评价
        share_data_a = {
            "type": "share",
            "data": {
                "url": f"{Url}",
                "title": f"{Title}",
                "content": f"{Content}"
                }
            }
        songs_output_a = R.get('record/nana7mi/精品单曲/', Song_name)
        final_send = MessageSegment.record(f'file:///{os.path.abspath(songs_output_a.path)}')
        await bot.send(ev, final_send)
        if USE_BILIURL is True:
            await bot.send(ev, share_data_a)
        else:
            await bot.send(ev, f"对于此作品，我的评价是：{Content}")

    if input in search_range:  #当参数在编号范围内时
        nums = int(input)
        Song_name = SONG_LIST[nums][0]  #获取文件名
        Url = SONG_LIST[nums][1]  #获取原曲链接
        Title = SONG_LIST[nums][2]  #获取原视频标题    
        Content = SONG_LIST[nums][3]  #获取评价
        share_data_b = {
            "type": "share",
            "data": {
                "url": f"{Url}",
                "title": f"{Title}",
                "content": f"{Content}"
                }
            }
        songs_output_b = R.get('record/nana7mi/精品单曲/', Song_name)
        final_send = MessageSegment.record(f'file:///{os.path.abspath(songs_output_b.path)}')
        await bot.send(ev, final_send)
        if USE_BILIURL is True:
            await bot.send(ev, share_data_b)
        else:
            await bot.send(ev, f"对于此作品，我的评价是：{Content}")


@sv.on_fullmatch(["不能转的列表", "不能转的编号", "娜娜米单曲列表", "nana7mi单曲列表"])
async def idlist_song(bot, ev):
    vlist = []
    for k, v in SONG_LIST.items():
        vlist.append(k)
        vlist.append(v[2])
        vlist.append('################')
        final = f"{vlist}"  #粗糙的排版，能用就行OTZ
    await bot.send(ev, final)



@sv.on_fullmatch(["来点滑了", "来点烧0娜娜米", "来点烧0nana7mi", "来点入脑", "来点娜娜米怪叫", "来点nana7mi怪叫", "发点怪叫"])
async def send_nnmsexy(bot, ev) -> MessageSegment:
    uid = ev['user_id']
    record_api = await bot.can_send_record()  #检查是否能发送语音
    record_check = record_api.get('yes')
    if record_check is True:
        voice_name = random.choice(SEXY_LIST)  #随机取文件名
        sexy_rec = R.get('record/nana7mi/怪叫', voice_name)
    else:
        await bot.send(ev, f"bot无法发送语音，原因：/can_send_record = {record_check}")
        return

    if not _nlmt.check(uid):
        data = {
            "type": "share",
            "data": {
                "url": "https://live.bilibili.com/21452505",
                "title": "七海Nana7mi的直播间 - 哔哩哔哩直播",
                "content": "每天晚上21:00开播 除了周一是24:00开播！"
                }
            }
        await bot.send(ev, MAX_WARN, at_sender=True)
        await bot.send(ev, data)
        return
    _nlmt.increase(uid)

    try:
        final_send = MessageSegment.record(f'file:///{os.path.abspath(sexy_rec.path)}')
        await bot.send(ev, final_send)
        await bot.send(ev, voice_name)
    except CQHttpError:
        sv.logger.error("娜娜米怪叫语音发送失败。")


  
@sv.on_fullmatch(["来点小火车", "来点铁轨难题", "发点小火车"])
async def send_nnmtrain(bot, ev) -> MessageSegment:
    uid = ev['user_id']
    record_api = await bot.can_send_record()  #检查是否能发送语音
    record_check = record_api.get('yes')
    if record_check is True:
        voice_name = random.choice(TRAIN_LIST)  #随机取文件名
        train_rec = R.get('record/nana7mi/小火车', voice_name)
    else:
        await bot.send(ev, f"bot无法发送语音，原因：/can_send_record = {record_check}")
        return

    if not _nlmt.check(uid):
        data = {
            "type": "share",
            "data": {
                "url": "https://live.bilibili.com/21452505",
                "title": "七海Nana7mi的直播间 - 哔哩哔哩直播",
                "content": "每天晚上21:00开播 除了周一是24:00开播！"
                }
            }
        await bot.send(ev, MAX_WARN, at_sender=True)
        await bot.send(ev, data)
        return
    _nlmt.increase(uid)

    try:
        final_send = MessageSegment.record(f'file:///{os.path.abspath(train_rec.path)}')
        await bot.send(ev, final_send)
    except CQHttpError:
        sv.logger.error("小火车语音发送失败。")



@sv.on_fullmatch(["来点古神语", "来点otto语", "发点古神语"])
async def send_nnmotto(bot, ev) -> MessageSegment:
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, CD_WARN, at_sender=True)
        return
    _flmt.start_cd(uid)

    record_api = await bot.can_send_record()  #检查是否能发送语音
    record_check = record_api.get('yes')
    if record_check is True:
        voice_name = random.choice(OTTO_LIST)  #随机取文件名
        otto_rec = R.get('record/nana7mi/古神语特辑', voice_name)
    else:
        await bot.send(ev, f"bot无法发送语音，原因：/can_send_record = {record_check}")
        return

    if not _nlmt.check(uid):
        data = {
            "type": "share",
            "data": {
                "url": "https://live.bilibili.com/21452505",
                "title": "七海Nana7mi的直播间 - 哔哩哔哩直播",
                "content": "每天晚上21:00开播 除了周一是24:00开播！"
                }
            }
        await bot.send(ev, MAX_WARN, at_sender=True)
        await bot.send(ev, data)
        return
    _nlmt.increase(uid)

    try:
        final_send = MessageSegment.record(f'file:///{os.path.abspath(otto_rec.path)}')
        await bot.send(ev, final_send)
    except CQHttpError:
        sv.logger.error("小火车语音发送失败。")



@sv.on_fullmatch(["来点可爱小七海", "来点可爱娜娜米", "发点可爱小七海", "发点可爱娜娜米"])
async def send_nnmlove(bot, ev) -> MessageSegment:
    uid = ev['user_id']
    record_api = await bot.can_send_record()  #检查是否能发送语音
    record_check = record_api.get('yes')

    if not _nlmt.check(uid):
        data = {
            "type": "share",
            "data": {
                "url": "https://live.bilibili.com/21452505",
                "title": "七海Nana7mi的直播间 - 哔哩哔哩直播",
                "content": "每天晚上21:00开播 除了周一是24:00开播！"
                }
            }
        await bot.send(ev, MAX_WARN, at_sender=True)
        await bot.send(ev, data)
        return
    _nlmt.increase(uid)

    if record_check is True:
        filelist = os.listdir(record_nnm_folder)
        path = None
        while not path or not os.path.isfile(path):
            filename = random.choice(filelist)
            path = os.path.join(record_nnm_folder, filename)
            rec = R.rec(record_nnm_folder, filename).cqcode
            await bot.send(ev, rec)
            if random.random() < 0.08:  # 8%机率触发王喜顺彩蛋
                await bot.send(ev, R.rec('nana7mi/special/坐飞机去你的坟头疯狂的偷吃你的贡品.mp3').cqcode)
    else:
        await bot.send(ev, f"bot无法发送语音，原因：/can_send_record = {record_check}")
        return



@sv.on_fullmatch(["来点可爱大七海", "发点可爱大七海", "发点七海nana7mi", "来点七海nana7mi"])
async def send_random_allnnm(bot, ev: CQEvent):
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, CD_WARN, at_sender=True)
        return
    _flmt.start_cd(uid)

    if not _nlmt.check(uid):
        data = {
            "type": "share",
            "data": {
                "url": "https://live.bilibili.com/21452505",
                "title": "七海Nana7mi的直播间 - 哔哩哔哩直播",
                "content": "每天晚上21:00开播 除了周一是24:00开播！"
                }
            }
        await bot.send(ev, MAX_WARN, at_sender=True)
        await bot.send(ev, data)
        return

    _nlmt.increase(uid)
    select = random.choice(allnnm_folder)
    filelist = os.listdir(select)
    path = None
    while not path or not os.path.isfile(path):
        filename = random.choice(filelist)
        path = os.path.join(select, filename)
        rec = R.rec(select, filename).cqcode
        await bot.send(ev, rec)
        if random.random() < 0.08:  # 8%机率触发王喜顺彩蛋
            await bot.send(ev, R.rec('nana7mi/special/坐飞机去你的坟头疯狂的偷吃你的贡品.mp3').cqcode)