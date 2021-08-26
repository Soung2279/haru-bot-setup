# -*- coding: utf-8 -*-
from time import time
import requests, asyncio, os, random, time
from nonebot.exceptions import CQHttpError
import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.typing import CQEvent, MessageSegment

from operator import __iadd__

from hoshino.util import FreqLimiter, DailyNumberLimiter

from . import chara
from . import _song_data,_record_data


_max = 1    # 用作判断使用者是否为首次使用，如果是首次使用会发送BGM来提升体验（bushi
_nlmt = DailyNumberLimiter(_max)
_cd = 5 # 调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)

Wiki_Menu_Record_img = R.img(f"musewiki/etc/IconVolume.png").cqcode
main_path = hoshino.config.RES_DIR  #使用在 _bot_.py 里填入的资源库文件夹

sv_help = '''
    ※MuseDash百科-语音查询※
当前菜单有以下内容：
    - 角色语音查询 -
- [摸摸+角色皮肤名]  摸摸角色的头(。・・)ノ
- [打打+角色名]  打一下角色（好过分ヽ(*。>Д<)o゜）
- [随机角色语音]  随便听一句
    - demo查询 -
- [peropero]  随机播放一条起始(peropero~games~)语音
- [随机demo]  随便听一首demo
    - 游戏音效查询 - 
- [随机游戏音效]  随便听听
- [听听好东西]  听一点MD玩家都喜欢听的

或发送以下指令进入其它菜单：
- [帮助md百科]
- [帮助百科资料查询]
- [帮助百科插图查询]
- [帮助百科成就查询]
- [帮助百科角色查询]
- [帮助百科歌曲推送]
'''.strip()

sv = Service(
    name = 'MuseDash百科-语音查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

def get_voice_record_menu():
    filename = 'MD OP.wav'  # 初次使用时发送的BGM文件名
    voice_rec = R.get('record/musewiki/audioclip/', filename)
    return voice_rec

@sv.on_fullmatch(["帮助MuseDash百科-语音查询", "帮助百科语音查询"])
async def bangzhu_musewiki_record(bot, ev) -> MessageSegment:
    file = get_voice_record_menu()
    voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, f"欢迎继续使用MuseDash百科-语音查询！")
    else:
        await bot.send(ev, voice_rec)

    _nlmt.increase(uid)
    final_output = Wiki_Menu_Record_img + sv_help
    await bot.send(ev, final_output)


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

nekovc_folder = "musewiki/角色语音/NEKO/游戏主播/触摸语音/"
yumevc_folder = "musewiki/角色语音/柚梅/领航员/触摸语音/"
jkvc_folder = "musewiki/角色语音/布若/制服少女/触摸语音/"
jokervc_folder = "musewiki/角色语音/布若/华服小丑/触摸语音/"
pilot_folder = "musewiki/角色语音/布若/飞行员/触摸语音/"
idol_folder = "musewiki/角色语音/布若/偶像/触摸语音/"
zombie_folder = "musewiki/角色语音/布若/僵尸少女/触摸语音/"
rockvc_folder = "musewiki/角色语音/凛/贝斯手/触摸语音/"
workervc_folder = "musewiki/角色语音/凛/打工战士/触摸语音/"
sleepyvc_folder ="musewiki/角色语音/凛/梦游少女/触摸语音/"
santavc_folder = "musewiki/角色语音/凛/圣诞礼物/触摸语音/"
bunnyvc_folder = "musewiki/角色语音/凛/兔女郎/触摸语音/"
rampagevc_folder = "musewiki/角色语音/凛/问题少女/触摸语音/"
blackvc_folder = "musewiki/角色语音/玛莉嘉/黑衣少女/触摸语音/"
magicvc_folder = "musewiki/角色语音/玛莉嘉/魔法少女/触摸语音/"
violinvc_folder = "musewiki/角色语音/玛莉嘉/提琴少女/触摸语音/"
evilvc_folder = "musewiki/角色语音/玛莉嘉/小恶魔/触摸语音/"
maidvc_folder = "musewiki/角色语音/玛莉嘉/女仆/触摸语音/"

neko_hurt_folder = "musewiki/角色语音/NEKO/通用受伤音效/"
yume_hurt_folder = "musewiki/角色语音/柚梅/通用受伤音效/"
rin_hurt_folder = "musewiki/角色语音/凛/通用受伤音效/"
buro_hurt_folder = "musewiki/角色语音/布若/通用受伤音效/"
marija_hurt_folder = "musewiki/角色语音/玛莉嘉/通用受伤音效/"


