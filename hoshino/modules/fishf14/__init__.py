import asyncio
import hoshino

from hoshino import Service, priv, config
from nonebot import MessageSegment

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv_help = '''
ff14钓鱼笔记帮助指北
- [钓鱼笔记+需查询的鱼的名字]
- [钓鱼区域+地图名称]
'''.strip()

sv = Service(
    name = 'ff14钓鱼',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助ff14钓鱼", "ff14帮助", "帮助ff14"])
async def bangzhu_ff14(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

from .fishtool import Fish
fish = Fish()


@sv.on_prefix(('钓鱼笔记', '钓鱼日记'))
async def diaoyu(bot, ev):
    uid = ev.user_id
    msg = ev.message.extract_plain_text().strip()
    if not msg:
        await bot.finish(ev, sv_help)
    result = fish.search_fish(msg)
    if result is None:
        await bot.send(ev, '没有查询到结果呢，输入有误或者数据未收录', at_sender=True)
    else:
        at = MessageSegment.at(uid)
        reply = f'已为{at}找到如下结果：\n{result}'
        if forward_msg_exchange == 1:
            msg = reply
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
                recall_1 = await bot.send(ev, reply)
                notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

                await asyncio.sleep(RECALL_MSG_TIME)

                await bot.delete_msg(message_id=recall_1['message_id'])
                await bot.delete_msg(message_id=notice['message_id'])
            else:
                await bot.send(ev, reply)  


@sv.on_prefix('钓鱼区域')
async def area(bot, ev):
    uid = ev.user_id
    msg = ev.message.extract_plain_text().strip()
    if not msg:
        await bot.finish(ev, sv_help)
    result = fish.search_area(msg)
    if result is None:
        await bot.send(ev, '所选区域有误', at_sender=True)
    else:
        at = MessageSegment.at(uid)
        reply = f'已为{at}找到如下结果：\n{result}'
        if forward_msg_exchange == 1:
            msg = reply
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
                recall_1 = await bot.send(ev, reply)
                notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

                await asyncio.sleep(RECALL_MSG_TIME)

                await bot.delete_msg(message_id=recall_1['message_id'])
                await bot.delete_msg(message_id=notice['message_id'])
            else:
                await bot.send(ev, reply)        
