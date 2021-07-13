import re
import json

from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import escape
from hoshino.aiorequests import post

sv_help = '''
[谜语人翻译 XX] XX是你不理解的dx
- [xxx 是什么]
'''.strip()

sv = Service(
    name = '谜语人翻译',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )


@sv.on_fullmatch(["帮助谜语人翻译"])
async def bangzhu_nbnhhsh(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


async def query(text: str) -> str:
    if len(text) > 50:
        return '太、太长了8…'
    if not re.match(r'^[a-zA-Z0-9]+$', text):
        return '只能包含字母'
    rsp = await post(
        'https://lab.magiconch.com/api/nbnhhsh/guess',
        headers={'content-type': 'application/json'},
        data=json.dumps({'text': text}),
    )
    rsp = await rsp.json()
    result = []
    for item in rsp:
        prefix = '[%s]: ' % item.get('name')
        trans = item.get('trans')
        if trans == None:
            inputting = item.get('inputting')
            if inputting == None:
                inputting = []
            inputting = ', '.join(inputting)
            if inputting == '':
                ans = '最佳答案：我不知道'
            else:
                ans = '有可能是：' + inputting
        else:
            ans = ', '.join(trans)
        result.append(prefix + ans)
    return '\n'.join(result)

@sv.on_prefix(['谜语人翻译', '谜语翻译'])
async def guess(bot, ev: CQEvent):
    s = escape(ev.message.extract_plain_text().strip())
    msg = await query(s)
    await bot.send(ev, msg, at_sender=True)

@sv.on_rex(re.compile(r'^\s*(?P<text>[a-zA-Z0-9]+)是(什么|甚么|啥|？|\?)'))
async def guess_re(bot, ev: CQEvent):
    match = ev['match']
    msg = await query(match.group('text'))
    await bot.send(ev, msg, at_sender=True)