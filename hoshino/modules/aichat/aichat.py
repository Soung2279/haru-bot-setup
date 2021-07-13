import hoshino
import aiohttp
from nonebot import MessageSegment
import os
import asyncio
import time
import json
import traceback
import nonebot
import random
import threading 
import re
import string
from hashlib import md5
from time import time
from urllib.parse import quote_plus

from nonebot import get_bot
from nonebot.helpers import render_expression
from hoshino import Service, priv, config
try:
    import ujson as json
except ImportError:
    import json

# 【Error】腾讯智能对话的旧API已弃用，新API与本功能不兼容，请尽快停用。

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
app_id = config.aichat_api_ID
app_key = config.aichat_api_KEY

sv_help = '''
【此功能已弃用】
- [@bot XX] @bot与bot对话。ai将概率回复。
'''.strip()

sv = Service(
    name = '智能闲聊',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = False, #是否可见服务名
    enable_on_default = False, #是否默认启用
    bundle = 'advance', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["智能闲聊帮助", "aichat帮助"])
async def bangzhu_aichat(bot, ev):
    await bot.send(ev, sv_help)

bot = get_bot()
cq_code_pattern = re.compile(r'\[CQ:\w+,.+\]')
salt = None

# 定义无法获取回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～',
    '唔……等会再告诉你',
    '意味わからん~'
)

def getReqSign(params: dict) -> str:
    hashed_str = ''
    for key in sorted(params):
        hashed_str += key + '=' + quote_plus(params[key]) + '&'
    hashed_str += 'app_key='+app_key
    sign = md5(hashed_str.encode())
    return sign.hexdigest().upper()


def rand_string(n=8):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(n))

@sv.on_message('group')
async def ai_reply(bot, context):
    msg = str(context['message'])
    
    if not msg.startswith(f'[CQ:at,qq={context["self_id"]}]'):
        return

    text = re.sub(cq_code_pattern, '', msg).strip()
    if text == '':
        return

    global salt
    if salt is None:
        salt = rand_string()
    session_id = md5((str(context['user_id'])+salt).encode()).hexdigest()

    param = {
        'app_id': app_id,
        'session': session_id,
        'question': text,
        'time_stamp': str(int(time())),
        'nonce_str': rand_string(),
    }
    sign = getReqSign(param)
    param['sign'] = sign

    async with aiohttp.request(
        'POST',
        'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat',
        params=param,
    ) as response:
        code = response.status
        if code != 200:
            raise ValueError(f'bad server http code: {code}')
        res = await response.read()
        #print (res)
    param = json.loads(res)
    if param['ret'] != 0:
        raise ValueError(param['msg'])
    reply = param['data']['answer']
    if reply:
        await bot.send(context, reply,at_sender=False) 
    else:
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        await bot.send(render_expression(EXPR_DONT_UNDERSTAND))