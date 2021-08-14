import requests, asyncio, os, time
from asyncio import events
from nonebot.exceptions import CQHttpError
import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.typing import CQEvent, MessageSegment
from . import chara
from hoshino.modules.musedash import _song_data
from operator import __iadd__
from hoshino.util import FreqLimiter, escape, DailyNumberLimiter

_max = 1
_nlmt = DailyNumberLimiter(_max)

Wiki_Menu_Achievement_img = R.img(f"musewiki/etc/achieve.png").cqcode
Wiki_show_Achieve_img_1 = R.img(f"musewiki/etc/SprTrophy.png").cqcode
Wiki_show_Achieve_img_2 = R.img(f"musewiki/etc/DiamomdTrophy0000.png").cqcode

sv_help = '''
※MuseDash百科-成就查询※

[查询成就]  进入查询菜单
[单曲成就查询]  查询单曲关卡成就
[游戏成就查询]  查询游戏成就
'''.strip()

sv = Service(
    name = 'MuseDash百科-成就查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

def get_voice_achieve_menu():
    filename = 'AchievementBgm.wav'
    voice_rec = R.get('record/musewiki/audioclip/', filename)
    return voice_rec

@sv.on_fullmatch(["帮助MuseDash百科-成就查询", "帮助百科成就查询"])
async def bangzhu_musewiki_achievement(bot, ev) -> MessageSegment:
    file = get_voice_achieve_menu()
    voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, f"欢迎继续使用MuseDash百科-成就查询！")
    else:
        await bot.send(ev, voice_rec)

    _nlmt.increase(uid)
    final_output = Wiki_Menu_Achievement_img + sv_help
    await bot.send(ev, final_output)

@sv.on_fullmatch(["查询成就", "成就查询"])
async def wiki_achievement_notice(bot, ev):
    await bot.send(ev, f'请输入查询的歌曲名，例如：【单曲成就查询 iyaiya】\n或者发送【查询游戏成就】来查看游戏成就列表')

# ID: [Song_Name, Belongs_Pack, Artist, Length, BPM, Level_To_Unlock, Difficulty_Sort, Highest_Difficulty, Search_Name, Designer, Achievements]
async def get_ach_info_from_song(ach):
    acg_data = _song_data.SONG_DATA[ach]
    Search_Name = acg_data[8]  #获取查询名，用于获取封面图片名称
    SongName = acg_data[0]  #获取歌曲原名
    Designer = acg_data[9]  #获取关卡设计
    Achievements = acg_data[10] #获取关卡成就

    Cover_Img = R.img(f"musewiki/songcover/{Search_Name}.png").cqcode

    song_cover = str(Cover_Img)

    ach_info_1 = f"※歌曲名：{SongName}\n※关卡设计：{Designer}"
    ach_info_2 = f"※关卡成就:\n {Achievements}"

    return ach_info_1, song_cover, ach_info_2, acg_data

def keyword_search_ach(keyword):
    ach_dict = _song_data.SONG_DATA
    result = []
    for ach in ach_dict:
        if keyword in ach_dict[ach][0] or keyword in ach_dict[ach][8]:  #获取歌曲原名和查询名，两个名字都可匹配，提高查询便利性
            result.append(ach)
    return result

@sv.on_prefix(('单曲成就查询'))
async def muse_wiki_achieve(bot, ev: CQEvent):
    s = ev.message.extract_plain_text()
    show_achieve = str(Wiki_show_Achieve_img_1)
    if not s:
        warn = f"请发送[单曲成就查询 歌名]~\n歌名不分大小写\n部分歌名支持呢称\n部分日文歌名支持中文汉字or罗马音\n例如：【单曲成就查询 无人区】"
        await bot.send(ev, warn)
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
        available_songs = keyword_search_ach(s)
        if not available_songs:
            await bot.send(ev, f'未找到含有关键词"{s}"的歌曲...')
            return
        elif len(available_songs) > 1:
            msg_part = '\n'.join(['• ' + song for song in available_songs])
            await bot.send(ev, f'从曲库中找到了这些:\n{msg_part}\n您想找的是哪首呢~')
            return
        else:
            ach_info_1, song_cover, ach_info_2, acg_data =  await get_ach_info_from_song(available_songs[0])

    final_msg = song_cover + ach_info_1 + show_achieve + ach_info_2  #合成单条消息
    await bot.send(ev, final_msg)


GAME_ACHIEVEMENT_1 = '''
MuseDash游戏目前有以下成就：

【第一次】  成功通关一个10级以上的关卡。
【弱者中的强者】  成功通关30个萌新难度关卡。
【中流砥柱】  成功通关30个高手难度关卡。
【你已经是大佬啦】  成功通关30个大触难度关卡。
【放弃治疗(隐藏)】  在不获得任何红心的前提下成功通关一个7级以上的关卡。
【这也行? (隐藏)】  在不击退任何敌人的前提下成功通关一个关卡。
【在哪里跌倒，就在哪里再次跌倒(隐藏)】  同一关卡的累计通关失败次数达到5。
【人生好艰难(隐藏)】  累计通关失败次数达到20。
【C】  取得10次“C”评价。
【B】  取得10次“B”评价。
【A】  取得10次“A”评价。
【S】  在一个10级以上的关卡中取得“S” 评价。
【Full Combo!!】  在一个10级以上的关卡中取得全连。
…………
'''.strip()

GAME_ACHIEVEMENT_2 = '''
【连击大师】  在80个不同的关卡中取得全连。
【就差一个(隐藏)】  成功通关一个7级以上的关卡，且仅“Miss” 一次。
【倒在终点(隐藏)】  在一个7级以上的关卡中通关失败，且恰好在最后一个敌人/障碍处“Miss” 时耗尽生命值。
【破五百!】  在一次游玩中取得500以上的最大连击数。
【见招拆招】  累计击退20000个敌人或BOSS远程攻击。
【贴身战斗】  累计击退200次BOSS近身攻击。
【SOLO】  累计完整演奏500个乐谱(长按)。
【躲闪大师】  累计躲避2000个障碍。
【意识流】  累计击退500个幽灵。
【爱可敌国】  累计收集500个红心。
【音符收集者】  累计收集500个音符。
【左右开弓】  在演奏乐谱 (长按)时累计击退500个敌人或BOSS远程攻击。
【小姐姐都是我的】  解锁12款角色皮肤
【我养你吧】  累计收集8只精灵
【插图收集】  累计收集10个插图
END.
'''.strip()

@sv.on_fullmatch(["查询游戏成就", "游戏成就查询"])
async def wiki_achievement_game(bot, ev):
    final_1 = Wiki_show_Achieve_img_2 + GAME_ACHIEVEMENT_1
    final_2 = Wiki_show_Achieve_img_2 + GAME_ACHIEVEMENT_2
    await bot.send(ev, final_1)
    time.sleep(5)
    await bot.send(ev, final_2)