from typing import Text
import requests, asyncio, os

import hoshino
from hoshino import Service, priv, aiorequests, R
from hoshino.modules.musedash import _song_data
from hoshino.typing import CQEvent, MessageSegment
import time, random
from operator import __iadd__
from nonebot.exceptions import CQHttpError
from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter, escape, DailyNumberLimiter

_max = 1
_nlmt = DailyNumberLimiter(_max)

forward_msg_name = 'SoungBot测试版'
forward_msg_uid = '756160433'

Wiki_Menu_Query_img = R.img(f"musewiki/etc/query.png").cqcode

sv_help = '''
※MuseDash百科-资料查询※

[peropero]  随机播放一条起始(peropero~games~)语音
[查询隐藏曲目]  查询隐藏曲目的解锁方式
[偏移值参考]  查询游戏偏移值设定参考
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
    if not _nlmt.check(uid):
        await bot.send(ev, f"欢迎继续使用MuseDash百科-资料查询！")
    else:
        await bot.send(ev, voice_rec)
    
    _nlmt.increase(uid)
    final_output = Wiki_Menu_Query_img + sv_help
    await bot.send(ev, final_output)

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
Base_in_1 = basepic1 + BASE1_IN_QUERY + Base_Cover_Img

basepic2 = R.img(f"musewiki/songcover/儿童鞋垫.png").cqcode
BASE2_IN_QUERY = f"歌曲名：もぺもぺ\n解锁方式：狂按大触\n来源：基础包"
Base_in_2 = basepic2 + BASE2_IN_QUERY + Base_Cover_Img

basepic3 = R.img(f"musewiki/songcover/irreplaceable.png").cqcode
BASE3_IN_QUERY = f"歌曲名：lrreplaceable feat.AKINO wish bless4\n解锁方式：狂按大触\n来源：基础包：经费在燃烧:纳米核心"
Base_in_3 = basepic3 + BASE3_IN_QUERY + Base_Cover_Img

basepic4 = R.img(f"musewiki/songcover/stargezer.png").cqcode
BASE4_IN_QUERY = f"歌曲名：Stargezer\n解锁方式：狂按大触\n来源：基础包：经费在燃烧 Vol.1"
Base_in_4 = basepic4 + BASE4_IN_QUERY + Base_Cover_Img

givenpic1 = R.img(f"musewiki/songcover/trippers feeling.png").cqcode
GIVEN1_IN_QUERY = f"歌曲名：trippers feeling!\n解锁方式：狂按大触\n歌曲位置：放弃治疗包 Vol.3"
Given_in_1 = givenpic1 + GIVEN1_IN_QUERY + Given_Cover_Img

givenpic2 = R.img(f"musewiki/songcover/万圣节.png").cqcode
GIVEN2_IN_QUERY = f"歌曲名：Sweet*Witch*Girls*\n解锁方式：将系统时间调整至2019年万圣节（2019.11.1）进入曲目即可看到\n歌曲位置：放弃治疗包 Vol.3"
Given_in_2 = givenpic2 + GIVEN2_IN_QUERY + Given_Cover_Img

givenpic3 = R.img(f"musewiki/songcover/freedom.png").cqcode
GIVEN3_IN_QUERY = f"歌曲名：FREEDOM DiVE↓\n解锁方式：在大触界面顺时针画3-5个圈圈\n歌曲位置：放弃治疗包 Vol.8"
Given_in_3 = givenpic3 + GIVEN3_IN_QUERY + Given_Cover_Img

otakupic1 = R.img(f"musewiki/songcover/goodtek.png").cqcode
OTAKU1_IN_QUERY = f"歌曲名：GOODTEK(Hyper Edit)\n解锁方式：将系统时间调整至2019年愚人节（2019.4.1）进入曲目即可看到\n歌曲位置：肥宅快乐包 Vol.2"
Otaku_in_1 = otakupic1 + OTAKU1_IN_QUERY + Otaku_Cover_Img

otakupic2 = R.img(f"musewiki/songcover/xing.png").cqcode
OTAKU2_IN_QUERY = f"歌曲名：XING\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.3"
Otaku_in_2 = otakupic2 + OTAKU2_IN_QUERY + Otaku_Cover_Img

otakupic3 = R.img(f"musewiki/songcover/conflict.png").cqcode
OTAKU3_IN_QUERY = f"歌曲名：conflict\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.3"
Otaku_in_3 = otakupic3 + OTAKU3_IN_QUERY + Otaku_Cover_Img

otakupic4 = R.img(f"musewiki/songcover/infinite energy.png").cqcode
OTAKU4_IN_QUERY = f"歌曲名：INFiNiTE ENERZY -Overdoze-\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.8"
Otaku_in_4 = otakupic4 + OTAKU4_IN_QUERY + Otaku_Cover_Img

otakupic5 = R.img(f"musewiki/songcover/ginevra.png").cqcode
OTAKU5_IN_QUERY = f"歌曲名：Ginevra\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.10"
Otaku_in_5 = otakupic5 + OTAKU5_IN_QUERY + Otaku_Cover_Img

otakupic6 = R.img(f"musewiki/songcover/square lake.png").cqcode
OTAKU6_IN_QUERY = f"歌曲名：Square Lake\n解锁方式：狂按大触\n歌曲位置：肥宅快乐包 Vol.11"
Otaku_in_6 = otakupic6 + OTAKU6_IN_QUERY + Otaku_Cover_Img

otakupic7 = R.img(f"musewiki/songcover/medusa.png").cqcode
OTAKU7_IN_QUERY = f"歌曲名：Medusa\n解锁方式：狂按高手\n歌曲位置：肥宅快乐包 Vol.11"
Otaku_in_7 = otakupic7 + OTAKU7_IN_QUERY + Otaku_Cover_Img

otakupic8 = R.img(f"musewiki/songcover/dataerror.png").cqcode
OTAKU8_IN_QUERY = f"歌曲名：DataError\n解锁方式：狂按高手\n歌曲位置：肥宅快乐包 SP"
Otaku_in_8 = otakupic8 + OTAKU8_IN_QUERY + Otaku_Cover_Img

collabpic1 = R.img(f"musewiki/songcover/igallta.png").cqcode
COLLAB1_IN_QUERY = f"歌曲名：igallta\n解锁方式：狂按大触\n歌曲位置：Phigros"
Collab_in_1 = collabpic1 + COLLAB1_IN_QUERY + Collab_Cover_Img

collabpic2 = R.img(f"musewiki/songcover/batle no1.png").cqcode
COLLAB2_IN_QUERY = f"歌曲名：BATTLE NO.1\n解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_2 = collabpic2 + COLLAB2_IN_QUERY + Collab_Cover_Img

collabpic3 = R.img(f"musewiki/songcover/cthugha.png").cqcode
COLLAB3_IN_QUERY = f"歌曲名：Cthugha\n解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_3 = collabpic3 + COLLAB3_IN_QUERY + Collab_Cover_Img

collabpic4 = R.img(f"musewiki/songcover/twinkle magic.png").cqcode
COLLAB4_IN_QUERY = f"歌曲名：TWINKLE★MAGIC\n解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_4 = collabpic4 + COLLAB4_IN_QUERY + Collab_Cover_Img

collabpic4v5 = R.img(f"musewiki/songcover/comet coaster.png").cqcode
COLLAB4v5_IN_QUERY = f"歌曲名：Comet Coaster\n解锁方式：解锁方式：狂按大触\n歌曲位置：HARDCORE TANO*C"
Collab_in_4v5 = collabpic4v5 + COLLAB4v5_IN_QUERY + Collab_Cover_Img

collabpic5 = R.img(f"musewiki/songcover/xodus.png").cqcode
COLLAB5_IN_QUERY = f"歌曲名：XODUS\n解锁方式：在大触界面画很多个 X\n歌曲位置：HARDCORE TANO*C"
Collab_in_5 = collabpic5 + COLLAB5_IN_QUERY + Collab_Cover_Img

collabpic6 = R.img(f"musewiki/songcover/happiness breeze.png").cqcode
COLLAB6_IN_QUERY = f"歌曲名：Happiness Breeze\n解锁方式：狂按大触\n歌曲位置：cyTus"
Collab_in_6 = collabpic6 + COLLAB6_IN_QUERY + Collab_Cover_Img

collabpic7 = R.img(f"musewiki/songcover/chrome.png").cqcode
COLLAB7_IN_QUERY = f"歌曲名：Chrome VOX\n解锁方式：狂按大触\n歌曲位置：cyTus"
Collab_in_7 = collabpic7 + COLLAB7_IN_QUERY + Collab_Cover_Img

collabpic8 = R.img(f"musewiki/songcover/chaos.png").cqcode
COLLAB8_IN_QUERY = f"歌曲名：CHAOS\n解锁方式：在收藏系统内打开Cytus2欢迎界面插画，等待几秒后凛桌子上的手机（键盘左边）会有CHAOS图标。在拨号结束前点击CHAOS图标或者电话按钮即可进入隐藏铺界面。\n歌曲位置：cyTus"
Collab_in_8 = collabpic8 + COLLAB8_IN_QUERY + Collab_Cover_Img

collabpic9 = R.img(f"musewiki/songcover/fujin.png").cqcode
COLLAB9_IN_QUERY = f"歌曲名：FUJIN Rumble\n解锁方式：狂按大触\n歌曲位置：Let's GROOVE!"
Collab_in_9 = collabpic9 + COLLAB9_IN_QUERY + Collab_Cover_Img

collabpic10 = R.img(f"musewiki/songcover/HG魔改造.png").cqcode
COLLAB10_IN_QUERY = f"歌曲名：HG魔改造ポリビニル少年\n解锁方式：狂按大触\n歌曲位置：Let's GROOVE!"
Collab_in_10 = collabpic10 + COLLAB10_IN_QUERY + Collab_Cover_Img

collabpic11 = R.img(f"musewiki/songcover/ouroboros.png").cqcode
COLLAB11_IN_QUERY = f"歌曲名：ouroboros -twin stroke of the end-\n解锁方式：在难度选择界面从大触难度开始按照高手-萌新-高手-大触-高手-萌新-高手-大触的顺序点击难度选择按钮，构成衔尾蛇即可解锁隐藏谱面。\n歌曲位置：Let's GROOVE!"
Collab_in_11 = collabpic11 + COLLAB11_IN_QUERY + Collab_Cover_Img

fmpic1 = R.img(f"musewiki/songcover/ouroboros.png").cqcode
FM_IN_QUERY = f"歌曲名：FM17314 SUGAR RADIO\n长按 去剪海的日子(暮色电台FM102)曲绘，直至圆圈转完为止即可进入隐藏曲\n来源：暮色电台FM102"
FM_in_1 = fmpic1 + FM_IN_QUERY + FM_Cover_Img

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
    final_1 = Otaku_in_1 + '\n' + Otaku_in_2 + '\n' + Otaku_in_3 
    final_2 = Otaku_in_4 + '\n' + Otaku_in_5 + '\n' + Otaku_in_6
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
