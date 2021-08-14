import requests, asyncio, os, random
from asyncio import events
from nonebot.exceptions import CQHttpError
import time
import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.typing import CQEvent, MessageSegment

from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter, DailyNumberLimiter

from . import chara

_max = 1
_nlmt = DailyNumberLimiter(_max)

forward_msg_name = 'SoungBot测试版'
forward_msg_uid = '756160433'

_cd = 300  #调用间隔冷却时间(s)  为避免被风控，建议调高
_flmt = FreqLimiter(_cd)

Wiki_Menu_Artwork_img = R.img(f"musewiki/etc/artwork.png").cqcode

sv_help = '''
※MuseDash百科-插图查询※

[查询插图]  进入插图查询菜单
[单/全图查询]  不同模式的插图查询
[动画查询]  查询游戏Live2D插画
[查询游戏场景]  进入游戏场景查询菜单
[纯/合成场景]  查看不同的场景图片
'''.strip()

sv = Service(
    name = 'MuseDash百科-插图查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

def get_voice_artwork_menu():
    filename = 'TroveBgm.wav'
    voice_rec = R.get('record/musewiki/audioclip/', filename)
    return voice_rec

@sv.on_fullmatch(["帮助MuseDash百科-插图查询", "帮助百科插图查询"])
async def bangzhu_musewiki_artwork(bot, ev) -> MessageSegment:
    file = get_voice_artwork_menu()
    voice_rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, f"欢迎继续使用MuseDash百科-插图查询！")
    else:
        await bot.send(ev, voice_rec)
    
    _nlmt.increase(uid)
    final_output = Wiki_Menu_Artwork_img + sv_help
    await bot.send(ev, final_output)


@sv.on_fullmatch(["查询插图", "插图查询"])
async def wiki_artwork_notice(bot, ev):
    await bot.send(ev, '请选择查询模式：单图查询/全图查询/动画查询')

@sv.on_fullmatch("单图查询")
async def wiki_artwork_menu(bot, ev):
    await bot.send(ev, '请按游戏内顺序查询：1-57，例如：单图查询1', at_sender=True)

@sv.on_fullmatch(["游戏场景查询", "muse场景查询", "查询游戏场景"])
async def wiki_image_scenes_menu(bot, ev):
    await bot.send(ev, f'请选择您要查询的场景。纯场景/合成场景。\n纯场景即不含游戏UI，场景对应敌人类型的图片，合成反之。\n例如：发送[纯场景]\n您也可以选择随机查看，指令【随机纯场景/合成场景】')

@sv.on_fullmatch(["纯场景", "纯场景查询", "查询纯场景"])
async def wiki_image_scenes_nogoods(bot, ev):
    await bot.send(ev, f"图片来源个人解包，原图可能较大\n请按游戏内序号选择1-7，如[纯场景1]", at_sender=True)

@sv.on_fullmatch(["合成场景", "合成场景查询", "查询合成场景"])
async def wiki_image_scenes_withgoods(bot, ev):
    await bot.send(ev, f"图片来源个人解包，原图可能较大\n请按游戏内序号选择1-7，如[合成场景1]", at_sender=True)

pic1 = R.img('musewiki/artwork/artwork(1).png').cqcode
sendpic1 = str(pic1)
title1 = '考试之后天台的3人。'
author1 = '画师：H2θ\n'
author_page1 = '画师主页：暂未收录'
text1 = title1 + sendpic1 + author1 + author_page1

pic2 = R.img('musewiki/artwork/artwork(2).png').cqcode
sendpic2 = str(pic2)
title2 = '我的心愿是征服世界~~~上的好吃的！'
author2 = '画师：UMU\n'
author_page2 = '画师主页：暂未收录'
text2 = title2 + sendpic2 + author2 + author_page2

pic3 = R.img('musewiki/artwork/artwork(3).png').cqcode
sendpic3 = str(pic3)
title3 = '当我睁开眼睛的时候你已经输了~'
author3 = '画师：H2θ\n'
author_page3 = '画师主页：暂未收录'
text3 = title3 + sendpic3 + author3 + author_page3

pic4 = R.img('musewiki/artwork/artwork(4).png').cqcode
sendpic4 = str(pic4)
title4 = '世界巡回演出。'
author4 = '画师：仲村原则\n'
author_page4 = '画师主页：https://m.weibo.cn/u/1953618075'
text4 = title4 + sendpic4 + author4 + author_page4

