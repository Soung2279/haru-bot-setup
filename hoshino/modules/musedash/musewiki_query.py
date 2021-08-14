# -*- coding: utf-8 -*-
from typing import Text
from time import time
import requests, asyncio, os, time, random
from datetime import datetime
import pytz
import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.typing import CQEvent, MessageSegment
from hoshino.util import FreqLimiter, escape, DailyNumberLimiter
from operator import __iadd__
from nonebot.exceptions import CQHttpError

from . import _song_data, _chip_data

tz = pytz.timezone('Asia/Shanghai')

_max = 1
_nlmt = DailyNumberLimiter(_max)

forward_msg_name = 'SoungBot测试版'
forward_msg_uid = '756160433'

Wiki_Menu_Query_img = R.img(f"musewiki/etc/query.png").cqcode

tips_tuple = _song_data.Muse_Tips

sv_help = '''
    ※MuseDash百科-资料查询※
当前菜单有以下内容：
    -资料查询-
- [查询隐藏曲目]  查询隐藏曲目的解锁方式
- [偏移值参考]  查询游戏偏移值设定参考
- [游戏冷知识]  游戏相关的一些小知识
- [md表情包]  来一张musedash相关的表情包

或发送以下指令进入其它菜单：
- [帮助md百科]
- [帮助百科插图查询]
- [帮助百科成就查询]
- [帮助百科语音查询]
- [帮助百科角色查询]
- [帮助百科歌曲推送]
- [帮助百科运势]
'''.strip()

sv = Service(
    name = 'MuseDash百科-资料查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'musedash', #属于哪一类
    help_ = sv_help #帮助文本
    )

def get_voice_query_menu():
    filename = 'OthersBgm.wav'
    voice_rec = R.get('record/musewiki/audioclip/', filename)
    return voice_rec

@sv.on_fullmatch(["帮助MuseDash百科-资料查询", "帮助百科资料查询"])
async def bangzhu_musewiki_query(bot, ev) -> MessageSegment:
    file = get_voice_query_menu()
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
        await bot.send(ev, f"欢迎继续使用MuseDash百科-资料查询！")
    else:
        await bot.send(ev, voice_rec)
    _nlmt.increase(uid)

    final_output = Wiki_Menu_Query_img + sv_help
    await bot.send(ev, final_output)


Base_Cover_Img = R.img(f"musewiki/pack/基础包.png").cqcode
Given_Cover_Img = R.img(f"musewiki/放弃治疗Vol.1.png").cqcode
Otaku_Cover_Img = R.img(f"musewiki/pack/肥宅快乐包Vol.1.png").cqcode
Collab_Cover_Img = R.img(f"musewiki/pack/联动包.png").cqcode
FM_Cover_Img = R.img(f"musewiki/pack/暮 色 電 台FM101.png").cqcode

IN_QUERY_NOTICE = '''
教程来源:https://www.taptap.com/topic/15501513
截止到 肥宅快乐包 Vol.12
MuseDash共有 28 首隐藏铺面。其中，

基础包 4首隐藏铺面

放弃治疗包 3首隐藏铺面

肥宅快乐包 8首隐藏铺面

联动包 12首隐藏铺面

暮色电台 1首隐藏铺面

请输入【隐藏查询+查询的曲包】，例如：[隐藏查询 基础包]
'''.strip()

basepic1 = R.img(f"musewiki/songcover/lights of muse.png").cqcode
BASE1_IN_QUERY = f"歌曲名：Lights of Muse\n解锁方式：狂按大触\n来源：基础包"
Base_in_1 = basepic1 + BASE1_IN_QUERY

basepic2 = R.img(f"musewiki/songcover/儿童鞋垫.png").cqcode
BASE2_IN_QUERY = f"歌曲名：もぺもぺ\n解锁方式：狂按大触\n来源：基础包"
Base_in_2 = basepic2 + BASE2_IN_QUERY

basepic3 = R.img(f"musewiki/songcover/irreplaceable.png").cqcode
BASE3_IN_QUERY = f"歌曲名：lrreplaceable feat.AKINO wish bless4\n解锁方式：狂按大触\n来源：基础包：经费在燃烧:纳米核心"
Base_in_3 = basepic3 + BASE3_IN_QUERY

