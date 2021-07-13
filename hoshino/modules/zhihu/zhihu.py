import aiohttp
import asyncio
import hoshino
from hoshino.typing import *
from hoshino import Service, priv, config

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

sv_help = '''
- [知乎日报] 查看今日知乎日报。
'''.strip()

sv = Service(
    name = '知乎日报',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助知乎日报"])
async def bangzhu_zhihu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

@sv.on_fullmatch(['知乎日报'])
async def news(bot, ev):
    STORY_URL_FORMAT = 'https://daily.zhihu.com/story/{}'
    async with aiohttp.request('GET', 'https://news-at.zhihu.com/api/4/news/latest', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}) as resp:
        data = await resp.json()
        stories = data.get('stories')
        if not stories:
            await bot.send(ev, '暂时没有数据，或者服务无法访问')
            return
        reply = ''
        for story in stories:
            url = STORY_URL_FORMAT.format(story['id'])
            title = story.get('title', '未知内容')
            reply += f'\n{title}\n{url}\n'
            if forward_msg_exchange == 1:
                msg = reply.strip()
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
                    recall = await bot.send(ev, reply.strip())
                    notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")
                
                    await asyncio.sleep(RECALL_MSG_TIME)

                    await bot.delete_msg(message_id=recall['message_id'])
                    await bot.delete_msg(message_id=notice['message_id'])
                else:
                    await bot.send(ev, reply.strip())