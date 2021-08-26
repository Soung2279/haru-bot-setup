from PIL import Image

from hoshino import Service, priv, logger, aiorequests
from hoshino.typing import CQEvent, MessageSegment
from hoshino.util import FreqLimiter, DailyNumberLimiter, pic2b64

from .generator import genImage

lmt = DailyNumberLimiter(10)

sv_help = '''
- [5000兆元] (上半句)|(下半句)生成图片
'''.strip()

sv = Service(
    name = '5000choyen',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助5000choyen", "帮助红白字"])
async def bangzhu_choyen(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

@sv.on_prefix(('5000兆元','5000兆円','5kcy','红白字'))
async def gen_5000_pic(bot, ev: CQEvent):
    uid = ev.user_id
    gid = ev.group_id
    mid= ev.message_id
    if not lmt.check(uid):
        await bot.send(ev, f'您今天已经使用过10次生成器了，休息一下明天再来吧~', at_sender=True)
        return
    try:
        keyword = ev.message.extract_plain_text().strip()
        if not keyword:
            await bot.send(ev, '请提供要生成的句子！')
            return
        if '｜' in keyword:
            keyword=keyword.replace('｜','|')
        upper=keyword.split("|")[0]
        downer=keyword.split("|")[1]
        img=genImage(word_a=upper, word_b=downer)
        img = str(MessageSegment.image(pic2b64(img)))
        await bot.send(ev, img)
        lmt.increase(uid)
    except OSError:
        await bot.send(ev, '生成失败……请检查字体文件设置是否正确')
    except:
        await bot.send(ev, '生成失败……请检查命令格式是否正确')
