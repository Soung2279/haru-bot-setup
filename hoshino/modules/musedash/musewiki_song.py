from time import time
import requests, asyncio, os, random, time
from nonebot.exceptions import CQHttpError
import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.modules.musedash import _song_data
from hoshino.typing import CQEvent, MessageSegment

from operator import __iadd__

from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter, escape, DailyNumberLimiter

from . import chara

_max = 1
_nlmt = DailyNumberLimiter(_max)
_cd = 10  #调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)

forward_msg_name = 'SoungBot测试版'
forward_msg_uid = '756160433'

Wiki_Menu_First_img = R.img(f"musewiki/etc/WelcomeLogo1.png").cqcode
Wiki_Menu_Second_img = R.img(f"musewiki/etc/WelcomeLogo2.png").cqcode

sv_help = '''
※MuseDash百科※
欢迎使用MuseDash百科！
※歌曲查询※
[详细查询+歌名]  详细查询单曲
[随机demo]  来一首随机demo

例如：详细查询 iyaiya

或发送以下指令进入额外查询分类：
[帮助百科资料查询]
[帮助百科插图查询]
[帮助百科成就查询]
[帮助百科角色查询]

建设中功能（暂不可用！）：
[查询联动]
[查询曲包]
[查询敌人]
[试听游戏歌曲]
[游戏冷知识]
'''.strip()

sv = Service(
    name = 'MuseDash百科',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

def get_voice_main_menu():
    filename = 'welcome_bgm.wav'
    voice_rec = R.get('record/musewiki/audioclip/', filename)
    return voice_rec

@sv.on_fullmatch(["帮助MuseDash百科", "帮助musedashwiki", "帮助musewiki", "musewiki帮助", "MuseDash百科"])
async def bangzhu_musewiki(bot, ev) -> MessageSegment:
    account = await bot.get_login_info()
    accid = account.get('user_id')
    check = str(accid)
    file = get_voice_main_menu()
    voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, f"欢迎继续使用MuseDash百科！")
    else:
        await bot.send(ev, voice_rec)

    _nlmt.increase(uid)
    if random.random() < 0.50:
        show_pic = Wiki_Menu_First_img
    else:
        show_pic = Wiki_Menu_Second_img
    
    final_output = show_pic + sv_help

    if check == '756160433':
        update_info = '百科当前为最新版本'
    else:
        update_info = ''
    await bot.send(ev, final_output)
    time.sleep(5)
    await bot.send(ev, update_info)
    

# ID: [Song_Name, Belongs_Pack, Artist, Length, BPM, Level_To_Unlock, Difficulty_Sort, Highest_Difficulty, Search_Name]
async def get_song_info_from_song(song):
    song_data = _song_data.SONG_DATA[song]
    Search_Name = song_data[8]  #获取查询名，用于获取封面图片名称
    SongName = song_data[0]  #获取歌曲原名
    Pack = song_data[1]  #获取来源曲包
    Artist = song_data[2]  #获取作者
    Length = song_data[3]  #获取时长
    Bpm = song_data[4]  #获取BPM
    Level_To_Unlock = song_data[5]  #获取解锁等级
    Difficulty_Sort = song_data[6]  #获取难度分级
    Highest_Difficulty = song_data[7]  #获取最高难度

    Level_Stars = R.img(f"musewiki/level_stars/{Difficulty_Sort}.png").cqcode
    Pack_Img = R.img(f"musewiki/pack/{Pack}.png").cqcode
    Cover_Img = R.img(f"musewiki/songcover/{Search_Name}.png").cqcode

    pack_cover= str(Pack_Img)
    song_cover = str(Cover_Img)
    song_level = str(Level_Stars)

    song_info_1 = f"※歌曲名：{SongName}\n※所属曲包：{Pack}"
    song_info_2 = f"※作者：{Artist}\n※时长：{Length}\n※每分钟节拍数(BPM)：{Bpm}\n※解锁等级：{Level_To_Unlock}\n※难度分级：\n"
    song_info_3 = f"※最高难度：{Highest_Difficulty}"

    return song_cover, song_info_1, pack_cover, song_info_2, song_level, song_info_3, song_data

def keyword_search(keyword):
    song_dict = _song_data.SONG_DATA
    result = []
    for song in song_dict:
        if keyword in song_dict[song][0] or keyword in song_dict[song][8]:  #获取歌曲原名和查询名，两个名字都可匹配，提高查询便利性
            result.append(song)
    return result

@sv.on_prefix(('详细查询'))
async def muse_wiki_advance(bot, ev: CQEvent):
    s = ev.message.extract_plain_text()
    if not s:
        await bot.send(ev, "请发送[详细查询 歌名]~\n歌名不分大小写", at_sender=True)
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
    if confi < 60:
        return
    
    if guess:
        msg = f'未找到"{name}"，可能是输入有误或未收录...'
        await bot.send(ev, msg)
        msg = f'您有{confi}%的可能在找{guess_name}'
        await bot.send(ev, msg)

    if s:
        available_songs = keyword_search(s)
        if not available_songs:
            await bot.send(ev, f'未找到含有关键词"{s}"的歌曲...')
            return
        elif len(available_songs) > 1:
            msg_part = '\n'.join(['• ' + song for song in available_songs])
            await bot.send(ev, f'从曲库中找到了这些:\n{msg_part}\n您想找的是哪首呢~')
            return
        else:
            song_cover, song_info_1, pack_cover, song_info_2, song_level, song_info_3, song_data =  await get_song_info_from_song(available_songs[0])

    final_msg = song_cover + song_info_1 + pack_cover + song_info_2 + song_level + song_info_3 #合成单条消息
    await bot.send(ev, final_msg)

#@sv.on_fullmatch(["xxx", "cxcx"])
#async def mainuie(bot, ev):
    #info_help = 'xxx'
    #mid = ev['message_id']
    #cq_message = f'[CQ:reply,id={mid}]'
    #data = await bot.get_login_info()
    #msg = data.get('user_id')
    #await bot.send(ev, msg)
    #finalmsg = cq_message + info_help
    #await bot.send(ev, finalmsg, at_sender=True)

demo_folder = R.get('record/musewiki/song_demos/').path

def get_random_demo():
    files = os.listdir(demo_folder)
    filename = random.choice(files)
    demo_rec = R.get('record/musewiki/song_demos/', filename)
    return demo_rec

@sv.on_fullmatch(["随机demo", "来点随机demo", "来点demo"])
async def wiki_send_random_demo(bot, ev) -> MessageSegment:
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, f"请等待{_cd}秒冷却", at_sender=True)
        return
    _flmt.start_cd(uid)

    file = get_random_demo()

    try:
        voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
        await bot.send(ev, voice_rec)
    except CQHttpError:
        sv.logger.error("MuseDash百科，随机demo发送失败。")