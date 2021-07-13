# coding=utf-8
import hoshino
import asyncio

from hoshino import Service, priv, config
from hoshino.typing import CQEvent

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv_help = '''
由于牌谱屋不收录铜之间以及银之间牌谱，故所有数据仅统计2019年11月29日后金场及以上场次的数据
PS：暂时只支持四麻对局的查询
'''.strip()

majsoul_help_1 = '''
查询指令：
- [雀魂信息/雀魂查询 昵称]  查询该ID的雀魂基本对局数据(包含金场以上所有)
- [三麻信息/三麻查询 昵称]  查询该ID雀魂三麻的基本对局数据(包含金场以上所有)
- [雀魂信息/雀魂查询 (金/金之间/金场/玉/王座) 昵称]  查询该ID在金/玉/王座之间的详细数据
- [三麻信息/三麻查询 (金/金之间/金场/玉/王座) 昵称]  查询该ID在三麻金/玉/王座之间的详细数据
- [雀魂牌谱 昵称]  查询该ID下最近五场的对局信息
- [三麻牌谱 昵称]  查询该ID下最近五场的三麻对局信息
'''.strip()

majsoul_help_2 = '''
对局订阅指令：
- [雀魂订阅 昵称]  订阅该昵称在金之间以上的四麻对局信息 
- [三麻订阅 昵称]  订阅该昵称在金之间以上的三麻对局信息 
- [(取消/关闭)雀魂订阅 昵称]  将该昵称在本群的订阅暂时关闭 
- [(取消/关闭)三麻订阅 昵称]  将该昵称在本群的三麻订阅暂时关闭 
- [开启雀魂订阅 昵称]  将该昵称在本群的订阅开启 
- [开启三麻订阅 昵称]  将该昵称在本群的三麻订阅开启 
- [删除雀魂订阅 昵称]  将该昵称在本群的订阅删除
- [删除三麻订阅 昵称]  将该昵称在本群的三麻订阅删除
- [雀魂订阅状态]  查询本群的雀魂订阅信息的开启状态 
- [三麻订阅状态]  查询本群的雀魂订阅信息的开启状态 
'''.strip()

sv = Service(
    name = '雀魂查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'○' if sv.check_enabled(gid) else '×'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)

@sv.on_fullmatch(["帮助雀魂查询"])
async def bangzhu_majsoul(bot, ev: CQEvent):
    if forward_msg_exchange == 1:
        data_all = []
        msg1 = sv_help
        data1 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": msg1
            }
        }
        msg2 = majsoul_help_1
        data2 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": msg2
                }
            }
        msg3 = majsoul_help_2
        data3 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": msg3
                }
            }
        data_all=[data1,data2,data3]
        if recall_msg_set == 1:
            recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")
                
            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
    else:
        if recall_msg_set == 1:
            recall_1 = await bot.send(ev, sv_help)
            recall_2 = await bot.send(ev, majsoul_help_1)
            recall_3 = await bot.send(ev, majsoul_help_2)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall_1['message_id'])
            await bot.delete_msg(message_id=recall_2['message_id'])
            await bot.delete_msg(message_id=recall_3['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send(ev, sv_help)
            await bot.send(ev, majsoul_help_1)
            await bot.send(ev, majsoul_help_2)


