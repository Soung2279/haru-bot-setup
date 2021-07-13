import hoshino
import asyncio
import re
from itertools import zip_longest

from nonebot.message import escape

from hoshino import Service, priv, config
from hoshino.typing import CQEvent

from . import yinglish

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv2_help = '''
- [淦翻译 XX] 好涩哦
'''.strip()

sv2 = Service(
    name = '怪话翻译',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv2_help #帮助文本
    )

@sv2.on_fullmatch(["帮助怪话翻译"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv2_help, at_sender=True)


def chs2yin(s, 淫乱度=1):
    return

@sv2.on_prefix('淦翻译')
async def ganfanyi(bot, ev: CQEvent):
    s = ev.message.extract_plain_text()
    if len(s) > 500:
        await bot.send(ev, '淦，内容太多，翻译不了', at_sender=True)
        return
    if len(s) < 1:
        await bot.send(ev, '淦！')
        return
    if forward_msg_exchange == 1:
        msg = yinglish.chs2yin(s)
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
            recall_1 = await bot.send(ev, yinglish.chs2yin(s))
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall_1['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send(ev, yinglish.chs2yin(s))



    

