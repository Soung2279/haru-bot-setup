import time
import json
import requests

from datetime import datetime
from copy import deepcopy
from os.path import dirname, join, exists
import hoshino
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter, DailyNumberLimiter

_nlmt = DailyNumberLimiter(2)  #上限次数
_cd = 10  #调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)

sv_help = '''
- [最近假期] 查看最近的假期时间
- [剩余假期] 查看今年剩余的假期
- [查看调休] 查看调休时间
'''.strip()

sv = Service(
    name = '假期查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助假期查询"])
async def bangzhu_holiday(bot, ev):
    await bot.send(ev, sv_help)

today = time.time()

curpath = dirname(__file__)
config = join(curpath, 'data.json')
if exists(config):
    with open(config) as fp:
        root = json.load(fp)

holiday = root['holiday']
holiday_cache = {}
holiday_cache = deepcopy(holiday)

def get_week_day(day):
    week_day_dict = {
        0 : '星期一',
        1 : '星期二',
        2 : '星期三',
        3 : '星期四',
        4 : '星期五',
        5 : '星期六',
        6 : '星期日',
    }
    return week_day_dict[day]

@sv.on_fullmatch(["最近假期", "近期假期", "临近假期", "最近假日", "近期假日", "临近假日"])
async def current_holiday(bot, ev: CQEvent):
    uid = ev['user_id']
    if not uid in hoshino.config.SUPERUSERS:
        if not _flmt.check(uid):
            await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
            return
        if not _nlmt.check(uid):
            await bot.send(ev, f"避免重复使用导致刷屏，此消息已忽略")
            return
    for data in holiday_cache:
        info = holiday_cache[data]
        timeArray = time.strptime(info['date'], "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        if info['holiday'] == True and today < timeStamp:
            time_int = int((timeStamp - today)/86400)+ 1
            name = info['name']
            msg = f"最近的假期是{name}哦！还有{time_int}天~"
            _flmt.start_cd(uid)
            _nlmt.increase(uid)
            await bot.send(ev, msg)
            return

@sv.on_fullmatch(["剩余假期", "余下假期", "剩余假日", "余下假日"])
async def year_holiday(bot, ev: CQEvent):
    uid = ev['user_id']
    false_holiday = 0
    holiday = 0
    msg = '今年剩余的假期有:\n'
    if not uid in hoshino.config.SUPERUSERS:
        if not _flmt.check(uid):
            await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
            return
        if not _nlmt.check(uid):
            await bot.send(ev, f"避免重复使用导致刷屏，此消息已忽略")
            return
    for data in holiday_cache:
        info = holiday_cache[data]
        timeArray = time.strptime(info['date'], "%Y-%m-%d")
        timeStamp = time.mktime(timeArray)
        if info['holiday'] == True and today < timeStamp:
            day = datetime.strptime(info['date'], "%Y-%m-%d").weekday()
            if day == 5 or day == 6:
                false_holiday = false_holiday + 1
            time_int = int((timeStamp - today)/86400)+ 1
            name = info['name']
            date = info['date']
            msg = msg + f'{date}{name},还有{time_int}天' + '\n'
            holiday = holiday +1
        elif info['holiday'] == False and today < timeStamp:
            false_holiday = false_holiday + 1
    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    real_holiday = holiday - false_holiday
    msg = msg + f'共{holiday}天\n减去调休与周末后剩余假期为{real_holiday}天'
    await bot.send(ev, msg)


@sv.on_fullmatch(["查看调休", "查询调休"])
async def false_holiday(bot, ev: CQEvent):
    msg = '今年剩余的调休日为:\n'
    for data in holiday_cache:
        info = holiday_cache[data]
        timeArray = time.strptime(info['date'], "%Y-%m-%d")
        timeStamp = time.mktime(timeArray)
        if info['holiday'] == False and today < timeStamp:
            day = datetime.strptime(info['date'], "%Y-%m-%d").weekday()
            week = get_week_day(day)
            date = info['date']
            msg = msg + f'{date},{week}' + '\n'
    await bot.send(ev, msg)


#每天四点更新假期数据
@sv.scheduled_job('cron',hour='4')
async def today_holiday():
    url = 'http://timor.tech/api/holiday/year'
    r = requests.get(url)
    holiday = r.json()

    with open('data.json', 'w') as f:
        json.dump(holiday, f)
    

@sv.on_fullmatch(["更新假期数据", "更新假日数据"])
async def today_holiday(bot, ev: CQEvent):
    now = datetime.now()  #获取当前时间
    hour = now.hour  #获取当前时间小时数
    minute = now.minute  #获取当前时间分钟数
    hour_str = f' {hour}' if hour<10 else str(hour)
    minute_str = f' {minute}' if minute<10 else str(minute)
    if not priv.check_priv(ev, priv.SUPERUSER):
        sv.logger.warning(f"非管理者：{ev.user_id}尝试于{hour_str}点{minute_str}分手动更新假期数据")
        await bot.send(ev, "只有bot主人才能使用此命令哦~")
        return

    url = 'http://timor.tech/api/holiday/year'
    r = requests.get(url)
    holiday = r.json()

    with open('data.json', 'w') as f:
        json.dump(holiday, f)

    data = {
    "type": "share",
    "data": {
        "url": "http://timor.tech/api/holiday/",
        "title": "提莫的神秘商店 - 免费节假日 API",
        "contene": ""
        }
    }

    await bot.send(ev, f"数据更新完成。可前往api查看最新数据。")
    await bot.send(ev, data)