@sv.on_prefix(('摸摸'))
async def wiki_send_record(bot, ev: CQEvent):
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, f"不能一直摸哦~会长不高的！再等{_cd}秒吧", at_sender=True)
        return
    _flmt.start_cd(uid)
    input = ev.message.extract_plain_text()
    if not input:
        await bot.send(ev, "不告诉我名字要怎么摸辣！呐，给你做个示范：【摸摸 飞行员布若】")
        return
    if input == "布若" or input == "buro" or input == "凛" or input == "rin" or input == "玛莉嘉" or input == "marija":  #联动角色NEKO和柚梅因为目前是唯一的，所以不做前缀判断，如果游戏后续出了新的角色皮肤，需要在此行进行修改。
        await bot.send(ev, f'角色有很多衣服啦，要告诉我是哪个皮肤哦！\n给你做个示范：【摸摸 游戏主播neko】')
        return
    else:
        if input == "游戏主播NEKO#ФωФ" or input == "游戏主播neko" or input == "NEKO#ФωФ" or input == "neko":#联动目前唯一所以可直接匹配名称
            voice_data = _record_data.NEKO_VOICE  # 字典NEKO_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{nekovc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "领航员柚梅" or input == "柚梅" or input == "yume":#联动目前唯一所以可直接匹配名称
            voice_data = _record_data.YUME_VOICE  # 字典YUME_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{yumevc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "制服少女布若" or input == "制服少女":
            voice_data = _record_data.JK_VOICE  # 字典JK_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{jkvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "华服小丑布若" or input == "华服小丑":
            voice_data = _record_data.JOKER_VOICE  # 字典JOKER_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{jokervc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "飞行员布若" or input == "飞行员":
            voice_data = _record_data.PILOT_VOICE  # 字典PILOT_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{pilot_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "偶像布若" or input == "偶像":
            voice_data = _record_data.IDOL_VOICE  # 字典IDOL_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{idol_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "僵尸少女布若" or input == "僵尸少女":
            voice_data = _record_data.ZOMBIE_VOICE  # 字典ZOMBIE_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{zombie_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "贝斯手凛" or input == "贝斯手":
            voice_data = _record_data.ROCK_VOICE  # 字典ROCK_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{rockvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "打工战士凛" or input == "打工战士":
            voice_data = _record_data.WORKER_VOICE  # 字典WORKER_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{workervc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "梦游少女凛" or input == "梦游少女":
            voice_data = _record_data.SLEEPY_VOICE  # 字典SLEEPY_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{sleepyvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "圣诞礼物凛" or input == "圣诞礼物":
            voice_data = _record_data.SANTA_VOICE  # 字典SANTA_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{santavc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "兔女郎凛" or input == "兔女郎":
            voice_data = _record_data.BUNNY_VOICE  # 字典BUNNY_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{bunnyvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "问题少女凛" or input == "问题少女":
            voice_data = _record_data.RAMPAGE_VOICE  # 字典RAMPAGE_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{rampagevc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "黑衣少女玛莉嘉" or input == "黑衣少女":
            voice_data = _record_data.BLACK_VOICE  # 字典BLACK_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{blackvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "魔法少女玛莉嘉" or input == "魔法少女":
            voice_data = _record_data.MAGIC_VOICE  # 字典MAGIC_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{magicvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "提琴少女玛莉嘉" or input == "提琴少女":
            voice_data = _record_data.VIOLIN_VOICE  # 字典VIOLIN_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{violinvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "小恶魔玛莉嘉" or input == "小恶魔":
            voice_data = _record_data.EVIL_VOICE  # 字典EVIL_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{evilvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return
        if input == "女仆玛莉嘉" or input == "女仆":
            voice_data = _record_data.MAID_VOICE  # MAID_VOICE
            filename = random.choice(list(voice_data))
            text = voice_data[filename]
            rrec = R.rec(f"{maidvc_folder}{filename}").cqcode
            await bot.send(ev, rrec)
            await bot.send(ev,text)
            return

all_voice_folder = [nekovc_folder,yumevc_folder,jkvc_folder,jokervc_folder,pilot_folder,idol_folder,zombie_folder,rockvc_folder,workervc_folder,sleepyvc_folder,santavc_folder,bunnyvc_folder,rampagevc_folder,blackvc_folder,magicvc_folder,violinvc_folder,evilvc_folder]

@sv.on_fullmatch(["随机角色语音"])
async def random_send_voice(bot, ev):
    ranvoice_folder = random.choice(all_voice_folder)
    final_fd = str(main_path+'record/'+ranvoice_folder)
    uid = ev['user_id']
    filelist = os.listdir(final_fd)
    path = None
    while not path or not os.path.isfile(path):
        filename = random.choice(filelist)
        path = os.path.join(final_fd, filename)
    if not _flmt.check(uid):
        await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
        return
    _flmt.start_cd(uid)

    try:
        await bot.send(ev, f'[CQ:record,file=file:///{path}]')
    except CQHttpError:
        sv.logger.error(f"发送随机角色语音失败")
        try:
            await bot.send(ev, '(；′⌒`)发送失败了捏')
        except:
            pass

