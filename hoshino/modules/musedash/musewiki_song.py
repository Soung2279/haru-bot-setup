# -*- coding: utf-8 -*-
from time import time
import requests, asyncio, os, random, time
from nonebot.exceptions import CQHttpError
from datetime import datetime
import pytz
import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.typing import CQEvent, MessageSegment

from operator import __iadd__

from hoshino.util import FreqLimiter, escape, DailyNumberLimiter
from . import chara  #改编自HoshinoBot自带的chara，感谢咖啡佬
from . import _song_data, wiki_log

tz = pytz.timezone('Asia/Shanghai')

_max = 1  #用作判断使用者是否为首次使用，如果是首次使用会发送BGM来提升体验（bushi
_nlmt = DailyNumberLimiter(_max)
_cd = 10  #调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)

Wiki_Menu_First_img = R.img(f"musewiki/etc/WelcomeLogo1.png").cqcode  #发送菜单时附带的图片，下同
Wiki_Menu_Second_img = R.img(f"musewiki/etc/WelcomeLogo2.png").cqcode

wiki_ver = wiki_log.wiki_ver  #从wiki_log.py里获取MuseDash百科的版本号，更新维护用的
tips_tuple = _song_data.Muse_Tips  #从_song_data.py里获取MuseDash的小提示，使用菜单时用的

sv_help = '''
    ※MuseDash百科※
欢迎使用MuseDash百科！当前菜单有以下内容：
    - 歌曲查询 -
- [详细查询+歌名]  详细查询单曲的各种信息，并发送对应的demo
- [随机歌曲信息]  随机查看一条歌曲信息

或发送以下指令进入其它菜单：
- [帮助百科资料查询]
- [帮助百科插图查询]
- [帮助百科成就查询]
- [帮助百科语音查询]
- [帮助百科角色查询]
- [帮助百科歌曲推送]
- [帮助百科运势]
'''.strip()

