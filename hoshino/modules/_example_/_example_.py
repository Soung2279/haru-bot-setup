import re
import asyncio
import hoshino

from hoshino import Service, priv, config, util
from hoshino.typing import CQEvent

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv_help = '''
文本
'''.strip()

sv = Service(
    name = 'name',  #功能名
    use_priv = priv.ADMIN, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'advance', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助name"])
async def bangzhu_name(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

@sv.on_fullmatch(('orderA', 'orderB'), only_to_me=True)
async def function_a(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        util.log(f"{ev.user_id}尝试, 已拒绝")
        await bot.send(ev, f"权限不足。", at_sender=True)
    else:
        if forward_msg_exchange == 1:
            data_all = []
            msg1 = f'text1'
            data1 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": msg1
                }
            }
            msg2 = f'text2'
            data2 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": msg2
                }
            }
            data_all=[data1,data2]
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
                recall_1 = await bot.send(ev, f'text1')
                recall_2 = await bot.send(ev, f'text2')
                notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

                await asyncio.sleep(RECALL_MSG_TIME)

                await bot.delete_msg(message_id=recall_1['message_id'])
                await bot.delete_msg(message_id=recall_2['message_id'])
                await bot.delete_msg(message_id=notice['message_id'])
            else:
                await bot.send(ev, f'text1')
                await bot.send(ev, f'text2')


HELP_DUEL_TEXT = '''
- [贵族签到]
- [免费招募]
- [创建贵族]
- [增加女友上限]
- [查询贵族]
- [贵族舞会/招募女友]
- [声望招募]
- [升级贵族]
- [升级称号]
- [贵族决斗+@qq]
- [接受/拒绝]
- [开枪]
- [支持x号x金币]
- [梭哈支持x号]
- [领金币/查金币]
- [为xxx转账xxx金币]
- [查女友+角色名]
- [确认重开]
- [分手+角色名]
- [开启声望系统]
- [用XXX声望兑换金币]
- [用xxx金币与@qq交易女友+角色名]
- [接受交易/拒绝交易]
- [离婚+角色名]
- [梭哈支持XX号]
- [购买上限]
- [查询庆典（查询本群正在进行的庆典状况）]
- [武器列表]
- [切换武器]
- [自定义武器装弹xx发]
- [查询本群不决斗惩罚]

'''.strip()

HELP_DUEL_TEXT_A = '''
- [初始化本群庆典]
- [重置交易] admin
- [设定群xxx为x号死] superuser
- [为xxx充值xxx金币] owner
- [重置决斗(决斗卡住时)] admin
- [重置金币+qq] owner
- [重置角色+qq] owner
- [开启（关闭）本群金币/签到/梭哈倍率/免费招募/声望招募庆典] owner
- [开启/关闭本群不决斗惩罚] admin
- [发放补偿xxx个金币/声望/公主之心] superuser in group
- [所有群发放补偿xxx个金币/声望/公主之心] superuser
- [真步真步]
- [封停/解封群xxx的xxx号] owner
- [清空群xxx的xxx的认输场次] owner
- [为xxx发放x个（礼物）] owner
- [本群重开] owner
'''.strip()


@sv.on_rex(f'^自定义武器装弹(\d+)发$')
async def weaponchange2(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    match = (ev['match'])
    n = int(match.group(1))
    duel = DuelCounter()
    if n % 2 != 0:
        msg = '子弹数量必须是2的倍数喔！'
        await bot.send(ev, msg, at_sender=True)
        return 
    if n == 0:
        msg = '子弹数不能为0！'
        await bot.send(ev, msg, at_sender=True)
        return 
    if duel_judger.get_on_off_status(ev.group_id):
        msg = '现在正在决斗中哦，无法切换武器。'
        await bot.send(ev, msg, at_sender=True)
        return   
    duel._set_weapon(gid,n)
    msg = f'已启用自定义武器，弹匣量为{n}'
    await bot.send(ev, msg, at_sender=True)