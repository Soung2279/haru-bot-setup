import hoshino
import asyncio
import os,base64
import shutil
import requests as req
from PIL import Image
from io import BytesIO
from hoshino import Service, R, priv, config
from .get_zhoubao_info import *
from .get_xur_info import *
from .get_chall_info import *
from .get_zhu_info import *


if os.path.exists(R.img('destiny2').path):
    shutil.rmtree(R.img('destiny2').path)  #删除目录，包括目录下的所有文件
    os.mkdir(R.img('destiny2').path)
else:
    os.mkdir(R.img('destiny2').path)

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv_help = '''
- [周报] 查看命运2周报
- [老九] 查看老九位置和装备
- [试炼] 查看试炼周报
- [蛛王] 查看蛛王商店
- [光尘] 查看光尘商店
- [百科] 小黑盒百科链接
'''.strip()

sv = Service(
    name = '命运2查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助命运2查询", "destiny2帮助", "帮助destiny2"])
async def bangzhu_destiny2(bot, ev):
    if forward_msg_exchange == 1:
        await bot.send(ev, sv_help, at_sender=True)
        msg = sv_help
        data = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": msg
            }
        }
        if recall_msg_set == 1:
            recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")
                
            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)        
    else:
        if recall_msg_set == 1:
            recall_1 = await bot.send(ev, sv_help)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall_1['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:               
            await bot.send(ev, sv_help)

#周报功能
@sv.on_fullmatch(('周报','命运2周报'))
async def zhoubao(bot, ev):
    bot = hoshino.get_bot()
    response = req.get(getzhoubaoImg(sethtml1()))
    ls_f = base64.b64encode(BytesIO(response.content).read())
    imgdata = base64.b64decode(ls_f)
    save_dir = R.img('destiny2').path
    path_dir = os.path.join(save_dir,'zhoubao.jpg')
    file = open(path_dir,'wb')
    # 以base64的形式写入文件，用于下载图片
    file.write(imgdata)
    file.close()
    # 先用下面这个形式写，万一以后要加新功能呢
    pzhoubao = ' '.join(map(str, [
        R.img(f'destiny2/zhoubao.jpg').cqcode,
    ]))
    msg = f'命运2 周报：\n图片作者：seanalpha\n{pzhoubao}'
    await bot.send(ev, msg)

#老九功能
@sv.on_fullmatch(('老九','仄','九','xur','老仄','苏尔'))
async def xur(bot, ev):
    response = req.get(getxurImg(sethtml2()))
    ls_f = base64.b64encode(BytesIO(response.content).read())
    imgdata = base64.b64decode(ls_f)
    save_dir = R.img('destiny2').path
    path_dir = os.path.join(save_dir,'xur.jpg')
    file = open(path_dir,'wb')
    file.write(imgdata)
    file.close()
    pxur = ' '.join(map(str, [
        R.img(f'destiny2/xur.jpg').cqcode,
    ]))
    msg = f'命运2 仄：\n图片作者：seanalpha\n{pxur}'
    await bot.send(ev, msg)

#试炼周报功能
@sv.on_fullmatch(('试炼','奥斯里斯试炼','试炼周报'))
async def chall(bot, ev):
    response = req.get(getchallImg(sethtml3()))
    ls_f = base64.b64encode(BytesIO(response.content).read())
    imgdata = base64.b64decode(ls_f)
    save_dir = R.img('destiny2').path
    path_dir = os.path.join(save_dir,'shilian.jpg')
    file = open(path_dir,'wb')
    file.write(imgdata)
    file.close()
    pshilian = ' '.join(map(str, [
        R.img(f'destiny2/shilian.jpg').cqcode,
    ]))
    msg = f'命运2 试炼周报：\n图片作者：seanalpha\n{pshilian}'
    await bot.send(ev, msg)

#蛛王商店功能
@sv.on_fullmatch(('蛛王','蛛王商店','猪王'))
async def zhu(bot, ev):
    response = req.get(getzhuImg(sethtml4()))
    ls_f = base64.b64encode(BytesIO(response.content).read())
    imgdata = base64.b64decode(ls_f)
    save_dir = R.img('destiny2').path
    path_dir = os.path.join(save_dir,'zhuwang.jpg')
    file = open(path_dir,'wb')
    file.write(imgdata)
    file.close()
    pzhuwang = ' '.join(map(str, [
        R.img(f'destiny2/zhuwang.jpg').cqcode,
    ]))
    msg = f'命运2 蛛王：\n图片来源：小黑盒百科\n注意小黑盒蛛王信息可能更新较慢\n{pzhuwang}'
    await bot.send(ev, msg)

#光尘商店（为了图方便，这里直接放了一张整个赛季的商店图片）
@sv.on_fullmatch(('光尘','光尘商店'))
async def buy(bot, ev):
    response = req.get("https://cdn.jsdelivr.net/gh/azmiao/picture-bed/img/buy-13.jpg")
    ls_f = base64.b64encode(BytesIO(response.content).read())
    imgdata = base64.b64decode(ls_f)
    save_dir = R.img('destiny2').path
    path_dir = os.path.join(save_dir,'guangchen.jpg')
    file = open(path_dir,'wb')
    file.write(imgdata)
    file.close()
    pguangchen = ' '.join(map(str, [
        R.img(f'destiny2/guangchen.jpg').cqcode,
    ]))
    msg = f'命运2 第13赛季光尘商店：\n{pguangchen}'
    await bot.send(ev, msg)

#百科后续打算做成其他形式，但目前直接放了个链接，自己去小黑盒看吧
@sv.on_fullmatch(('百科','命运2百科'))
async def baike(bot, ev):
    msg = '命运2 百科链接\n https://api.xiaoheihe.cn/wiki/get_homepage_info_for_app/?wiki_id=1085660&is_share=1 \n来自: 小黑盒'
    await bot.send(ev, msg)
