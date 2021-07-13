import os
import random
from nonebot.exceptions import CQHttpError
from nonebot import MessageSegment
from hoshino import Service, priv


sv_help = '''
- [原神kfc]  发出二次元的声音.avi
'''.strip()

sv = Service(
    name = '异世相遇',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助异世相遇"])
async def bangzhu_kfc(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

def get_kfc():
    files = os.listdir(os.path.dirname(__file__) + '/record')
    rec = random.choice(files)
    return rec


@sv.on_fullmatch(('原神KFC', '原神kfc', '二次元KFC', '二次元kfc', '异世相遇尽享美味', '异世相遇'))
async def kfc(bot, ev) -> MessageSegment:
    try:
        rec = MessageSegment.record(f'file:///{os.path.dirname(__file__)}/record/{get_kfc()}')
        await bot.send(ev, rec)
    except CQHttpError:
        sv.logger.error("发送失败")