basepic4 = R.img(f"musewiki/songcover/stargezer.png").cqcode
BASE4_IN_QUERY = f"歌曲名：Stargezer\n解锁方式：狂按大触\n来源：基础包：经费在燃烧 Vol.1"
Base_in_4 = basepic4 + BASE4_IN_QUERY

givenpic1 = R.img(f"musewiki/songcover/trippers feeling.png").cqcode
GIVEN1_IN_QUERY = f"歌曲名：trippers feeling!\n解锁方式：狂按大触\n歌曲位置：放弃治疗包 Vol.3"
Given_in_1 = givenpic1 + GIVEN1_IN_QUERY

givenpic2 = R.img(f"musewiki/songcover/万圣节.png").cqcode
GIVEN2_IN_QUERY = f"歌曲名：Sweet*Witch*Girls*\n解锁方式：将系统时间调整至2019年万圣节（2019.11.1）进入曲目即可看到\n歌曲位置：放弃治疗包 Vol.3"
Given_in_2 = givenpic2 + GIVEN2_IN_QUERY

givenpic3 = R.img(f"musewiki/songcover/freedom.png").cqcode
GIVEN3_IN_QUERY = f"歌曲名：FREEDOM DiVE↓\n解锁方式：在大触界面顺时针画3-5个圈圈\n歌曲位置：放弃治疗包 Vol.8"
Given_in_3 = givenpic3 + GIVEN3_IN_QUERY

otakupic1 = R.img(f"musewiki/songcover/goodtek.png").cqcode
OTAKU1_IN_QUERY = f"歌曲名：GOODTEK(Hyper Edit)\n解锁方式：将系统时间调整至2019年愚人节（2019.4.1）进入曲目即可看到\n歌曲位置：肥宅快乐包 Vol.2"
Otaku_in_1 = otakupic1 + OTAKU1_IN_QUERY

otakupic2 = R.img(f"musewiki/songcover/xing.png").cqcode
OTAKU2_IN_QUERY = f"歌曲名：XING\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.3"
Otaku_in_2 = otakupic2 + OTAKU2_IN_QUERY

otakupic3 = R.img(f"musewiki/songcover/conflict.png").cqcode
OTAKU3_IN_QUERY = f"歌曲名：conflict\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.3"
Otaku_in_3 = otakupic3 + OTAKU3_IN_QUERY

otakupic4 = R.img(f"musewiki/songcover/infinite energy.png").cqcode
OTAKU4_IN_QUERY = f"歌曲名：INFiNiTE ENERZY -Overdoze-\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.8"
Otaku_in_4 = otakupic4 + OTAKU4_IN_QUERY

otakupic5 = R.img(f"musewiki/songcover/ginevra.png").cqcode
OTAKU5_IN_QUERY = f"歌曲名：Ginevra\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.10"
Otaku_in_5 = otakupic5 + OTAKU5_IN_QUERY

otakupic6 = R.img(f"musewiki/songcover/square lake.png").cqcode
OTAKU6_IN_QUERY = f"歌曲名：Square Lake\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.11"
Otaku_in_6 = otakupic6 + OTAKU6_IN_QUERY

otakupic7 = R.img(f"musewiki/songcover/medusa.png").cqcode
OTAKU7_IN_QUERY = f"歌曲名：Medusa\n解锁方式：狂按高手\n歌曲位置：肥宅快乐包 Vol.11"
Otaku_in_7 = otakupic7 + OTAKU7_IN_QUERY

otakupic8 = R.img(f"musewiki/songcover/dataerror.png").cqcode
OTAKU8_IN_QUERY = f"歌曲名：DataError\n解锁方式：狂按高手\n歌曲位置：肥宅快乐包 SP"
Otaku_in_8 = otakupic8 + OTAKU8_IN_QUERY

collabpic1 = R.img(f"musewiki/songcover/igallta.png").cqcode
COLLAB1_IN_QUERY = f"歌曲名：igallta\n解锁方式：狂按大触\n歌曲位置：Phigros"
Collab_in_1 = collabpic1 + COLLAB1_IN_QUERY

collabpic2 = R.img(f"musewiki/songcover/batle no1.png").cqcode
COLLAB2_IN_QUERY = f"歌曲名：BATTLE NO.1\n解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_2 = collabpic2 + COLLAB2_IN_QUERY