pic5 = R.img('musewiki/artwork/artwork(5).png').cqcode
sendpic5 = str(pic5)
title5 = '布若的私人衣柜。'
author5 = '画师：H2θ\n'
author_page5 = '画师主页：暂未收录'
text5 = title5 + sendpic5 + author5 + author_page5

pic6 = R.img('musewiki/artwork/artwork(6).png').cqcode
sendpic6 = str(pic6)
title6 = '啊啊玛莉嘉被吃掉啦！我不是叉烧啊！'
author6 = '画师：H2θ & Yu13\n'
author_page6 = '画师主页：H2θ：暂未收录\nYu13：https://m.weibo.cn/u/1747710857'
text6 = title6 + sendpic6 + author6 + author_page6

pic7 = R.img('musewiki/artwork/artwork(7).png').cqcode
sendpic7 = str(pic7)
title7 = '为了防止世界被破坏，少女们决定成为偶像。'
author7 = '画师：狸八\n'
author_page7 = '画师主页：https://m.weibo.cn/u/1921811972'
text7 = title7 + sendpic7 + author7 + author_page7

pic8 = R.img('musewiki/artwork/artwork(8).png').cqcode
sendpic8 = str(pic8)
title8 = '被拍下全校通报批评的照片。'
author8 = '画师：H2θ & Yu13\n'
author_page8 = '画师主页：H2θ：暂未收录\nYu13：https://m.weibo.cn/u/1747710857'
text8 = title8 + sendpic8 + author8 + author_page8

pic9 = R.img('musewiki/artwork/artwork(9).png').cqcode
sendpic9 = str(pic9)
title9 = '迟到的新年祝福！'
author9 = '画师：图乌吐\n'
author_page9 = '画师主页：twitter@thurim6'
text9 = title9 + sendpic9 + author9 + author_page9

pic10 = R.img('musewiki/artwork/artwork(10).png').cqcode
sendpic10 = str(pic10)
title10 = '在恒星消失之处。'
author10 = '画师：牧鱼\n'
author_page10 = '画师主页：https://m.weibo.cn/u/2009646437'
text10 = title10 + sendpic10 + author10 + author_page10

pic11 = R.img('musewiki/artwork/artwork(11).png').cqcode
sendpic11 = str(pic11)
title11 = '留下布若大人的痕迹。'
author11 = '画师：狸八\n'
author_page11 = '画师主页：https://m.weibo.cn/u/1921811972'
text11 = title11 + sendpic11 + author11 + author_page11

pic12 = R.img('musewiki/artwork/artwork(12).png').cqcode
sendpic12 = str(pic12)
title12 = '一名假装会打棒球的女子。'
author12 = '画师：H2θ & Yu13\n'
author_page12 = '画师主页：H2θ：暂未收录\nYu13：https://m.weibo.cn/u/1747710857'
text12 = title12 + sendpic12 + author12 + author_page12

pic13 = R.img('musewiki/artwork/artwork(13).png').cqcode
sendpic13 = str(pic13)
title13 = '将要放学的下午时光。'
author13 = '画师：H2θ & Yu13\n'
author_page13 = '画师主页：H2θ：暂未收录\nYu13：https://m.weibo.cn/u/1747710857'
text13 = title13 + sendpic13 + author13 + author_page13

pic14 = R.img('musewiki/artwork/artwork(14).png').cqcode
sendpic14 = str(pic14)
title14 = '玛莉嘉的私人衣柜。'
author14 = '画师：H2θ\n'
author_page14 = '画师主页：暂未收录'
text14 = title14 + sendpic14 + author14 + author_page14

pic15 = R.img('musewiki/artwork/artwork(15).png').cqcode
sendpic15 = str(pic15)
title15 = '那么哪里可以找到这样的咖啡馆呢？'
author15 = '画师：mayu\n'
author_page15 = '画师主页：https://m.weibo.cn/u/3612639510'
text15 = title15 + sendpic15 + author15 + author_page15

pic16 = R.img('musewiki/artwork/artwork(16).png').cqcode
sendpic16 = str(pic16)
title16 = '玛莉嘉的私人照片。'
author16 = '画师：H2θ\n'
author_page16 = '画师主页：暂未收录'
text16 = title16 + sendpic16 + author16 + author_page16

