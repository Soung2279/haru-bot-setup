import hoshino
import nonebot
from nonebot import scheduler
from nonebot import on_command, CommandSession
from hoshino import log, priv, Service, util
from hoshino.typing import CQEvent
from .data_source import Check

from datetime import datetime

MAX_PERFORMANCE_PERCENT = hoshino.config.check.MAX_PERFORMANCE_PERCENT
PROCESS_NAME_LIST = hoshino.config.check.PROCESS_NAME_LIST

logger = log.new_logger('check')
check = Check(hoshino.config.check.PROCESS_NAME_LIST)

sv = Service('server_check', use_priv=priv.ADMIN, manage_priv=priv.SUPERUSER, visible=False, enable_on_default=True) 
#【notice】维护人员才用得到的功能，不对用户开放。故没有指令文档。
@sv.on_command('check', aliases=('运行检查', '后端检查', '服务器检查', '检查服务器'), only_to_me=True)
async def music_recommend(session: CommandSession):
    check_report_admin = await check.get_check_info()
    if check_report_admin:
        await session.send(check_report_admin)
    else:
        logger.error("Not found Check Report")
        await session.send("[ERROR]Not found Check Report")

#定时向超级管理员[SUPERUSER]私聊发送服务器状态
#9：00，12：00，18：00，23：00
@scheduler.scheduled_job('cron', hour='9', minute='00') 
async def check_task():
    bot = nonebot.get_bot()
    weihu = hoshino.config.SUPERUSERS[0]
    result = await check.get_check_easy()        
    await bot.send_private_msg(user_id=weihu, message=result)

@scheduler.scheduled_job('cron', hour='12', minute='00') 
async def check_task():
    bot = nonebot.get_bot()
    weihu = hoshino.config.SUPERUSERS[0]
    result = await check.get_check_easy()        
    await bot.send_private_msg(user_id=weihu, message=result)

@scheduler.scheduled_job('cron', hour='18', minute='00') 
async def check_task():
    bot = nonebot.get_bot()
    weihu = hoshino.config.SUPERUSERS[0]
    result = await check.get_check_easy()        
    await bot.send_private_msg(user_id=weihu, message=result)

@scheduler.scheduled_job('cron', hour='23', minute='00') 
async def check_task():
    bot = nonebot.get_bot()
    weihu = hoshino.config.SUPERUSERS[0]
    result = await check.get_check_easy()        
    await bot.send_private_msg(user_id=weihu, message=result)


@sv.on_fullmatch(["服务器状态", "bot状态"], only_to_me=True)
async def info_check(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        util.log(f'{ev.user_id}尝试查看服务器状态, 已拒绝')
        await bot.send(ev, f"权限不足。", at_sender=True)
        return
    else:
        result = await check.get_check_easy()
        await bot.send(ev, result)