collabpic3 = R.img(f"musewiki/songcover/cthugha.png").cqcode
COLLAB3_IN_QUERY = f"歌曲名：Cthugha\n解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_3 = collabpic3 + COLLAB3_IN_QUERY

collabpic4 = R.img(f"musewiki/songcover/twinkle magic.png").cqcode
COLLAB4_IN_QUERY = f"歌曲名：TWINKLE★MAGIC\n解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_4 = collabpic4 + COLLAB4_IN_QUERY

collabpic4v5 = R.img(f"musewiki/songcover/comet coaster.png").cqcode
COLLAB4v5_IN_QUERY = f"歌曲名：Comet Coaster\n解锁方式：解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_4v5 = collabpic4v5 + COLLAB4v5_IN_QUERY

collabpic5 = R.img(f"musewiki/songcover/xodus.png").cqcode
COLLAB5_IN_QUERY = f"歌曲名：XODUS\n解锁方式：在大触界面画很多个 X\n歌曲位置：HARDCORE TANO*C"
Collab_in_5 = collabpic5 + COLLAB5_IN_QUERY

collabpic6 = R.img(f"musewiki/songcover/happiness breeze.png").cqcode
COLLAB6_IN_QUERY = f"歌曲名：Happiness Breeze\n解锁方式：狂按大触\n歌曲位置：cyTus"
Collab_in_6 = collabpic6 + COLLAB6_IN_QUERY

collabpic7 = R.img(f"musewiki/songcover/chrome.png").cqcode
COLLAB7_IN_QUERY = f"歌曲名：Chrome VOX\n解锁方式：狂按大触\n歌曲位置：cyTus"
Collab_in_7 = collabpic7 + COLLAB7_IN_QUERY

collabpic8 = R.img(f"musewiki/songcover/chaos.png").cqcode
COLLAB8_IN_QUERY = f"歌曲名：CHAOS\n解锁方式：在收藏系统内打开Cytus2欢迎界面插画，等待几秒后凛桌子上的手机（键盘左边）会有CHAOS图标。在拨号结束前点击CHAOS图标或者电话按钮即可进入隐藏铺界面。\n歌曲位置：cyTus"
Collab_in_8 = collabpic8 + COLLAB8_IN_QUERY

collabpic9 = R.img(f"musewiki/songcover/fujin.png").cqcode
COLLAB9_IN_QUERY = f"歌曲名：FUJIN Rumble\n解锁方式：狂按大触\n歌曲位置：Let's GROOVE!"
Collab_in_9 = collabpic9 + COLLAB9_IN_QUERY

collabpic10 = R.img(f"musewiki/songcover/HG魔改造.png").cqcode
COLLAB10_IN_QUERY = f"歌曲名：HG魔改造ポリビニル少年\n解锁方式：狂按大触\n歌曲位置：Let's GROOVE!"
Collab_in_10 = collabpic10 + COLLAB10_IN_QUERY

collabpic11 = R.img(f"musewiki/songcover/ouroboros.png").cqcode
COLLAB11_IN_QUERY = f"歌曲名：ouroboros -twin stroke of the end-\n解锁方式：在难度选择界面从大触难度开始按照高手-萌新-高手-大触-高手-萌新-高手-大触的顺序点击难度选择按钮，构成衔尾蛇即可解锁隐藏谱面。\n歌曲位置：Let's GROOVE!"
Collab_in_11 = collabpic11 + COLLAB11_IN_QUERY

fmpic1 = R.img(f"musewiki/songcover/去剪海的日子.png").cqcode
FM_IN_QUERY = f"歌曲名：FM17314 SUGAR RADIO\n长按 去剪海的日子(暮色电台FM102)曲绘，直至圆圈转完为止即可进入隐藏曲\n来源：暮色电台FM102"
FM_in_1 = fmpic1 + FM_IN_QUERY

@sv.on_fullmatch(["查询隐藏曲目", "隐藏曲目查询"])
async def in_query_main(bot, ev):
    await bot.send(ev, IN_QUERY_NOTICE)

