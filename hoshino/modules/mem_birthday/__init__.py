import os
import asyncio
import hoshino
from hoshino import Service, priv
from .create_config import *
from .comp_birth import *
from .update_age import *

sv_help = '''
每天早上8点自动推送群内生日祝福
- [群员生日初始化] (bot主人用)初始化生日信息
'''.strip()

sv = Service(
    name = '群友生日提醒',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助群友生日提醒", "帮助mem_birthday"])
async def bangzhu_mem_birthday(bot, ev):
    await bot.send(ev, sv_help)

# 正常来说只要初始化一次就够了
@sv.on_fullmatch(["群员生日初始化", "群友生日初始化"])
async def init_birth(bot, ev):
    now = datetime.now()  #获取当前时间
    hour = now.hour  #获取当前时间小时数
    minute = now.minute  #获取当前时间分钟数
    hour_str = f' {hour}' if hour<10 else str(hour)
    minute_str = f' {minute}' if minute<10 else str(minute)
    if not priv.check_priv(ev, priv.SUPERUSER):
        sv.logger.warning(f"非管理者：{ev.user_id}尝试于{hour_str}点{minute_str}分手动更新假期数据")
        await bot.send(ev, "只有bot主人才能使用此命令哦~")
        return
    # 首次启动时，若没有`config.yml`则创建配置文件
    _current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    if not os.path.exists(_current_dir):
        _bot = hoshino.get_bot()
        msg = '所有群的群成员信息正在初始化中，请耐心等待...\n（初始化时间受群数量和人数影响，总共两三百人大概要1分钟或者更久）'
        await bot.send(ev, msg)
        await create_yml(_bot, _current_dir)
        msg = '初始化成功，您可前往bot插件目录查看 `config.yml` 内容是否有误'  #数据结构非常简单，user_id是QQ号，yes_age是昨天的年龄，tod_age是今天的年龄
        await bot.send(ev, msg)
    else:
        msg = '初始化失败，文件已存在不可再初始化！'  #为防止误触，不提供群内删除文件的命令，若想重新初始化，请手动到本文件目录删除`config.yml`
        await bot.send(ev, msg)

# 推送生日祝福
@sv.scheduled_job('cron', hour='8', minute='00') # 早上8点推送祝福，让你在赶着上班上学的同时得到一丝温馨感（
async def auto_compare():
    bot = hoshino.get_bot()
    glist_info = await bot.get_group_list()
    for each_g in glist_info:
        gid = each_g['group_id']
        bir_list = judge_bir(gid)
        if bir_list:
            sv.logger.info(f'检测到今天群{gid}里有{len(bir_list)}个B生日！')
            msg = get_bir_info(bir_list)
            await bot.send_group_msg(group_id=gid, message=msg)
        else:
            sv.logger.info(f'今天群{gid}里没有群友生日欸~')
            return

# 更新每天的年龄，运行起来也要挺久的时间
@sv.scheduled_job('cron', hour='2', minute='00') # 凌晨两点更新数据
async def auto_update():
    bot = hoshino.get_bot()
    sv.logger.info('正在更新群友信息...预计用时几分钟')
    glist_info = await bot.get_group_list()
    for each_g in glist_info:
        gid = each_g['group_id']
        await repalce_age(bot, gid)
    sv.logger.info('所有群友年龄信息更新完成')