sv = Service(
    name = 'MuseDash百科-main',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

def get_voice_main_menu():
    filename = 'welcome_bgm.wav'  # 初次使用时发送的BGM文件名
    voice_rec = R.get('record/musewiki/audioclip/', filename)
    return voice_rec


@sv.on_fullmatch(["帮助MuseDash百科", "帮助musedashwiki", "帮助md百科", "musewiki帮助", "MuseDash百科"])
async def bangzhu_musewiki(bot, ev) -> MessageSegment:
    file = get_voice_main_menu()
    voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
    uid = ev['user_id']
    now_hour=datetime.now(tz).hour
    if not _flmt.check(uid):
        await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
        return
    _flmt.start_cd(uid)

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
        await bot.send(ev, greetings + tips)
    if not _nlmt.check(uid):  #如果是第一次使用（即首次发送命令：帮助musedashwiki）就发送对应的BGM
        await bot.send(ev, f"欢迎继续使用MuseDash百科！")
    else:
        await bot.send(ev, voice_rec)
    _nlmt.increase(uid)

    if random.random() < 0.50:  #有两张菜单图片，随机选择一张
        show_pic = Wiki_Menu_First_img
    else:
        show_pic = Wiki_Menu_Second_img
    
    final_output = show_pic + sv_help

    update_info = f'当前版本{wiki_ver}' #这个指令在wiki_log.py里面
    await bot.send(ev, final_output)
    time.sleep(2)  #避免长消息刷屏引起风控，等待2秒
    await bot.send(ev, update_info)


# ID: [Song_Name, Belongs_Pack, Artist, Length, BPM, Level_To_Unlock, Difficulty_Sort, Highest_Difficulty, Search_Name]
#上面辣么长一串英文是啥呢？其实是字典（_song_data.py）的格式，使用对应下标就可查询想要的内容，例如想要bot发送Artist(作者)，用下标[2]就可以读取辣（下标从0开始哦）
async def get_song_info_from_song(song):
    song_data = _song_data.SONG_DATA[song]
    Search_Name = song_data[8]  #获取查询名，用于获取封面图片名称
    SongName = song_data[0]  #获取歌曲原名
    Pack = song_data[1]  #获取来源曲包
    Artist = song_data[2]  #获取作者
    Length = song_data[3]  #获取时长
    Bpm = song_data[4]  #获取BPM
    Level_To_Unlock = song_data[5]  #获取解锁方式或等级
    Difficulty_Sort = song_data[6]  #获取难度分级
    Highest_Difficulty = song_data[7]  #获取最高难度

    Level_Stars = R.img(f"musewiki/level_stars/{Difficulty_Sort}.png").cqcode  #发送难度分级的图片路径
    Pack_Img = R.img(f"musewiki/pack/{Pack}.png").cqcode  #发送曲包图片路径
    Cover_Img = R.img(f"musewiki/songcover/{Search_Name}.png").cqcode  #发送歌曲封面路径
    Song_Demo = f'[CQ:record,file=file:///C:/Resources/record/musewiki/song_demos/{Search_Name}_demo.wav]'  #发送歌曲demo路径

    pack_cover= str(Pack_Img)
    song_cover = str(Cover_Img)
    song_level = str(Level_Stars)

    song_info_1 = f"※歌曲名：{SongName}\n※所属曲包：{Pack}"
    song_info_2 = f"※作者：{Artist}\n※时长：{Length}\n※每分钟节拍数(BPM)：{Bpm}\n※解锁方式or等级：{Level_To_Unlock}\n※难度分级：\n"
    song_info_3 = f"※最高难度：{Highest_Difficulty}"

    return song_cover, song_info_1, pack_cover, song_info_2, song_level, song_info_3, song_data, Song_Demo

def keyword_search(keyword):
    song_dict = _song_data.SONG_DATA
    result = []
    for song in song_dict:
        if keyword in song_dict[song][0] or keyword in song_dict[song][8]:  #获取歌曲原名和查询名，两个名字都可匹配，提高查询便利性
            result.append(song)
    return result


ADVANCE_NOTICE = '''
本功能支持部分呢称，简写，罗马音查询哦
如果还是查不到，请使用歌曲原名（不要问我日文怎么打啦）
如果还还还查不到，可以尝试使用官方Wiki上的歌曲名哦
'''.strip()
@sv.on_prefix(('详细查询'))
async def muse_wiki_advance(bot, ev: CQEvent):
    s = ev.message.extract_plain_text()
    if not s:
        await bot.send(ev, "不告诉我歌名要怎么查询啦！")
        if random.random() < 0.50:  #避免多人查询或者连续查询刷屏导致风控，故使用随机发送NOTICE。什么？你问我为什么要用随机？因为我太菜了QAQ（其实也想过用time.sleep()但是好像没啥用）
            await bot.send(ev, ADVANCE_NOTICE)
        return

    name = escape(ev.message.extract_plain_text().strip())
    id_ = chara.name2id(name)
    confi = 100
    guess = False
    c = chara.fromid(id_)
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
        guess = True
    c = chara.fromid(id_)
    if confi < 60:  #可能性设置，如果可能性低于设置的值则bot不会有所回应
        await bot.send(ev, "阿八阿八，是脸滚到键盘了嘛=  =。")
        return

    if guess:
        msg = f'没有找到歌曲"《{name}》"哦！可能是输入有误或未收录...\n（也可能是bot太笨了qaq'
        await bot.send(ev, msg)
        if random.random() < 0.50:
            await bot.send(ev, ADVANCE_NOTICE)
        msg = f'我猜您有{confi}%的可能在找{guess_name}哦'
        await bot.send(ev, msg)

    if s:
        available_songs = keyword_search(s)
        if not available_songs:
            return
        elif len(available_songs) > 1:
            msg_part = '\n'.join(['• %d'%song for song in available_songs])
            await bot.send(ev, f'好像有很多相似的歌曲哦~:\n{msg_part}\n您想找的是哪首呢~')
            return
        else:
            song_cover, song_info_1, pack_cover, song_info_2, song_level, song_info_3, song_data, Song_Demo = await get_song_info_from_song(available_songs[0])

    final_msg = song_cover + song_info_1 + pack_cover + song_info_2 + song_level + song_info_3 #合成单条文本消息
    await bot.send(ev, final_msg)
    await bot.send(ev, Song_Demo)  #发送歌曲demo


@sv.on_fullmatch(('随机歌曲信息'))
async def muse_wiki_song_push(bot, ev: CQEvent):
    my_dict = _song_data.SONG_DATA
    num = random.choice(list(my_dict))
    song_data = _song_data.SONG_DATA[num]
    SongName = song_data[0]  #获取歌曲原名
    s = SongName
    if s:
        available_songs = keyword_search(s)
        if not available_songs:  #如果bot随机的歌名不在曲库里面（当然不可能啦，除非字典有误
            await bot.send(ev, "bot坏掉惹...")
            return
        else:
            song_cover, song_info_1, pack_cover, song_info_2, song_level, song_info_3, song_data = await get_song_info_from_song(available_songs[0])

    final_msg = song_cover + song_info_1 + pack_cover + song_info_2 + song_level + song_info_3 #合成单条文本消息
    await bot.send(ev, final_msg)

svsong_help = '''
※百科歌曲推送※
- [启用百科歌曲推送]  每天下午1点推送
- [禁用百科歌曲推送]  禁用
'''.strip()

svsong = Service(
    name = '百科歌曲推送',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = False, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = svsong_help #帮助文本
    )

@sv.on_fullmatch(["帮助百科歌曲推送"])
async def bangzhu_push_songs(bot, ev):
    await bot.send(ev, svsong_help)

@svsong.scheduled_job('cron', hour='13', minute='00')  #每天下午1点推送
async def wiki_push_songs():
    bot = hoshino.get_bot()
    glist = await svsong.get_enable_groups()
    info_head = '今日份MuseDash歌曲推送'
    song_dict = _song_data.SONG_DATA
    random_name = random.choice(list(song_dict[0]))
    s = random_name
    if s:
        available_songs = keyword_search(s)
        if not available_songs:
            await bot.send(f'获取随机歌曲失败...')
            return
        else:
            song_cover, song_info_1, pack_cover, song_info_2, song_level, song_info_3, song_data, Song_Demo =  await get_song_info_from_song(available_songs[0])

    final_msg = song_cover + song_info_1 + pack_cover + song_info_2 + song_level + song_info_3 #合成单条消息
    for gid, selfids in glist.items():
        sid = random.choice(selfids)
        await bot.send_group_msg(self_id=sid, group_id=gid, message=info_head)
        await bot.send_group_msg(self_id=sid, group_id=gid, message=final_msg)
        #await bot.send_group_msg(self_id=sid, group_id=gid, message=Song_Demo) 如果需要发送demo，就取消注释这条。