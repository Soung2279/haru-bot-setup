import asyncio

import hoshino
from hoshino.service import sucmd
from hoshino.typing import CommandSession, CQHttpError
from hoshino.service import Service

lock = asyncio.Lock()
broadcast_record = []

#格式：[bc|广播] [服务名|g-群号/群号/群号] 广播内容
@sucmd('broadcast', aliases=('bc', '广播'))
async def broadcast(session: CommandSession):
    msg = session.current_arg
    if not ' ' in msg:
        await session.send(f'请输入服务名，全群广播则输入all，分群广播请以"g-"开头后接QQ群号，并以逗号相隔')
        return
    args = msg.split(' ',1)
    bc_sv_name =  args[0]
    bc_msg = args[1]
    svs = Service.get_loaded_services()
    if bc_sv_name not in svs and bc_sv_name != 'all' and not bc_sv_name.startswith('g-'):
        await session.send(f'未找到该服务，请输入正确的服务')
        return
    sid = list(hoshino.get_self_ids())[0]
    if bc_sv_name == 'all':
        gl = await session.bot.get_group_list(self_id=sid)
        gl = [ g['group_id'] for g in gl ]
    elif bc_sv_name.startswith('g-'):
        bc_l = bc_sv_name.replace('g-', '')
        gl = bc_l.split(r'/')
    else:
        enable_groups = await svs[bc_sv_name].get_enable_groups()
        gl = enable_groups.keys()
    for sid in hoshino.get_self_ids():
        for g in gl:
            await asyncio.sleep(0.5)
            try:
                msg_obj = await session.bot.send_group_msg(self_id=sid, group_id=g, message=bc_msg)
                with await lock:
                    broadcast_record.append(msg_obj['message_id'])
                hoshino.logger.info(f'群{g} 投递广播成功')
            except Exception as e:
                hoshino.logger.error(f'群{g} 投递广播失败：{type(e)}')
                try:
                    await session.send(f'群{g} 投递广播失败：{type(e)}')
                except Exception as e:
                    hoshino.logger.critical(f'向广播发起者进行错误回报时发生错误：{type(e)}')
    await session.send(f'广播完成！')
    await asyncio.sleep(120)
    with await lock:
        broadcast_record.clear()

@sucmd('broadcast_list', aliases=('bc_list', '群列表'))
async def broadcast_list(session: CommandSession):
    sid = list(hoshino.get_self_ids())[0]
    gl = await session.bot.get_group_list(self_id=sid)
    msg = '已加入的群聊和对应群号：'
    for g in gl:
        group_name = g['group_name']
        group_id = g['group_id']
        msg = msg + f'\n{group_name}: {group_id}'
    await session.send(msg)

@sucmd('broadcast_recall', aliases=('bc_recall', '广播撤回'))
async def broadcast_recall(session: CommandSession):
    with await lock:
        if len(broadcast_record) == 0:
            await session.send(f'无可以撤回的广播')
            return
        for msg_id in broadcast_record:
            try:
                await session.bot.delete_msg(message_id=msg_id)
            except Exception as e:
                hoshino.logger.error(f'消息{msg_id} 撤回失败：{type(e)}')
                try:
                    await session.send(f'消息{msg_id} 撤回失败：{type(e)}')
                except Exception as e:
                    hoshino.logger.critical(f'向广播发起者进行错误回报时发生错误：{type(e)}')
        broadcast_record.clear()
    await session.send(f'广播撤回完成！')