pic17 = R.img('musewiki/artwork/artwork(17).png').cqcode
sendpic17 = str(pic17)
title17 = '当然是相机先次辣。'
author17 = '画师：洛尔\n'
author_page17 = '画师主页：https://m.weibo.cn/u/5396187602'
text17 = title17 + sendpic17 + author17 + author_page17

pic18 = R.img('musewiki/artwork/artwork(18).png').cqcode
sendpic18 = str(pic18)
title18 = 'school day'
author18 = '画师：咸鱼鸽厂长\n'
author_page18 = '画师主页：twitter@nogikeyametal'
text18 = title18 + sendpic18 + author18 + author_page18

pic19 = R.img('musewiki/artwork/artwork(19).png').cqcode
sendpic19 = str(pic19)
title19 = '这个看起来也很可口呢w'
author19 = '画师：BerryVerrine\n'
author_page19 = '画师主页：twitter@berryverrine'
text19 = title19 + sendpic19 + author19 + author_page19

pic20 = R.img('musewiki/artwork/artwork(20).png').cqcode
sendpic20 = str(pic20)
title20 = '求你们善良！--愚人节专属插图'
author20 = '画师：洛尔\n'
author_page20 = '画师主页：https://m.weibo.cn/u/5396187602'
text20 = title20 + sendpic20 + author20 + author_page20

pic21 = R.img('musewiki/artwork/artwork(21).png').cqcode
sendpic21 = str(pic21)
title21 = '儿童节当然是永远都可以过的！'
author21 = '画师：狸八\n'
author_page21 = '画师主页：https://m.weibo.cn/u/1921811972'
text21 = title21 + sendpic21 + author21 + author_page21

pic22 = R.img('musewiki/artwork/artwork(22).png').cqcode
sendpic22 = str(pic22)
title22 = 'Muse Dash一周年纪念！'
author22 = '画师：洛尔\n'
author_page22 = '画师主页：https://m.weibo.cn/u/5396187602'
text22 = title22 + sendpic22 + author22 + author_page22

pic23 = R.img('musewiki/artwork/artwork(23).png').cqcode
sendpic23 = str(pic23)
title23 = '不要停下来呀！（指角色换新服装'
author23 = '画师：花花\n'
author_page23 = '画师主页：暂未收录'
text23 = title23 + sendpic23 + author23 + author_page23

pic24 = R.img('musewiki/artwork/artwork(24).png').cqcode
sendpic24 = str(pic24)
title24 = '2019中秋节快乐~(@>v<@)'
author24 = '画师：Masho\n'
author_page24 = '画师主页：https://m.weibo.cn/u/1792838210'
text24 = title24 + sendpic24 + author24 + author_page24

pic25 = R.img('musewiki/artwork/artwork(25).png').cqcode
sendpic25 = str(pic25)
title25 = '秘技：反复涂鸦疾走！'
author25 = '画师：BoomBoomx_X\n'
author_page25 = '画师主页：https://m.weibo.cn/u/6377035369'
text25 = title25 + sendpic25 + author25 + author_page25

pic26 = R.img('musewiki/artwork/artwork(26).png').cqcode
sendpic26 = str(pic26)
title26 = '哎呀？！好像绊到了什么东西？'
author26 = '画师：待野深海鱼\n'
author_page26 = '画师主页：http://keelott.lofter.com/'
text26 = title26 + sendpic26 + author26 + author_page26

pic27 = R.img('musewiki/artwork/artwork(27).png').cqcode
sendpic27 = str(pic27)
title27 = '这堆零食被我承包了！'
author27 = '画师：SCU\n'
author_page27 = '画师主页：https://m.weibo.cn/p/1005055746306977'
text27 = title27 + sendpic27 + author27 + author_page27

pic28 = R.img('musewiki/artwork/artwork(28).png').cqcode
sendpic28 = str(pic28)
title28 = '回望着过去的少女们也即将踏上新的旅程。二周年快乐，接下来也请多多指教！'
author28 = '画师：DK争争\n'
author_page28 = '画师主页：https://m.weibo.cn/u/5543098417'
text28 = title28 + sendpic28 + author28 + author_page28

pic29 = R.img('musewiki/artwork/artwork(29).png').cqcode
sendpic29 = str(pic29)
title29 = '網 上 衝 浪 ❤'
author29 = '画师：mil7uka\n'
author_page29 = '画师主页：https://m.weibo.cn/u/5890309364'
text29 = title29 + sendpic29 + author29 + author_page29

