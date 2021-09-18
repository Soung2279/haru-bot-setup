# coding=utf-8
import hoshino
from hoshino import Service, priv, config
from hoshino.typing import HoshinoBot,CQEvent
from hoshino.util import FreqLimiter, DailyNumberLimiter
from os.path import join
from .Life import Life
from .PicClass import *
import traceback
import random

_max = 15  #每日上限
_nlmt = DailyNumberLimiter(_max)
_cd = 10  #调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)
main_path = hoshino.config.RES_DIR  #使用在 _bot_.py 里填入的资源库文件夹
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID

sv_help = '''
- [/remake]
- [人生重来]
'''.strip()

sv = Service(
    name = '人生重来模拟器',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助人生重来模拟器", "帮助人生重来"])
async def bangzhu_push_songs(bot, ev):
    await bot.send(ev, sv_help)

def genp(prop):
    ps = []
    # for _ in range(4):
    #     ps.append(min(prop, 8))
    #     prop -= ps[-1]
    tmp = prop
    while True:
        for i in range(0,4):
            if i == 3:
                ps.append(tmp)
            else:
                if tmp>=10:
                    ps.append(random.randint(0, 10))
                else:
                    ps.append(random.randint(0, tmp))
                tmp -= ps[-1]
        if ps[3]<10:
            break
        else:
            tmp = prop
            ps.clear()
    return {
        'CHR': ps[0],
        'INT': ps[1],
        'STR': ps[2],
        'MNY': ps[3]
    }

@sv.on_fullmatch(["/remake","人生重来"])
async def remake(bot,ev:CQEvent):
    pic_list = []
    mes_list = []
    uid = ev['user_id']

    if not _flmt.check(uid):
        await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
        return
    _flmt.start_cd(uid)

    Life.load(join(FILE_PATH,'data'))
    while True:
        life = Life()
        life.setErrorHandler(lambda e: traceback.print_exc())
        life.setTalentHandler(lambda ts: random.choice(ts).id)
        life.setPropertyhandler(genp)
        flag = life.choose()
        if flag:
            break

    name = ev["sender"]['card'] or ev["sender"]["nickname"]
    choice = 0
    person = name + "本次重生的基本信息如下：\n\n【你的天赋】\n"
    for t in life.talent.talents:
        choice = choice + 1
        person = person + str(choice) + "、天赋：【" + t.name + "】" + " 效果:" + t.desc + "\n"

    person = person + "\n【基础属性】\n"
    person = person + "   美貌值:" + str(life.property.CHR)+"  "
    person = person + "智力值:" + str(life.property.INT)+"  "
    person = person + "体质值:" + str(life.property.STR)+"  "
    person = person + "财富值:" + str(life.property.MNY)+"  "
    pic_list.append("这是"+name+"本次轮回的基础属性和天赋:")
    pic_list.append(ImgText(person).draw_text())

    await bot.send(ev, "你的命运正在重启....",at_sender=True)

    res = life.run() #命运之轮开始转动
    mes = '\n'.join('\n'.join(x) for x in res)
    pic_list.append("这是"+name+"本次轮回的生平:")
    pic_list.append(ImgText(mes).draw_text())

    sum = life.property.gensummary() #你的命运之轮到头了
    pic_list.append("这是" + name + "本次轮回的评价:")
    pic_list.append(ImgText(sum).draw_text())

    '''
    for img in pic_list:
        data = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": img
            }
        }
        mes_list.append(data)
    '''
    #await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
    #await bot.send_group_msg(group_id=ev['group_id'], messages=mes_list)
    #await bot.send(ev, str(mes_list))
    #await bot.send(ev, str(pic_list))

    if not _nlmt.check(uid):
        await bot.send(ev, f"今日已经使用{_max}次了哦~")
        return
    else:
        await bot.send(ev, str(mes_list))
        await bot.send(ev, str(pic_list))
    _nlmt.increase(uid)
    #await bot.send_group_msg(group_id=ev['group_id'], messages=pic_list)
