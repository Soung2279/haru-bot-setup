import random
import asyncio
from hoshino import Service, util, priv, config
from hoshino.typing import CQEvent
import time
from .choicer import Choicer

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv_help = '''
- [今天我是什么少女]  查看今天的自己
- [今天你是什么少女 @人]  查看今天的他人
'''.strip()

sv = Service(
    name = '今天也是少女',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助今天也是少女"])
async def bangzhu_shaojo(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

inst = Choicer(util.load_config(__file__))

@sv.on_fullmatch('今天我是什么少女')
async def my_shoujo(bot, ev: CQEvent):
    uid = ev.user_id
    name = ev.sender['card'] or ev.sender['nickname']
    msg = inst.format_msg(uid, name)
    if forward_msg_exchange == 1:
        data = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": msg
            }
        }
        if recall_msg_set == 1:
            recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)
    else:
        if recall_msg_set == 1:
            recall_1 = await bot.send(ev, msg)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall_1['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send(ev, msg)


@sv.on_prefix('今天你是什么少女')
@sv.on_suffix('今天你是什么少女')
async def other_shoujo(bot, ev: CQEvent):
    arr = []
    for i in ev.message:
        if i['type'] == 'at' and i['data']['qq'] != 'all':
            arr.append(int(i['data']['qq']))
    gid = ev.group_id
    for uid in arr:
        info = await bot.get_group_member_info(
                group_id=gid,
                user_id=uid,
                no_cache=True
        )
        name = info['card'] or info['nickname']
        msg = inst.format_msg(uid, name)
        if forward_msg_exchange == 1:
            data = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": msg
            }
        }
        if recall_msg_set == 1:
            recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)
    else:
        if recall_msg_set == 1:
            recall_1 = await bot.send(ev, msg)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall_1['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send(ev, msg)
