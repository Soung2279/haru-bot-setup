import os
import random

from nonebot.exceptions import CQHttpError
from nonebot import MessageSegment

from hoshino import R, Service, priv



sv_help = '''
- [xcw骂我]
'''.strip()

sv = Service(
    name = 'xcw骂我',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助xcw骂我"])
async def bangzhu_xcw(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


'''-----随机发送文件夹内容①----------'''
xcw_folder_mawo = R.get('record/mawo/').path

'''-----随机发送文件夹内容②----------'''
def get_xcw_mawo():  #get
    files = os.listdir(xcw_folder_mawo)  #folder
    filename = random.choice(files)
    rec = R.get('record/mawo/', filename)  #folder
    return rec


######开始发送
'''xxxxxxx语音xxxxxxxxx'''
@sv.on_fullmatch(['xcw骂我'])
async def xcw_mawo(bot, ev) -> MessageSegment:
    # conditions all ok, send a xcw.
    file = get_xcw_mawo()
    try:
        rec = MessageSegment.record(f'file:///{os.path.abspath(file.path)}')
        await bot.send(ev, rec)
    except CQHttpError:
        sv.logger.error("发送失败")