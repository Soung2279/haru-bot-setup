import requests, random, os, json
from hoshino import Service, R, aiorequests, priv
from hoshino.typing import CQEvent, Message
from hoshino.util import FreqLimiter, DailyNumberLimiter
import hoshino

_nlmt = DailyNumberLimiter(2)  #上限次数
_cd = 10  #调用间隔冷却时间(s)
_flmt = FreqLimiter(_cd)

sv_help = '''
- [发病 对象] 对发病对象发病
- [小作文] 随机发送一篇发病小作文
- [病情加重 对象/小作文] 将一篇发病小作文添加到数据库中（必须带“/”）
- [病情查重 小作文] 对一篇小作文进行查重
- [<回复一个小作文> 病情查重] 同上
'''.strip()

sv = Service(
    name = 'as发病小作文',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )
    
@sv.on_fullmatch(["帮助as发病小作文", "帮助cp"])
async def bangzhu_asill(bot, ev):
    await bot.send(ev, sv_help)

def get_data():
    _path = os.path.join(os.path.dirname(__file__), 'data.json')
    if os.path.exists(_path):
        with open(_path,"r",encoding='utf-8') as df:
            try:
                words = json.load(df)
            except Exception as e:
                hoshino.logger.error(f'读取发病小作文时发生错误{type(e)}')
                return None
    else:
        hoshino.logger.error(f'目录下未找到发病小作文')
    return random.choice(words)

@sv.on_fullmatch(('asill帮助','发病帮助','小作文帮助','帮助发病','小作文发病'))
async def asill_help(bot, ev: CQEvent):
        await bot.send(ev, f"{sv.help}")

@sv.on_fullmatch('小作文')
async def xzw(bot,ev:CQEvent):
    gid = ev.group_id
    illness = get_data()
    uid = ev['user_id']
    if not uid in hoshino.config.SUPERUSERS:
        if not _flmt.check(uid):
            await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
            return
        if not _nlmt.check(uid):
            await bot.send(ev, f"避免重复使用导致刷屏，此消息已忽略")
            return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    await bot.send(ev, illness["text"])

@sv.on_prefix('发病')
async def fb(bot, ev: CQEvent):
    aim = str(ev.message).strip()
    uid = ev['user_id']
    if not uid in hoshino.config.SUPERUSERS:
        if not _flmt.check(uid):
            await bot.send(ev, f"┭┮﹏┭┮呜哇~频繁使用的话bot会宕机的...再等{_cd}秒吧", at_sender=True)
            return
        if not _nlmt.check(uid):
            await bot.send(ev, f"避免重复使用导致刷屏，此消息已忽略")
            return
    if not aim:
        await bot.send(ev, "请发送[发病 对象]~", at_sender=True)
    else:
        illness = get_data()
        text = illness["text"]
        person = illness["person"]
        text = text.replace(person,aim)
        _flmt.start_cd(uid)
        _nlmt.increase(uid)
        await bot.send(ev, text)

@sv.on_prefix('病情加重')
async def bqjz(bot, ev: CQEvent):
    kw = ev.message.extract_plain_text().strip()
    arr = kw.split('/')
    if not arr[0] or not arr[1] or len(arr) > 2:
        await bot.send(ev, "请发送[病情加重 对象/小作文]（必须带“/”）~", at_sender=True)
    else: 
        new_illness = {"person" : arr[0], "text" : arr[1]}
        _path = os.path.join(os.path.dirname(__file__), 'data.json')
        words = None
        if os.path.exists(_path):
            with open(_path,"r",encoding='utf8') as df:
                try:
                    words = json.load(df)
                except Exception as e:
                    hoshino.logger.error(f'读取发病小作文时发生错误{type(e)}')
                    return None
            words.append(new_illness)        
            with open(_path,"w",encoding='utf8') as df:        
                try:
                    json.dump(words,df,indent=4)
                    await bot.send(ev, "病情已添加", at_sender=True)
                except Exception as e:
                    hoshino.logger.error(f'添加发病小作文时发生错误{type(e)}')
                    return None
        else:
            hoshino.logger.error(f'目录下未找到发病小作文')


async def check(bot, ev: CQEvent, text):
    url = 'https://asoulcnki.asia/v1/api/check'
    data = {'text': text}
    try:
        resp = await aiorequests.post(url, json=data)
        resp = await resp.json()
        assert resp['message'] == 'success'
    except Exception as e:
        sv.logger.error(e)
        await bot.finish(ev, '查重失败了...{e}')
    data = resp['data']
    if rate := data['rate']:
        relate = []
        for i in data.get('related', []):
            rrate = i.get('rate', 0)
            rname = i.get('reply', {}).get('m_name', 'unknown')
            url = i.get('reply_url')
            relate.append(f'----\n{url}\n{rrate:.2%} / {rname}')
        relate = '\n'.join(relate)
        msg = f'总文字复制比：{rate:.2%}\n相似小作文：\n{relate}'
    else:
        msg = '没有相似的小作文'
    await bot.send(ev, msg)


@sv.on_prefix('病情查重')
async def chachong(bot, ev: CQEvent):
    kw = ev.message.extract_plain_text().strip()
    await check(bot, ev, kw)
    
@sv.on_message()
async def huifuchachong(bot, ev: CQEvent):
    fseg = ev.message[0]
    if fseg.type == 'reply' and ev.message.extract_plain_text().strip() == '病情查重':
        msg = await bot.get_msg(message_id=fseg.data['id'])
        text = Message(msg['message']).extract_plain_text().strip()
        await check(bot, ev, text)