pic30 = R.img('musewiki/artwork/artwork(30).png').cqcode
sendpic30 = str(pic30)
title30 = '*图片仅供参考，请注意安全驾驶。如果有交通违章账单，请发送到这里。'
author30 = '画师：白上家 & 忍忍\n'
author_page30 = '画师主页：白上家：https://m.bilibili.com/space/332704117\n忍忍：https://m.weibo.cn/u/1147272555'
text30 = title30 + sendpic30 + author30 + author_page30

pic31 = R.img('musewiki/artwork/artwork(31).png').cqcode
sendpic31 = str(pic31)
title31 = '我 是 你 爸 爸。'
author31 = '画师：洛尔\n'
author_page31 = '画师主页：https://m.weibo.cn/u/5396187602'
text31 = title31 + sendpic31 + author31 + author_page31

pic32 = R.img('musewiki/artwork/artwork(32).png').cqcode
sendpic32 = str(pic32)
title32 = '不给糖的话，我就要开始捣乱咯！'
author32 = '画师：Yosetsu\n'
author_page32 = '画师主页：https://m.weibo.cn/u/3771040124'
text32 = title32 + sendpic32 + author32 + author_page32

pic33 = R.img('musewiki/artwork/artwork(33).png').cqcode
sendpic33 = str(pic33)
title33 = '多一条命！'
author33 = '画师：BoomBoomx_X\n'
author_page33 = '画师主页：https://m.weibo.cn/u/6377035369'
text33 = title33 + sendpic33 + author33 + author_page33

pic34 = R.img('musewiki/artwork/artwork(34).png').cqcode
sendpic34 = str(pic34)
title34 = '《我想吃的外婆不可能是操纵小红帽追杀我的女巫》'
author34 = '画师：鼠\n'
author_page34 = '画师主页：https://m.weibo.cn/u/3404523420'
text34 = title34 + sendpic34 + author34 + author_page34

pic35 = R.img('musewiki/artwork/artwork(35).png').cqcode
sendpic35 = str(pic35)
title35 = '谷田！立花！我们是在YouTube活动的Vtuber组合Marpril！在Muse Dash的CD墙拍了纪念照片❤'
author35 = '画师：Marpril & 红茶\n'
author_page35 = '画师主页：Marpril：https://www.youtube.com/channel/UCWhv732tk4DAQ7X32qHKrfA\n红茶：https://m.weibo.cn/u/5156432595'
text35 = title35 + sendpic35 + author35 + author_page35

pic36 = R.img('musewiki/artwork/artwork(36).png').cqcode
sendpic36 = str(pic36)
title36 = '来自天空之境'
author36 = '画师：裹方\n'
author_page36 = '画师主页：https://end.oops.jp/'
text36 = title36 + sendpic36 + author36 + author_page36

pic37 = R.img('musewiki/artwork/artwork(37).png').cqcode
sendpic37 = str(pic37)
title37 = '多吃甜品才能长高高'
author37 = '画师：待野深海鱼\n'
author_page37 = '画师主页：http://keelott.lofter.com/'
text37 = title37 + sendpic37 + author37 + author_page37

pic38 = R.img('musewiki/artwork/artwork(38).png').cqcode
sendpic38 = str(pic38)
title38 = '为什么要在我的车头庆祝300万啦？！'
author38 = '画师：狗肉\n'
author_page38 = '画师主页：https://m.weibo.cn/u/2899151975'
text38 = title38 + sendpic38 + author38 + author_page38

pic39 = R.img('musewiki/artwork/artwork(39).png').cqcode
sendpic39 = str(pic39)
title39 = '最近是在长身体吗:p'
author39 = '画师：p奶\n'
author_page39 = '画师主页：https://m.weibo.cn/u/6418545947'
text39 = title39 + sendpic39 + author39 + author_page39

pic40 = R.img('musewiki/artwork/artwork(40).png').cqcode
sendpic40 = str(pic40)
title40 = '三人组的假日旅行时间'
author40 = '画师：mayu\n'
author_page40 = '画师主页：https://m.weibo.cn/u/3612639510'
text40 = title40 + sendpic40 + author40 + author_page40

pic41 = R.img('musewiki/artwork/artwork(41).png').cqcode
sendpic41 = str(pic41)
title41 = '领航员柚梅，朝着新世界航行出发！'
author41 = '画师：狗肉\n'
author_page41 = '画师主页：https://m.weibo.cn/u/2899151975'
text41 = title41 + sendpic41 + author41 + author_page41

