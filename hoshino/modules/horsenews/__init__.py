import os
import hoshino
from hoshino import Service, R, priv
from hoshino.typing import *
from hoshino.util import FreqLimiter, concat_pic, pic2b64, silence
from .news_spider import *

sv_help = '''
=====功能=====
- [马娘新闻] 查看最近五条新闻
（自动推送） 该功能没有命令
'''.strip()

sv = Service(
    name = '马娘新闻_查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = False, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

svuma = Service(
    name = '马娘新闻_推送',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = False, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助马娘新闻"])
async def bangzhu_horsenews(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

# 主动获取新闻功能
@sv.on_fullmatch(('马娘新闻', '赛马娘新闻'))
async def uma_news(bot, ev):
    await bot.send(ev, get_news())

# 马娘新闻播报
@svuma.scheduled_job('cron', minute='*/5')
async def uma_news_poller():
    if (judge() == True):
        svuma.logger.info('检测到马娘新闻更新！')
        await svuma.broadcast(news_broadcast(), 'umamusume-news-poller', 0.2)
    else:
        svuma.logger.info('暂未检测到马娘新闻更新')
        return
