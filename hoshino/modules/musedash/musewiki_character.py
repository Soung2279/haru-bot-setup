# -*- coding: utf-8 -*-
from time import time
import requests, asyncio, os, time, random
from datetime import datetime
import pytz
import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.typing import CQEvent, MessageSegment
from hoshino.util import FreqLimiter, escape, DailyNumberLimiter
from operator import __iadd__

from . import _chip_data, _song_data

tz = pytz.timezone('Asia/Shanghai')

_max = 1
_nlmt = DailyNumberLimiter(_max)


Wiki_Menu_Character_img = R.img(f"musewiki/etc/muses.png").cqcode
Wiki_Menu_Chip_img = R.img(f"musewiki/etc/eflins.png").cqcode

tips_tuple = _song_data.Muse_Tips

sv_help = '''
    ※MuseDash百科※
当前菜单有以下内容：
    -角色&精灵查询-
- [查询角色]  查询游戏内角色
- [查询精灵]  查询游戏内精灵

或发送以下指令进入其它菜单：
- [帮助百科资料查询]
- [帮助百科插图查询]
- [帮助百科成就查询]
- [帮助百科语音查询]
- [帮助帮助md百科]
- [帮助百科歌曲推送]
- [帮助百科运势]
'''.strip()

sv = Service(
    name = 'MuseDash百科-角色查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

def get_voice_character_menu():
    filename = 'ElfinsBgm.wav'
    voice_rec = R.get('record/musewiki/audioclip/', filename)
    return voice_rec

@sv.on_fullmatch(["帮助MuseDash百科-角色查询", "帮助百科角色查询"])
async def bangzhu_musewiki_chip(bot, ev) -> MessageSegment:
    file = get_voice_character_menu()
    voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
    uid = ev['user_id']
    now_hour=datetime.now(tz).hour
    if 0<=now_hour<6:  #凌晨
        tips = random.choice(tips_tuple)
        greetings = '(｡･∀･)ﾉﾞ凌晨好！'
        await bot.send(ev, greetings + tips)
    elif 8<=now_hour<12:  #上午
        tips = random.choice(tips_tuple)
        greetings = '(((o(*ﾟ▽ﾟ*)o)))上午好！'
        await bot.send(ev, greetings + tips)
    elif 12<=now_hour<14:  #中午
        tips = random.choice(tips_tuple)
        greetings = '(o゜▽゜)o☆中午好！'
        await bot.send(ev, greetings + tips)
    elif 14<=now_hour<18:  #下午
        tips = random.choice(tips_tuple)
        greetings = 'o(^▽^)o下午好！'
        await bot.send(ev, greetings + tips)
    elif 18<=now_hour<21:  #晚上
        tips = random.choice(tips_tuple)
        greetings = '♪(´∇`*)晚上好！'
        await bot.send(ev, greetings + tips)
    elif 21<=now_hour<24:  #深夜
        tips = random.choice(tips_tuple)
        greetings = '✧(≖ ◡ ≖✿)深夜好！'
    if not _nlmt.check(uid):
        await bot.send(ev, f"欢迎继续使用MuseDash百科-角色查询！")
    else:
        await bot.send(ev, voice_rec)
    _nlmt.increase(uid)

    final_output = Wiki_Menu_Character_img + sv_help
    await bot.send(ev, final_output)

# No.: [name, description, skill, chipname, chipdescription]
async def get_chip_info_from_chip(chip):
    chip_data = _chip_data.CHIP_DATA[chip]
    Name = chip_data[0]  #获取精灵名称
    DESCRIPTION = chip_data[1]  #获取精灵描述
    SKILL = chip_data[2]  #获取技能
    CHIPNAME = chip_data[3]  #获取信物
    CHIPDESCRIPTION = chip_data[4]  #获取信物描述

    chippic = R.img(f"musewiki/chip/chip_pic/{Name}.png").cqcode
    chipgood = R.img(f"musewiki/chip/chip_goods/{CHIPNAME}.png").cqcode

    chip_image_cover = str(chippic)
    chip_goods_image = str(chipgood)

    chip_info_1 = f"精灵名：{Name}\n精灵描述：{DESCRIPTION}\n技能：{SKILL}\n"
    chip_info_2 = f"信物：{CHIPNAME}\n信物描述：{CHIPDESCRIPTION}"

    return chip_info_1, chip_image_cover, chip_info_2, chip_goods_image, chip_data

def keyword_search_chip(keyword):
    chip_dict = _chip_data.CHIP_DATA
    result = []
    for chip in chip_dict:
        if keyword in chip_dict[chip][0] or keyword in chip:
            result.append(chip)
    return result

@sv.on_prefix(('查询精灵'))
async def muse_wiki_chip(bot, ev: CQEvent):
    show_chips = str(Wiki_Menu_Chip_img)
    s = ev.message.extract_plain_text()
    if not s:
        await bot.send(ev, "请发送[查询精灵 精灵名]~\n精灵名需要完整匹配", at_sender=True)
        return
    if s:
        available_chips = keyword_search_chip(s)
        if not available_chips:
            await bot.send(ev, f'未找到含有关键词"{s}"的精灵...')
            return
        elif len(available_chips) > 1:
            msg_part = '\n'.join(['• ' + chip for chip in available_chips])
            await bot.send(ev, f'从资料库中找到了这些:\n{msg_part}\n您想找的是什么呢~')
            return
        else:
            chip_info_1, chip_image_cover, chip_info_2, chip_goods_image, chip_data =  await get_chip_info_from_chip(available_chips[0])

    final_msg = show_chips + '\n' + chip_image_cover + chip_info_1 + chip_goods_image + chip_info_2 #合成单条消息
    await bot.send(ev, final_msg)

# Name: [cosName, character, HP, description, skill, chipName, chipDescription, cv]
async def get_chara_info_from_chara(chara):
    chara_data = _chip_data.CHARA_DATA[chara]
    cosName = chara_data[0]  #获取皮肤名称
    character = chara_data[1]  #获取角色名
    HP = chara_data[2]  #获取血量
    description = chara_data[3]  #获取描述
    skill = chara_data[4]  #获取技能
    charaName =chara_data[5]  #获取信物
    chipDescription =chara_data[6]  #获取信物描述
    cv =chara_data[7]  #获取声优

    charapic = R.img(f"musewiki/chip/chara_pic/{cosName}.png").cqcode
    charagood = R.img(f"musewiki/chip/chara_goods/{charaName}.png").cqcode
    chara_bgm = f'[CQ:record,file=file:///C:/Resources/record/musewiki/角色语音/bgm/{cosName}.wav]'

    chara_image = str(charapic)
    chara_goods_image = str(charagood)

    

    chara_info_1 = f"角色名：{cosName}{character}\n初始血量：{HP}\n角色描述：{description}\n技能: {skill}\n"
    chara_info_2 = f"信物：{charaName}\n信物描述：{chipDescription}\n声优: {cv}"

    return chara_info_1, chara_image, chara_info_2, chara_goods_image, chara_data, chara_bgm

def keyword_search_chara(keyword):
    chara_dict = _chip_data.CHARA_DATA
    result = []
    for chara in chara_dict:
        if keyword in chara or keyword in chara_dict[chara][0]:
            result.append(chara)
    return result

@sv.on_prefix(('查询角色'))
async def muse_wiki_chara(bot, ev: CQEvent):
    s = ev.message.extract_plain_text()
    if not s:
        await bot.send(ev, "不告诉我名字要怎么查询啦！")
        return
    if s:
        available_charas = keyword_search_chara(s)
        if not available_charas:
            await bot.send(ev, f'没有找到叫"{s}"的角色哦')
            return
        elif len(available_charas) > 1:
            msg_part = '\n'.join(['• ' + chara for chara in available_charas])
            await bot.send(ev, f'好像有很多相似的名字哦~:\n{msg_part}\n您想找的是谁呢~')
            return
        else:
            chara_info_1, chara_image, chara_info_2, chara_goods_image, chara_data, chara_bgm =  await get_chara_info_from_chara(available_charas[0])

    final_msg = chara_image + chara_info_1 + chara_goods_image + chara_info_2 #合成单条消息
    await bot.send(ev, final_msg)
    await bot.send(ev, chara_bgm)