pic42 = R.img('musewiki/artwork/artwork(42).png').cqcode
sendpic42 = str(pic42)
title42 = '另一个玛莉嘉？神秘女子参上！！！'
author42 = '画师：狗肉\n'
author_page42 = '画师主页：https://m.weibo.cn/u/2899151975'
text42 = title42 + sendpic42 + author42 + author_page42

pic43 = R.img('musewiki/artwork/artwork(43).png').cqcode
sendpic43 = str(pic43)
title43 = '红烧牛肉面里为什么会有鱼板啊？！'
author43 = '画师：狗肉\n'
author_page43 = '画师主页：https://m.weibo.cn/u/2899151975'
text43 = title43 + sendpic43 + author43 + author_page43

pic44 = R.img('musewiki/artwork/artwork(44).png').cqcode
sendpic44 = str(pic44)
title44 = '世纪末的怪盗与追踪者'
author44 = '画师：狗肉\n'
author_page44 = '画师主页：https://m.weibo.cn/u/2899151975'
text44 = title44 + sendpic44 + author44 + author_page44

pic45 = R.img('musewiki/artwork/artwork(45).png').cqcode
sendpic45 = str(pic45)
title45 = '从天而降的中华三人组？！'
author45 = '画师：mayu\n'
author_page45 = '画师主页：https://m.weibo.cn/u/3612639510'
text45 = title45 + sendpic45 + author45 + author_page45

pic46 = R.img('musewiki/artwork/artwork(46).png').cqcode
sendpic46 = str(pic46)
title46 = '等等...转盘奖品不包括我！'
author46 = '画师：mayu\n'
author_page46 = '画师主页：https://m.weibo.cn/u/3612639510'
text46 = title46 + sendpic46 + author46 + author_page46

pic47 = R.img('musewiki/artwork/artwork(47).png').cqcode
sendpic47 = str(pic47)
title47 = '咕➡咕↘咕↗咕⬆'
author47 = '画师：谷地\n'
author_page47 = '画师主页：twitter@beco_100me'
text47 = title47 + sendpic47 + author47 + author_page47

pic48 = R.img('musewiki/artwork/artwork(48).png').cqcode
sendpic48 = str(pic48)
title48 = '福瑞控过年辣！'
author48 = '画师：裹紧我的萧备子\n'
author_page48 = '画师主页：https://m.weibo.cn/u/5504333416'
text48 = title48 + sendpic48 + author48 + author_page48

pic49 = R.img('musewiki/artwork/artwork(49).png').cqcode
sendpic49 = str(pic49)
title49 = '只有三个选项可以提高绘美的好感度哦(ゝ∀･)!'
author49 = '画师：红茶\n'
author_page49 = '画师主页：https://m.weibo.cn/u/5156432595'
text49 = title49 + sendpic49 + author49 + author_page49

pic50 = R.img('musewiki/artwork/artwork(50).png').cqcode
sendpic50 = str(pic50)
title50 = '儿童节和好朋友们一起去了公园玩~'
author50 = '画师：mil7uka\n'
author_page50 = '画师主页：https://m.weibo.cn/u/5890309364'
text50 = title50 + sendpic50 + author50 + author_page50

pic51 = R.img('musewiki/artwork/artwork(51).png').cqcode
sendpic51 = str(pic51)
title51 = '今日宜听歌 带上收音机 前往宇宙蹦迪'
author51 = '画师：啊旁白\n'
author_page51 = '画师主页：https://m.weibo.cn/u/2566204374'
text51 = title51 + sendpic51 + author51 + author_page51

pic52 = R.img('musewiki/artwork/artwork(52).png').cqcode
sendpic52 = str(pic52)
title52 = '《暮色电台精选集》2000年第一版，附赠的随声听抽奖券已经过期了。'
author52 = '画师：红茶\n'
author_page52 = '画师主页：https://m.weibo.cn/u/5156432595'
text52 = title52 + sendpic52 + author52 + author_page52

pic53 = R.img('musewiki/artwork/artwork(53).png').cqcode
sendpic53 = str(pic53)
title53 = '今天也要打包那么多圣诞礼物么...'
author53 = '画师：红茶\n'
author_page53 = '画师主页：https://m.weibo.cn/u/5156432595'
text53 = title53 + sendpic53 + author53 + author_page53

