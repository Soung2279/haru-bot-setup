import base64
from .generate import *
from io import BytesIO
import hoshino
import nonebot
import os
import re
import traceback
from hoshino import Service, priv
from hoshino.typing import CQEvent

sv_help = '''
崩3活动日历
- [崩3日历] : 查看本群订阅服务器日历
- [崩3日历 on/off] : 订阅/取消订阅指定服务器的日历推送
- [崩3日历 time 时:分] : 设置日历推送时间
- [崩3日历 status] : 查看本群日历推送设置
'''.strip()

sv = Service(
    name = '崩3日历',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '订阅', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助假期查询"])
async def bangzhu_holiday(bot, ev):
    await bot.send(ev, sv_help)

group_data = {}


def load_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding='utf8') as f:
            data = json.load(f)
            for k, v in data.items():
                group_data[k] = v
    except:
        traceback.print_exc()


def save_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(group_data, f, ensure_ascii=False, indent=2)
    except:
        traceback.print_exc()


async def send_calendar(group_id):
    bot = hoshino.get_bot()
    available_group = await sv.get_enable_groups()
    if str(group_id) not in group_data or int(group_id) not in available_group:
        return
    for server in group_data[str(group_id)]['server_list']:
        im = await generate_day_schedule(server)
        base64_str = im2base64str(im)
        if 'cardimage' not in group_data[group_id] or not group_data[group_id]['cardimage']:
            msg = f'[CQ:image,file={base64_str}]'
        else:
            msg = f'[CQ:cardimage,file={base64_str}]'
        for _ in range(5):  # 失败重试5次
            try:
                await bot.send_group_msg(group_id=int(group_id), message=msg)
                sv.logger.info(f'群{group_id}推送{server}日历成功')
                break
            except:
                sv.logger.info(f'群{group_id}推送{server}日历失败')
            await asyncio.sleep(60)


def update_group_schedule(group_id):
    group_id = str(group_id)
    if group_id not in group_data:
        return
    nonebot.scheduler.add_job(
        send_calendar,
        'cron',
        args=(group_id,),
        id=f'calendar_{group_id}',
        replace_existing=True,
        hour=group_data[group_id]['hour'],
        minute=group_data[group_id]['minute']
    )


@sv.on_rex(r'^崩坏?[3三]日[历程](.*)')
async def start_scheduled(bot, ev):
    group_id = str(ev['group_id'])
    server = 'cn'
    cmd = ev['match'].group(1)
    if not cmd:
        im = await generate_day_schedule(server)
        base64_str = im2base64str(im)
        if group_id not in group_data or 'cardimage' not in group_data[group_id] or not group_data[group_id]['cardimage']:
            msg = f'[CQ:image,file={base64_str}]'
        else:
            msg = f'[CQ:cardimage,file={base64_str}]'
    else:
        if group_id not in group_data:
            group_data[group_id] = {
                'server_list': [],
                'hour': 8,
                'minute': 0,
                'cardimage': False,
            }
        if not hoshino.priv.check_priv(ev, hoshino.priv.ADMIN):
            return
            msg = '权限不足'
        elif 'on' in cmd:
            if server not in group_data[group_id]['server_list']:
                group_data[group_id]['server_list'].append(server)
            save_data()
            msg = f'崩3日程推送已开启'
        elif 'off' in cmd:
            if server in group_data[group_id]['server_list']:
                group_data[group_id]['server_list'].remove(server)
            save_data()
            msg = f'崩3日程推送已关闭'
        elif 'time' in cmd:
            match = re.search(r'(\d*):(\d*)', cmd)
            if not match or len(match.groups()) < 2:
                msg = '请指定推送时间'
            else:
                group_data[group_id]['hour'] = int(match.group(1))
                group_data[group_id]['minute'] = int(match.group(2))
                msg = f"推送时间已设置为: {group_data[group_id]['hour']}:{group_data[group_id]['minute']:02d}"
        elif 'status' in cmd:
            msg = f"订阅日历: {group_data[group_id]['server_list']}"
            msg += f"\n推送时间: {group_data[group_id]['hour']}:{group_data[group_id]['minute']:02d}"
        elif 'cardimage' in cmd:
            if 'cardimage' not in group_data[group_id] or not group_data[group_id]['cardimage']:
                group_data[group_id]['cardimage'] = True
                msg = f'已切换为cardimage模式'
            else:
                group_data[group_id]['cardimage'] = False
                msg = f'已切换为标准image模式'
            save_data()
        else:
            return
            msg = '指令错误'
        update_group_schedule(group_id)
        save_data()
    await bot.send(ev, msg)


@nonebot.on_startup
async def startup():
    load_data()
    for group_id in group_data:
        update_group_schedule(group_id)
