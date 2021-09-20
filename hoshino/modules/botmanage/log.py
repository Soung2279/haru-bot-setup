import re
import asyncio
import hoshino
from nonebot import on_command
from hoshino import Service, priv, config
from hoshino.typing import CQEvent

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID

recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv = Service('_botlog_', manage_priv=priv.SUPERUSER, visible=False, enable_on_default=True)

LOG = '''
2021.9.21 bot更新日志
=====================
- 更新 -
新增以下功能：
百度一下：懒人福音，群聊中直接发送搜索链接，详细指令请发送【帮助百度一下】查看
vtb名单：查询某人是否为虚拟主播，并给出相关信息，可模糊匹配，详细指令请发送【帮助vtb名单】查看

- 修复 -
修复部分依赖文件冲突
=====================
如有建议请使用【来杯咖啡】【额外说明】或进入群聊：1121815503
'''.strip()



EXTRA_TIP = '''
额外说明：
bot帮助界面
【腾讯文档】soungbothelp
https://docs.qq.com/sheet/DUXlISFNFS1BnZFlF
此文档包含了所有服务层的可触发指令。

也可以在群聊中让管理员发送lssv。查看本群搭载的服务，并使用帮助+服务名来查看详细的帮助文档。
例如：【帮助雀魂查询】
'''.strip()

@sv.on_fullmatch(('额外说明', 'extratip'))
async def extra_log(bot, ev):
    await bot.send(ev, f"{EXTRA_TIP}")

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
#  设定是否启用转发群消息的样式发送消息。1是启用，0是禁用。

@sv.on_fullmatch(["更新日志", "botlog"])
async def upgrate_log(bot, ev):
    gid = ev.group_id
    if forward_msg_exchange == 1:
        msg = LOG  #转发文本
        data = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",  #bot转发消息中的名称
                "uin": f"{forward_msg_uid}",  #bot转发使用的画像（头像）
                "content": msg  #转发文本
            }
        }
        if recall_msg_set == 1:
            msg = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=msg['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)
    else:
        if recall_msg_set == 1:
            msg = await bot.send(ev, LOG)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=msg['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send(ev, LOG)