pic54 = R.img('musewiki/artwork/artwork(54).png').cqcode
sendpic54 = str(pic54)
title54 = 'NEKO#ФωФ的实况时间————「Muse Daaaaaaaaaaash！」'
author54 = '画师：狗肉\n'
author_page54 = '画师主页：https://m.weibo.cn/u/2899151975'
text54 = title54 + sendpic54 + author54 + author_page54

pic55 = R.img('musewiki/artwork/artwork(55).png').cqcode
sendpic55 = str(pic55)
title55 = 'haloooo？！是来自新世界的粉红兔兔！'
author55 = '画师：mayu\n'
author_page55 = '画师主页：https://m.weibo.cn/u/3612639510'
text55 = title55 + sendpic55 + author55 + author_page55

pic56 = R.img('musewiki/artwork/artwork(56).png').cqcode
sendpic56 = str(pic56)
title56 = '请问今天要来点nanahira吗？'
author56 = '画师：Nanahira & VINOVIS\n'
author_page56 = '画师主页：Nanahira：https://www.youtube.com/channel/UC_fYA9QRK-aJnFTgvR_4zug\nVINOVIS：twitter@inh__sy'
text56 = title56 + sendpic56 + author56 + author_page56

pic57 = R.img('musewiki/artwork/artwork(57).png').cqcode
sendpic57 = str(pic57)
title57 = '事情正按照计划中所设想的那样发展（拖走'
author57 = '画师：暂未收录\n'
author_page57 = '画师主页：暂未收录'
text57 = title57 + sendpic57 + author57 + author_page57

@sv.on_fullmatch("单图查询1")
async def send_artwork(bot, ev):
    info_help = text1
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询2")
async def send_artwork(bot, ev):
    info_help = text2
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询3")
async def send_artwork(bot, ev):
    info_help = text3
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询4")
async def send_artwork(bot, ev):
    info_help = text4
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询5")
async def send_artwork(bot, ev):
    info_help = text5
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询6")
async def send_artwork(bot, ev):
    info_help = text6
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询7")
async def send_artwork(bot, ev):
    info_help = text7
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询8")
async def send_artwork(bot, ev):
    info_help = text8
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询9")
async def send_artwork(bot, ev):
    info_help = text9
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询10")
async def send_artwork(bot, ev):
    info_help = text10
    mid = ev['message_id']
    cq_message = f'[CQ:reply,id={mid}]'
    finalmsg = cq_message + info_help
    await bot.send(ev, finalmsg)
@sv.on_fullmatch("单图查询11")
async def send_artwork(bot, ev):
    await bot.send(ev, text11)
@sv.on_fullmatch("单图查询12")
async def send_artwork(bot, ev):
    await bot.send(ev, text12)
@sv.on_fullmatch("单图查询13")
async def send_artwork(bot, ev):
    await bot.send(ev, text13)
@sv.on_fullmatch("单图查询14")
async def send_artwork(bot, ev):
    await bot.send(ev, text14)
@sv.on_fullmatch("单图查询15")
async def send_artwork(bot, ev):
    await bot.send(ev, text15)
@sv.on_fullmatch("单图查询16")
async def send_artwork(bot, ev):
    await bot.send(ev, text16)
@sv.on_fullmatch("单图查询17")
async def send_artwork(bot, ev):
    await bot.send(ev, text17)
@sv.on_fullmatch("单图查询18")
async def send_artwork(bot, ev):
    await bot.send(ev, text18)
@sv.on_fullmatch("单图查询19")
async def send_artwork(bot, ev):
    await bot.send(ev, text19)
@sv.on_fullmatch("单图查询20")
async def send_artwork(bot, ev):
    await bot.send(ev, text20)
@sv.on_fullmatch("单图查询21")
async def send_artwork(bot, ev):
    await bot.send(ev, text21)
@sv.on_fullmatch("单图查询22")
async def send_artwork(bot, ev):
    await bot.send(ev, text22)
@sv.on_fullmatch("单图查询23")
async def send_artwork(bot, ev):
    await bot.send(ev, text23)
@sv.on_fullmatch("单图查询24")
async def send_artwork(bot, ev):
    await bot.send(ev, text24)
@sv.on_fullmatch("单图查询25")
async def send_artwork(bot, ev):
    await bot.send(ev, text25)
@sv.on_fullmatch("单图查询26")
async def send_artwork(bot, ev):
    await bot.send(ev, text26)