@sv.on_prefix(('打打'))
async def wiki_send_hurt(bot, ev: CQEvent):
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, f"好痛！让我缓一会儿嘛！再等{_cd}秒吧", at_sender=True)
        return
    _flmt.start_cd(uid)
    input = ev.message.extract_plain_text()
    if not input:
        await bot.send(ev, f"对着空气出拳...噗哈哈哈哈哈")
        return
    else:
        if input == "NEKO#ФωФ" or input == "neko":
            final_fd = str(main_path+'record/'+neko_hurt_folder)
            filelist = os.listdir(final_fd)
            path = None
            while not path or not os.path.isfile(path):
                filename = random.choice(filelist)
                path = os.path.join(final_fd, filename)
            try:
                await bot.send(ev, f'[CQ:record,file=file:///{path}]')
            except CQHttpError:
                sv.logger.error(f"发送record失败")
            return
        if input == "柚梅" or input == "yume":
            final_fd = str(main_path+'record/'+yume_hurt_folder)
            filelist = os.listdir(final_fd)
            path = None
            while not path or not os.path.isfile(path):
                filename = random.choice(filelist)
                path = os.path.join(final_fd, filename)
            try:
                await bot.send(ev, f'[CQ:record,file=file:///{path}]')
            except CQHttpError:
                sv.logger.error(f"发送record失败")
            return
        if input == "布若" or input == "buro":
            final_fd = str(main_path+'record/'+buro_hurt_folder)
            filelist = os.listdir(final_fd)
            path = None
            while not path or not os.path.isfile(path):
                filename = random.choice(filelist)
                path = os.path.join(final_fd, filename)
            try:
                await bot.send(ev, f'[CQ:record,file=file:///{path}]')
            except CQHttpError:
                sv.logger.error(f"发送record失败")
            return
        if input == "凛" or input == "rin":
            final_fd = str(main_path+'record/'+rin_hurt_folder)
            filelist = os.listdir(final_fd)
            path = None
            while not path or not os.path.isfile(path):
                filename = random.choice(filelist)
                path = os.path.join(final_fd, filename)
            try:
                await bot.send(ev, f'[CQ:record,file=file:///{path}]')
            except CQHttpError:
                sv.logger.error(f"发送record失败")
            return
        if input == "玛莉嘉" or input == "marija":
            final_fd = str(main_path+'record/'+marija_hurt_folder)
            filelist = os.listdir(final_fd)
            path = None
            while not path or not os.path.isfile(path):
                filename = random.choice(filelist)
                path = os.path.join(final_fd, filename)
            try:
                await bot.send(ev, f'[CQ:record,file=file:///{path}]')
            except CQHttpError:
                sv.logger.error(f"发送record失败")
            return


@sv.on_fullmatch(["随机游戏音效"])  #比较鸡肋的功能，若不需要可自行删除
async def random_send_audioclip(bot, ev):
    audioclip_folder = str(main_path+'record/musewiki/etc/')
    uid = ev['user_id']
    filelist = os.listdir(audioclip_folder)
    path = None
    if not _flmt.check(uid):
        await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
        return
    _flmt.start_cd(uid)
    while not path or not os.path.isfile(path):
        filename = random.choice(filelist)
        path = os.path.join(audioclip_folder, filename)
    try:
        await bot.send(ev, f'[CQ:record,file=file:///{path}]')
    except CQHttpError:
        sv.logger.error(f"发送record失败")
    

@sv.on_fullmatch(["听听好东西"])
async def random_send_faovr(bot, ev):
    faovr_folder = str(main_path+'record/musewiki/favor/')
    uid = ev['user_id']
    filelist = os.listdir(faovr_folder)
    path = None
    if not _flmt.check(uid):
        await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
        return
    _flmt.start_cd(uid)
    while not path or not os.path.isfile(path):
        filename = random.choice(filelist)
        path = os.path.join(faovr_folder, filename)
    try:
        await bot.send(ev, f'[CQ:record,file=file:///{path}]')
    except CQHttpError:
        sv.logger.error(f"发送record失败")

voice_folder_title = R.get('record/musewiki/title/').path

def get_voice_title():
    files = os.listdir(voice_folder_title)
    filename = random.choice(files)
    voice_rec = R.get('record/musewiki/title/', filename)
    return voice_rec

@sv.on_fullmatch(['peropero', 'muse标题语音', 'musedash标题语音'])
async def wiki_voice_title(bot, ev) -> MessageSegment:
    file = get_voice_title()
    try:
        voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
        await bot.send(ev, voice_rec)
    except CQHttpError:
        sv.logger.error("MuseDash百科-资料查询-随机标题语音发送失败。")