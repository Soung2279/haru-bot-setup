from nonebot import *
import requests,random,os
import hoshino
from hoshino import R, Service, priv, util
from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter


bot=get_bot()

sv_help = '''
- [网抑云]
- [到点了]
- [上号]
'''.strip()

sv = Service(
    name = '网抑云时间',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

_time_limit = 3
_lmt = FreqLimiter(_time_limit)

def pic_gender_cqcode(dic_name):
    '''
    获得/res/img/dic_name目录下一张随机图片，返回cqcode
    '''
    pic_dir = R.img(dic_name).path
    
    file_list:list = os.listdir(pic_dir)
    img_random = random.choice(file_list)
    img_path = dic_name + '/' + img_random
    img_cqcode = R.img(str(img_path)).cqcode
    return img_cqcode

@sv.on_keyword(('上号','生而为人','生不出人','网抑云','已黑化','到点了'))
async def net_ease_cloud_word(bot,ev:CQEvent):
    gid = ev.group_id
    if random.random()<0.90:
        if not _lmt.check(gid):
            await bot.send(ev, '抑郁太多对身体不好,请等待一会儿哦', at_sender=True)
            return
        _lmt.start_cd(gid)
        try:
            pics = pic_gender_cqcode('wcloud/success')
        except Exception as e:
            hoshino.logger.error(f'获取目录res/img/wcloud/success下的图片时发生错误{type(e)}, 请检查')
        await bot.send(ev, pics)
    else:
        await bot.send(ev, R.img(f"wcloud/failed/nowc{random.randint(1, 7)}.jpg").cqcode)
        await bot.send(ev, f'上号失败，不准抑郁')

    