@sv.on_fullmatch("单图查询27")
async def send_artwork(bot, ev):
    await bot.send(ev, text27)
@sv.on_fullmatch("单图查询28")
async def send_artwork(bot, ev):
    await bot.send(ev, text28)
@sv.on_fullmatch("单图查询29")
async def send_artwork(bot, ev):
    await bot.send(ev, text29)
@sv.on_fullmatch("单图查询30")
async def send_artwork(bot, ev):
    await bot.send(ev, text30)
@sv.on_fullmatch("单图查询31")
async def send_artwork(bot, ev):
    await bot.send(ev, text31)
@sv.on_fullmatch("单图查询32")
async def send_artwork(bot, ev):
    await bot.send(ev, text32)
@sv.on_fullmatch("单图查询33")
async def send_artwork(bot, ev):
    await bot.send(ev, text33)
@sv.on_fullmatch("单图查询34")
async def send_artwork(bot, ev):
    await bot.send(ev, text34)
@sv.on_fullmatch("单图查询35")
async def send_artwork(bot, ev):
    await bot.send(ev, text35)
@sv.on_fullmatch("单图查询36")
async def send_artwork(bot, ev):
    await bot.send(ev, text36)
@sv.on_fullmatch("单图查询37")
async def send_artwork(bot, ev):
    await bot.send(ev, text37)
@sv.on_fullmatch("单图查询38")
async def send_artwork(bot, ev):
    await bot.send(ev, text38)
@sv.on_fullmatch("单图查询39")
async def send_artwork(bot, ev):
    await bot.send(ev, text39)
@sv.on_fullmatch("单图查询40")
async def send_artwork(bot, ev):
    await bot.send(ev, text40)
@sv.on_fullmatch("单图查询41")
async def send_artwork(bot, ev):
    await bot.send(ev, text41)
@sv.on_fullmatch("单图查询42")
async def send_artwork(bot, ev):
    await bot.send(ev, text42)
@sv.on_fullmatch("单图查询43")
async def send_artwork(bot, ev):
    await bot.send(ev, text43)
@sv.on_fullmatch("单图查询44")
async def send_artwork(bot, ev):
    await bot.send(ev, text44)
@sv.on_fullmatch("单图查询45")
async def send_artwork(bot, ev):
    await bot.send(ev, text45)
@sv.on_fullmatch("单图查询46")
async def send_artwork(bot, ev):
    await bot.send(ev, text46)
@sv.on_fullmatch("单图查询47")
async def send_artwork(bot, ev):
    await bot.send(ev, text47)
@sv.on_fullmatch("单图查询48")
async def send_artwork(bot, ev):
    await bot.send(ev, text48)
@sv.on_fullmatch("单图查询49")
async def send_artwork(bot, ev):
    await bot.send(ev, text49)
@sv.on_fullmatch("单图查询50")
async def send_artwork(bot, ev):
    await bot.send(ev, text50)
@sv.on_fullmatch("单图查询51")
async def send_artwork(bot, ev):
    await bot.send(ev, text51)
@sv.on_fullmatch("单图查询52")
async def send_artwork(bot, ev):
    await bot.send(ev, text52)
@sv.on_fullmatch("单图查询53")
async def send_artwork(bot, ev):
    await bot.send(ev, text53)
@sv.on_fullmatch("单图查询54")
async def send_artwork(bot, ev):
    await bot.send(ev, text54)
@sv.on_fullmatch("单图查询55")
async def send_artwork(bot, ev):
    await bot.send(ev, text55)
@sv.on_fullmatch("单图查询56")
async def send_artwork(bot, ev):
    await bot.send(ev, text56)
@sv.on_fullmatch("单图查询57")
async def send_artwork(bot, ev):
    await bot.send(ev, text57)

@sv.on_fullmatch("纯场景1")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/no_goods/Scene01Bg.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("纯场景2")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/no_goods/Scene02Bg.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("纯场景3")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/no_goods/Scene03Bg.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("纯场景4")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/no_goods/Scene04Bg.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("纯场景5")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/no_goods/Scene05Bg.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("纯场景6")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/no_goods/Scene06Bg.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("纯场景7")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/no_goods/Scene07Bg.png').cqcode
    await bot.send(ev, img)

