import asyncio
import hoshino
from hoshino import Service, priv, R, config
from . import main
from . import get

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv_help = '''
- [选图 猫猫] 选择生成表情包所用的底图
- [选图列表] 查看能选择的底图列表,<>内的数字为必选数字
- [HelloWorld.jpg] 将.jpg前的文字作为内容来生成表情包
'''.strip()

sv = Service(
    name = '选图生成',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助选图生成"])
async def bangzhu_image_generate(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


@sv.on_prefix(('选图','imgsw','IMGSW'))
async def switch_img(bot, ev):
    uid = ev.user_id
    msg = str(ev.message).strip()
    mark = await get.setQqName(uid,msg)
    if mark != None:
            img = R.img(f'image-generate/image_data/{mark}/{mark}.jpg').cqcode
            await bot.send(ev,f'表情已更换为{msg}\n{img}', at_sender=True)

@sv.on_suffix(('.jpg','.JPG'))
@sv.on_prefix(('生成表情包','imgen','IMGEN'))
async def generate_img(bot, ev):
    msg = ev.message.extract_plain_text()
    uid = ev.user_id
    await main.img(bot, ev, msg, uid)
    

image_list = '''
狗妈<1~3>
熊猫<1~3>
马自立<1~2>
粽子<1~2>
吹雪<1~2>
心心
阿夸
臭鼬
好学
黑手
逗乐了
奥利给
kora
珂学家
财布
守夜冠军
恶臭
我爱你
peko
星姐
爱丽丝
猫猫
猪
猫猫猫
gvc
猫
ksm
栞栞
'''.strip()

@sv.on_fullmatch(('选图列表','imgswl','IMGSWL'))
async def switch_list(bot, ev):
    if forward_msg_exchange == 1:
        msg = image_list
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
            recall_1 = await bot.send(ev, image_list)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall_1['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send(ev, image_list)