@sv.on_fullmatch(["隐藏查询 基础包", "查询隐藏 基础包"])
async def in_query_wikisearch(bot, ev):
    text = f'基础包(含经费在燃烧，纳米核心等)共有 4首 隐藏铺面'
    fxtext = Base_Cover_Img + text
    final = Base_in_1 + '\n' + Base_in_2 + '\n' + Base_in_3 + '\n' + Base_in_4
    await bot.send(ev, fxtext, at_sender=True)
    await bot.send(ev, final, at_sender=True)

@sv.on_fullmatch(["隐藏查询 放弃治疗包", "查询隐藏 放弃治疗包"])
async def in_query_wikisearch(bot, ev):
    text = f'放弃治疗包共有 3首 隐藏铺面'
    fxtext = Base_Cover_Img + text
    final = Given_in_1 + '\n' + Given_in_2 + '\n' + Given_in_3
    await bot.send(ev, text, at_sender=True)
    await bot.send(ev, final, at_sender=True)

@sv.on_fullmatch(["隐藏查询 肥宅快乐包", "查询隐藏 肥宅快乐包"])
async def in_query_wikisearch(bot, ev):
    text = f'肥宅快乐包共有 8首 隐藏铺面'
    fxtext = Otaku_Cover_Img + text
    final_1 = Otaku_in_1 + '\n' + Otaku_in_2 + '\n' + Otaku_in_3 + '\n' + Otaku_in_7
    final_2 = Otaku_in_4 + '\n' + Otaku_in_5 + '\n' + Otaku_in_6 + '\n' + Otaku_in_8
    await bot.send(ev, fxtext, at_sender=True)
    await bot.send(ev, final_1, at_sender=True)
    time.sleep(3)
    await bot.send(ev, final_2, at_sender=True)

@sv.on_fullmatch(["隐藏查询 联动包", "查询隐藏 联动包"])
async def in_query_wikisearch(bot, ev):
    text = f'联动包共有 12首 隐藏铺面'
    fxtext = Collab_Cover_Img + text
    final_1 = Collab_in_1 + '\n' + Collab_in_2 + '\n' + Collab_in_3 + '\n' + Collab_in_4 + '\n' + Collab_in_4v5 + '\n' + Collab_in_5
    final_2 = Collab_in_6 + '\n' + Collab_in_7 + '\n' + Collab_in_8 + '\n' + Collab_in_9 + '\n' + Collab_in_10 + '\n' + Collab_in_11
    await bot.send(ev, fxtext, at_sender=True)
    await bot.send(ev, final_1, at_sender=True)
    time.sleep(3)
    await bot.send(ev, final_2, at_sender=True)

@sv.on_fullmatch(["隐藏查询 暮色电台", "查询隐藏 暮色电台"])
async def in_query_wikisearch(bot, ev):
    text = f'暮色电台共有 1首 隐藏铺面'
    fxtext = FM_Cover_Img + text
    final = FM_in_1
    await bot.send(ev, fxtext, at_sender=True)
    await bot.send(ev, final, at_sender=True)