@sv.on_fullmatch("合成场景1")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/with_goods/SceneFX01.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("合成场景2")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/with_goods/SceneFX02.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("合成场景3")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/with_goods/SceneFX03.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("合成场景4")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/with_goods/SceneFX04.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("合成场景5")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/with_goods/SceneFX05.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("合成场景6")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/with_goods/SceneFX06.png').cqcode
    await bot.send(ev, img)
@sv.on_fullmatch("合成场景7")
async def send_scenes(bot, ev):
    img = R.img('musewiki/scenes/with_goods/SceneFX07.png').cqcode
    await bot.send(ev, img)

@sv.on_fullmatch("全图查询")
async def wiki_artwork_all(bot, ev):
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, f"查询过于频繁，有{_cd}秒冷却哦", at_sender=True)
        return
    _flmt.start_cd(uid)

    try:
        await bot.send(ev, '图片较多，将合并转发消息，耗时较长，请耐心等待。')
        data_all_1 = []
        data_all_2 = []
        data_all_3 = []
        data1 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text1 + '\n' + text2 + '\n' + text3 + '\n' + text4 + '\n' + text5
            }
        }
        data2 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text6 + '\n' + text7 + '\n' + text8 + '\n' + text9 + '\n' + text10
            }
        }
        data3 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text11 + '\n' + text12 + '\n' + text13 + '\n' + text14 + '\n' + text15
            }
        }
        data4 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text16 + '\n' + text17 + '\n' + text18 + '\n' + text19 + '\n' + text20
            }
        }
        data5 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text21 + '\n' + text22 + '\n' + text23 + '\n' + text24 + '\n' + text25
            }
        }
        data6 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text26 + '\n' + text27 + '\n' + text28 + '\n' + text29 + '\n' + text30
            }
        }
        data7 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text31 + '\n' + text32 + '\n' + text33 + '\n' + text34 + '\n' + text35
            }
        }
        data8 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text36 + '\n' + text37 + '\n' + text38 + '\n' + text39 + '\n' + text40
            }
        }
        data9 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text41 + '\n' + text42 + '\n' + text43 + '\n' + text44 + '\n' + text45
            }
        }
        data10 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text46 + '\n' + text47 + '\n' + text48 + '\n' + text49 + '\n' + text50
            }
        }
        data11 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text51 + '\n' + text52 + '\n' + text53 + '\n' + text54 + '\n' + text55
            }
        }
        data12 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": text56 + '\n' + text57
            }
        }
        data_all_1=[data1,data2,data3,data4,data5]
        data_all_2=[data6,data7,data8,data9,data10]
        data_all_3=[data11,data12]

        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all_1)
        time.sleep(5)
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all_2)
        time.sleep(5)
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all_3)
    except CQHttpError:
        sv.logger.error(f"MuseDash百科，发送[全图查询]消息失败")
        try:
            await bot.send(ev, '发送消息失败，bot可能被风控')
        except:
            pass

nogood_folder_scene = R.img('musewiki/scenes/no_goods/').path

withgood_folder_scene = R.img('musewiki/scenes/with_goods/').path

def scene_gener_nog():
    while True:
        filelist_no = os.listdir(nogood_folder_scene)
        random.shuffle(filelist_no)
        for filename in filelist_no:
            if os.path.isfile(os.path.join(nogood_folder_scene, filename)):
                yield R.img('musewiki/scenes/no_goods/', filename)

def scene_gener_with():
    while True:
        filelist_in = os.listdir(withgood_folder_scene)
        random.shuffle(filelist_in)
        for filename in filelist_in:
            if os.path.isfile(os.path.join(withgood_folder_scene, filename)):
                yield R.img('musewiki/scenes/with_goods/', filename)

scene_gener_nog = scene_gener_nog()

def get_nogoods():
    return scene_gener_nog.__next__()

scene_gener_with = scene_gener_with()

def get_withgoods():
    return scene_gener_with.__next__()

@sv.on_fullmatch(["随机纯场景"])
async def wiki_scene_nogood(bot, ev):
    pic = get_nogoods()
    try:
        await bot.send(ev, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"MuseDash百科-插图查询，发送图片{pic.path}失败")
        try:
            await bot.send(ev, '发送图片失败...')
        except:
            pass

@sv.on_fullmatch(["随机合成场景"])
async def wiki_scene_withgood(bot, ev):
    pic = get_withgoods()
    try:
        await bot.send(ev, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"MuseDash百科-插图查询，发送图片{pic.path}失败")
        try:
            await bot.send(ev, '发送图片失败...')
        except:
            pass