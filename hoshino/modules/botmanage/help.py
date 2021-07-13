from hoshino import Service, priv, config
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID

TOP_MANUAL_1 = '''
使用说明:
查看当前bot更新：[更新日志]
方括号[ ]内为指令，在群聊中发送指令即可
'''.strip()

TOP_MANUAL_2 = '''
※本bot有五类功能，触发关键词：
- [帮助订阅]
- [帮助查询]
- [帮助娱乐]
- [帮助通用]
- [帮助原神]
- [帮助extra]
- *[帮助advance] #多数情况下不会用到此项。
'''.strip()

TOP_MANUAL_3 = '''
※查看单个功能详情
开启功能后发送：
- [帮助XXX] （无空格）
XXX为功能名。例如：帮助智能闲聊
'''.strip()

TOP_MANUAL_4 = '''
※绝大多数功能的开关需群管及以上权限
※控制功能开关:
- [启用 XXX] （有空格）
- [禁用 XXX] （有空格）
XXX为功能名。例如：启用 智能闲聊
※本群功能开关总览:
- [lssv]
'''.strip()

TOP_MANUAL_0 = '''
SoungBot使用指南

'''.strip()

TOP_MANUAL_TEXT = '''
文本帮助
'''.strip()


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

@sv.on_prefix(('help', '帮助'))
async def send_help(bot, ev: CQEvent):
    gid = ev.group_id
    services = Service.get_bundles()
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if not bundle_name:
        data_all = []
        data1 ={
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": TOP_MANUAL_1
            }
        }
        data2 ={
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": TOP_MANUAL_2
            }
        }    
        data3 ={
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": TOP_MANUAL_3
            }
        }
        data4 ={
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": TOP_MANUAL_4
            }
        }
        data_all=[data1,data2,data3,data4]
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
        await bot.send(ev, f'当前版本{config.VERSION}')
    elif bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
        data_all = []
        data1 ={
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": msg
            }
            }
        data2 ={
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": TOP_MANUAL_3
            }
            }    
        data_all=[data1,data2]    
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
        await bot.send(ev, f'当前版本{config.VERSION}')


@sv.on_fullmatch(["文字帮助", "文本帮助", "备用帮助", "文本help", "文字help", "备用help"])
async def bangzhu_help_text(bot, ev):
    await bot.send(ev, TOP_MANUAL_0)
    await bot.send(ev, TOP_MANUAL_TEXT)
    await bot.send(ev, f'当前版本{config.VERSION}')