OFFSET_LENOVO = '''
- 联想 -
联想Z5：0.128
'''.strip()
OFFSET_ZTC = '''
- 中兴 - 
中兴 ZD-P1-TJ3：0.085
'''.strip()
OFFSET_TX = '''
- 黑鲨 -
黑鲨手机：0.195
'''.strip()
OFFSET_LG = '''
- LG -
LG v20：0.135
LG v30：0.170
LG G6：0.335
'''.strip()
OFFSET_360 = '''
- 360 -
360 N5：0.235
360 N6 Pro：0.400
360N7：0.080
'''.strip()
OFFSET_GOOGLE = '''
- GOOGLE -
Google Pixel：0.000
Google Pixel C：0.060
Google Pixel 3 XL：-0.010
'''.strip()
OFFSET_LESI = '''
- 乐视 -
乐视乐Max 2：0.245
乐视 x620：0.200
'''.strip()
OFFSET_NUBIA = '''
- nubia -
nubia Z11 Max：0.280
nubia Z17：0.190
'''.strip()
OFFSET_MEIZU = '''
- 魅族 -
魅族 16th：0.150
魅蓝 5S：0
魅蓝S6：0.075
魅族 15Plus：0.100
魅蓝 Note 5：0.050
魅蓝 Note 6：0.200
魅蓝 e2：0.030
'''.strip()
OFFSET_ONEPLUS = '''
- 一加 -
OnePlus 3T：0.155
OnePlus 3：0.075
OnePlus 5：0.420
OnePlus 5T：0.150
OnePlus 6：0.165
OnePlus 6T：0.100
'''.strip()
OFFSET_SONY = '''
- SONY -
Xperia XZs：0.195
Xperia XZ1：0.060
Xperia XZ2：0.020
Z4 Tablet：0.025
Xperia Z5：-0.050
SONY XZ PREMIUM：0.150
'''.strip()
OFFSET_SAMSUNG = '''
- SAMSUNG -
Galaxy Note4：0.055
Galaxy S6：0.145
Galaxy C7：0.165
Galaxy On7：0.200
Galaxy S7 edge：0.155
Galaxy S8：0.030
Galaxy S9：-0.0150
Galaxy S10：0.04
Galaxy Tab S 10.5：0.045
'''.strip()
OFFSET_APPLE = '''
- APPLE -
iPad Pro 2：0.002
iPad Pro 9.7‘’：0
iPad Air2：0
iPad mini：0.100
iPad mini i4:0.003
iPad （2017new）：0
iPad 2017：0
iPad 2018：0
iPhone 6S：0.010
iPhone 6sp：0.028
iPhone 8：0.100
iPhone 8 plus：0
'''.strip()
OFFSET_OPPO = '''
- OPPO -
OPPO A3：0.015
OPPO A33m：0.165
OPPO A59s：0.100
OPPO A83：0.000
OPPO A9x：0.091
OPPO R7s：0.100
OPPO R9s：0.170
OPPO R9s Plus：0.170
OPPO R11：0.125
OPPO R11s：0.095
OPPO Find X：0.165
'''.strip()
OFFSET_VIVO = '''
- vivo -
vivo NEXs：0.140
vivo V3M A：0.190
vivo Xplay6：0.07
vivo X9：0.105
vivoX9p：0.020
vivo X9s：0.065
vivo X20：0.160
vivo X50：0.121 / 0.079
vivo Y51：0.500
vivo Y66：0.015
vivo Y67：0.150
vivo Y67a：0.070
vivo Y75：0.000
vivo Y79：0.080
vivo Y85a：0.010
vivo Z1i：0.190
'''.strip()
OFFSET_HUAWEI = '''
- HUAWEI -
（华为目前数值暂时有偏差，数值仅供参考）
HUAWEI 麦芒6：0.15
HUAWEI CAZ AL-10：0.160
HUAWEI DIG-AL00：0.135
华为畅享 6S：0.135
荣耀 畅玩平板 2：0.070
HUAWEI Mate 8：0.020
HUAWEI Mate 9：0.065
HUAWEI nova：0.160
HUAWEI nova 2：0.035
HUAWEI nova 3e：0.035
HUAWEI P10：0.025
HUAWEI P10 Plus：0.010
HUAWEI P20 Pro：0.070
HUAWEI Honor 5A：0.010
HUAWEI Honor 8：0.045
HUAWEI Honor 8 青春版：0.185
HUAWEI Honor V8：0.120
HUAWEI Honor 9：0.045
HUAWEI Honor 10：0.450
HUAWEI Honor V10：0.300
'''.strip()
OFFSET_MI = '''
- 小米 -
小米 5 ：0.165
小米 5C：0.100
小米 5S：0.130
小米 5S Plus：0.160
小米 6：0.160
小米 6X：0.195
小米 8：0.160
小米MAX：0.150
小米MAX2：0.150
小米MAX3：0.200
小米MIX2：0.040
小米MIX2S：0.150
小米NOTE LTE：0.010
小米NOTE2：0.100
红米3：0.265
红米4：0.107
红米5 plus：0.165
红米5A：0.115
红米Note1:0.005
红米 Note 2：0.005
红米 Note 3：0.005
红米 Note 4X：0.130
红米 Note 5：0.195
红米 Note 5A：0.215
红米 S2：0.130
红米 K30Ultra：0.020
'''.strip()

OFFSET_MAIN = '''
由于硬件设备种类繁多，播放音乐会有不同程度的延迟，为保证游戏中的打击和音乐对上，需要使用偏移校准功能。
请输入您的设备厂商进行查询，例如[偏移值 小米]
或者直接【查询所有偏移参考】
如果bot未响应，大概率是未收录该厂商。请尝试向官方提交反馈
[Offset 值收集反馈帖！！( ゜▽゜)つロ！]https://www.taptap.com/topic/3306697
'''.strip()

Wiki_Menu_Achievement_img_1 = R.img(f"musewiki/etc/ImgOffsetTips.png").cqcode
Wiki_Menu_Achievement_img_2 = R.img(f"musewiki/etc/IconOffset.png").cqcode

@sv.on_fullmatch(["偏移值参考", "查询偏移值参考", "偏移值参考查询"])
async def offset_query_main(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_1 + OFFSET_MAIN
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["查询所有偏移参考", "查询所有偏移值参考"])
async def offset_query_all(bot, ev):
    text = f"消息较长，请注意"
    fxtext = Wiki_Menu_Achievement_img_2 + text
    await bot.send(ev, fxtext)
    OFFSET_ALL_1 = OFFSET_LENOVO + '\n' + OFFSET_ZTC + '\n' + OFFSET_TX + '\n' + OFFSET_LG + '\n' + OFFSET_360 + '\n' + OFFSET_GOOGLE + '\n' + OFFSET_LESI + '\n' + OFFSET_NUBIA + '\n' + OFFSET_MEIZU + '\n' + OFFSET_ONEPLUS
    OFFSET_ALL_2 = OFFSET_SONY + '\n' + OFFSET_SAMSUNG + '\n' + OFFSET_APPLE + '\n' + OFFSET_OPPO
    OFFSET_ALL_3 = OFFSET_VIVO + '\n' + OFFSET_HUAWEI + '\n' + OFFSET_MI
    await bot.send(ev, OFFSET_ALL_1)
    time.sleep(5)
    await bot.send(ev, OFFSET_ALL_2)
    time.sleep(5)
    await bot.send(ev, OFFSET_ALL_3)

@sv.on_fullmatch(["偏移值联想", "偏移值 联想"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_LENOVO
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值中兴", "偏移值 中兴"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_ZTC
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值黑鲨", "偏移值 黑鲨"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_TX
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值LG", "偏移值 LG"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_LG
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值360", "偏移值 360"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_360
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值谷歌", "偏移值 谷歌"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_GOOGLE
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值乐视", "偏移值 乐视"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_LESI
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值努比亚", "偏移值 努比亚"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_NUBIA
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值魅族", "偏移值 魅族"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_MEIZU
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值一加", "偏移值 一加"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_ONEPLUS
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值索尼", "偏移值 索尼"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_SONY
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值三星", "偏移值 三星"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_SAMSUNG
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值苹果", "偏移值 苹果"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_APPLE
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值oppo", "偏移值 oppo"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_OPPO
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值vivo", "偏移值 vivo"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_VIVO
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值华为", "偏移值 华为"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_HUAWEI
    await bot.send(ev, fxtext)

@sv.on_fullmatch(["偏移值小米", "偏移值 小米"])
async def offset_query_point(bot, ev):
    fxtext = Wiki_Menu_Achievement_img_2 + OFFSET_MI
    await bot.send(ev, fxtext)


Wiki_Idea_Id_img = R.img(f"musewiki/etc/IconJoyCon.png").cqcode
Wiki_Idea_Tips_img = R.img(f"musewiki/etc/IconHandle.png").cqcode
Wiki_Idea_Main_img = R.img(f"musewiki/etc/button_quetion_blue.png").cqcode

IDEA_MAIN = '''
目前有如下冷知识哦！请选择一项查看
- [游戏之最]
- [小彩蛋]
- [分数公式]
- [科普qa]
- [随机qa]
- [md表情包]
'''.strip()

IDEA_MAX = '''
※MuseDash游戏之最※
BPM(每分钟节拍数)最高的曲目为：MuseDashを作っているPeroPeroGamesさんが倒産しちゃったよ～
BPM值为：33~333（取最高值）

BPM(每分钟节拍数)最低的曲目为：竹
BPM值为：33~333（取最高值）：5~315（取最低值）

难度等级最高的曲目为：
FREEDOM DiVE↓
ouroboros -twin stroke of the end-
XODUS
难度等级为：Level-12（大触&隐藏）
......
'''.strip()

TIPS_QUERY = '''
※MuseDash小彩蛋※
YInMn Blue的单曲成就玩了“114514”的梗。可发送【单曲成就查询YInMn Blue】查看
......
'''.strip()

YF_SCORE = '''
※音符
不受fever影响，不受连击加成，没有打击判定，固定获得200分
'''.strip()
CL_SCORE = '''
※齿轮
包括地面齿轮（可以自然生成和boss丢出）和天空齿轮（一般只能由boss丢出）
不受fever影响，不受连击加成，没有打击判定，固定获得200分
'''.strip()
HX_SCORE = '''
※红心
不受fever影响，不受连击加成，不受打击判定影响
当角色为满血时，获得300分。若角色并非满血，则不得分
'''.strip()
YP_SCORE = '''
※乐谱
长按key的开始和结尾都视为一个“小型怪物击打”，这个得分和怪物击打没有区别，受fever等因素的加成，也能获得combo数（同时这也意味着如果你有一个长按没有打，你会获得两个miss）
长按key的中间一次判定加10分，不受fever影响，不受连击加成影响，没有打击判定
'''.strip()
LD_SCORE = '''
※连打
连打得分不受fever影响，不受连击加成，不受打击判定影响。
连打分为两部分，连打过程（每次点按）和连打结束，其中连打过程每次点按获得20分，结束获得200分。
连打结束时，会获得一个combo
连打有时间限制和次数限制，二者任意一个达到以后连打就会结束。
因未知原因，有时连打的最后一次的20分得分会消失，可能与连打的极限次数有关。
'''.strip()
XD_SCORE = '''
怪物的基本得分为200
小型怪物1.0x
'''.strip()
ZD_SCORE = '''
怪物的基本得分为200
中型怪物1.5x
'''.strip()
DD_SCORE = '''
怪物的基本得分为200
大型怪物2.0x
'''.strip()

yfimg = R.img(f"musewiki/query/scores/音符.png").cqcode
climg = R.img(f"musewiki/query/scores/齿轮.png").cqcode
hximg = R.img(f"musewiki/query/scores/红心.png").cqcode
ypimg = R.img(f"musewiki/query/scores/乐谱.png").cqcode
ldimg = R.img(f"musewiki/query/scores/连打.png").cqcode
xdimg = R.img(f"musewiki/query/scores/小型敌人.png").cqcode
zdimg = R.img(f"musewiki/query/scores/中型敌人.png").cqcode
ddimg = R.img(f"musewiki/query/scores/大型敌人.png").cqcode

yfmain = yfimg + YF_SCORE
clmain = climg + CL_SCORE
hxmain = hximg + HX_SCORE
ypmain = ypimg + YP_SCORE
ldmain = ldimg + LD_SCORE
xdmain = xdimg + XD_SCORE
zdmain = zdimg + ZD_SCORE
ddmain = ddimg + DD_SCORE

DAJI_SCORE = '''
打击判定影响得分
perfect 1.0x
great 0.5x

连击（combo）数会为怪物击打奖励带来加成
0连击1.0x
10连击1.1x
20连击1.2x
30连击1.3x
40连击1.4x
50+连击1.5x
连击在50次或以上以后，就会固定在1.5x的倍率不变
从29连到30连的这一次攻击享受的是30连击的加成，其余同理
因为未知原因，20连击实际的得分为241（而非200x1.2=240）

如果你使用了角色【华服小丑 布若】，则：
50连击1.5x
60连击1.6x
70+连击1.7x
换句话说，华服小丑的连击加成封顶是70连而不是50连。
'''.strip()

FEVER_SCORE = '''
fever状态会带来1.5x的系数加成，如果你携带了精灵【小女巫】，则系数上升到1.7x
特别注意的是：如果你使用的是自动fever，那么让角色进入fever的这一次攻击也会享受fever加成
fever默认持续5秒，携带精灵【喵斯】变为7秒

只有以下行为会获得fever能量：
击打怪物、击打长按key、连打结束
换言之，**只有能获得combo数的行为才能获得fever能量**
fever持续过程中不会获得fever能量

fever能量槽的上限是120，每种行为所获得的能量数量如下：
小型、中型怪物2点
长按key开始和结束2点
大型怪物4点
连打结束4点

同时也会有一些倍率影响
great判定0.5x
魔法少女玛莉嘉1.2x
'''.strip()

@sv.on_fullmatch(["游戏冷知识"])
async def wiki_query_idea(bot, ev):
    final_output = Wiki_Idea_Main_img + IDEA_MAIN
    await bot.send(ev, final_output)
@sv.on_fullmatch(["游戏之最"])
async def wiki_query_idea_max(bot, ev):
    final_output = Wiki_Idea_Id_img + IDEA_MAX
    await bot.send(ev, final_output)
@sv.on_fullmatch(["小彩蛋"])
async def wiki_query_idea_tips(bot, ev):
    final_output = Wiki_Idea_Tips_img + TIPS_QUERY
    await bot.send(ev, final_output)

@sv.on_fullmatch(["分数公式"])
async def wiki_query_score(bot, ev):
    txt = f"本菜单有两项可供查看，请选择查看对象：\n1.基础得分\n2.打击得分\n3.fever得分\n\n※或者发送【全部分数项】查看所有文本"
    await bot.send(ev, txt)

@sv.on_fullmatch(["基础得分"])
async def wiki_query_score_base(bot, ev):
    head = f"感谢musedash吧用户【一墨滢一】的主题帖\nMuse Dash中有以下8种分数项："
    all_text_1 = yfmain + '\n' + clmain + '\n' + hxmain + '\n' + ypmain
    all_text_2 = ldmain + '\n' + xdmain + '\n' + zdmain + '\n' + ddmain
    await bot.send(ev, head)
    await bot.send(ev, all_text_1)
    time.sleep(3)
    await bot.send(ev, all_text_2)

@sv.on_fullmatch(["打击得分"])
async def wiki_query_score_daji(bot, ev):
    await bot.send(ev, DAJI_SCORE)

@sv.on_fullmatch(["fever得分"])
async def wiki_query_score_fever(bot, ev):
    await bot.send(ev, FEVER_SCORE)

@sv.on_fullmatch(["全部分数项"])
async def wiki_query_score_all(bot, ev):
    data = {
    "type": "share",
    "data": {
        "url": "https://tieba.baidu.com/p/6843150739?see_lz=1",
        "title": "【数据党】MuseDash数据考据 分数公式",
        "contene": "from musedash吧 一墨滢一"
        }
    }
    await bot.send(ev, data)

@sv.on_fullmatch(["科普qa"])
async def wiki_query_qa(bot, ev):
    data = {
    "type": "share",
    "data": {
        "url": "https://tieba.baidu.com/p/6181852681?see_lz=1",
        "title": "Muse Dash常见问题Q＆A（科普向）",
        "contene": "from musedash吧"
        }
    }
    await bot.send(ev, data)

qa_folder = R.img('musewiki/query/qa/').path

def qa_gener_pic():
    while True:
        filelist_qa = os.listdir(qa_folder)
        random.shuffle(filelist_qa)
        for filename in filelist_qa:
            if os.path.isfile(os.path.join(qa_folder, filename)):
                yield R.img('musewiki/query/qa/', filename)

qa_gener_pic = qa_gener_pic()

def get_qas():
    return qa_gener_pic.__next__()

@sv.on_fullmatch(["随机qa"])
async def wiki_query_ranqa(bot, ev):
    pic = get_qas()
    try:
        await bot.send(ev, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"MuseDash百科-资料查询，发送QA图片{pic.path}失败")
        try:
            await bot.send(ev, '发送图片失败...')
        except:
            pass

fun_folder = R.img('musewiki/query/表情包/').path

def fun_gener_pic():
    while True:
        filelist_fun = os.listdir(fun_folder)
        random.shuffle(filelist_fun)
        for filename in filelist_fun:
            if os.path.isfile(os.path.join(fun_folder, filename)):
                yield R.img('musewiki/query/表情包/', filename)

fun_gener_pic = fun_gener_pic()

def get_funs():
    return fun_gener_pic.__next__()

@sv.on_fullmatch(["md表情包"])
async def wiki_query_ranemoji(bot, ev):
    pic = get_funs()
    try:
        await bot.send(ev, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"MuseDash百科-资料查询，发送表情包{pic.path}失败")
        try:
            await bot.send(ev, '发送表情包失败...')
        except:
            pass