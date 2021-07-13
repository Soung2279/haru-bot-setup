import requests
import re
import html2text
from hoshino import Service, R, priv
from aiocqhttp.message import MessageSegment

sv_help = '''
将bilibili小程序转换为单条信息
(在有多个bot的群聊中，此功能可能导致死循环！)
'''.strip()

sv = Service(
    name = '反小程序',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助反小程序"])
async def bangzhu_pulipuli(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

def humanNum(num):
    if num < 10000:
        return num
    else:
        a = int(num)/10000
        b = re.findall(r"\d{1,}?\.\d{1}", str(a))
        return f'{b[0]}万'


def getVideoInfo(param_aid, param_bvid):
    url = f'https://api.bilibili.com/x/web-interface/view?aid={param_aid}&bvid={param_bvid}'
    try:
        with requests.get(url, timeout=20) as resp:
            res = resp.json()
            data = res['data']
            bvid = data['bvid']
            aid = data['aid']
            pic = data['pic']
            title = data['title']
            name = data['owner']['name']
            view = data['stat']['view']
            danmaku = data['stat']['danmaku']
            play = humanNum(view)
            danku = humanNum(danmaku)
            cover = MessageSegment.image(pic)
            result = f'{cover}\nav{aid}\n{title}\nUP:{name}\n{play}播放 {danku}弹幕\nhttps://www.bilibili.com/video/{bvid}'.strip()
            return result
    except Exception as ex:
        sv.logger.error(f'[getVideoInfo ERROR]:{ex}')
        return None


def getSearchVideoInfo(keyword):
    url = f'https://api.bilibili.com/x/web-interface/search/all/v2?{keyword}'
    try:
        with requests.get(url, timeout=20) as resp:
            res = resp.json()
            data = res['data']['result']
            videos = [x for x in data if x['result_type'] == 'video']
            if (len(videos) == 0):
                return None
            video = videos[0]['data'][0]
            aid = video['aid']
            bvid = video['bvid']
            pic = video['pic']
            play = humanNum(video['play'])
            danku = humanNum(video['video_view'])
            title = html2text.html2text(video['title'])
            cover = MessageSegment.image(f'http://{pic}')
            author = video['author']
            result = f'{cover}\n（搜索）av{aid}\n{title}\nUP:{author}\n{play}播放 {danku}弹幕\nhttps://www.bilibili.com/video/{bvid}'.strip()
            return result
    except Exception as ex:
        sv.logger.error(f'[getSearchVideoInfo ERROR]:{ex}')
        return None


def getAvBvFromNormalLink(link):
    if isinstance(link, str) is False:
        return None
    search = re.findall(
        r'bilibili\.com\/video\/(?:[Aa][Vv]([0-9]+)|([Bb][Vv][0-9a-zA-Z]+))', link)
    if len(search) <= 0:
        return search
    result = {'aid': search[0][0], 'bvid': search[0][1]}
    return result


def getAvBvFromShortLink(link):
    try:
        with requests.head(link, timeout=20) as resp:
            status = resp.status_code
            if(status >= 200 and status < 400):
                location = resp.headers['location']
                normal_link = getAvBvFromNormalLink(location)
                return normal_link
            else:
                sv.logger.error('request bilibili short link fail')
                return None
    except Exception as ex:
        sv.logger.error(f'[getAvBvFromShortLink ERROR]:{ex}')


def getAvBvFromMsg(msg):
    search = getAvBvFromNormalLink(msg)
    if len(search) > 0:
        return search
    search = re.findall(r'b23\.tv\/[a-zA-Z0-9]+', msg)
    if len(search) > 0:
        return getAvBvFromShortLink(f'http://{search[0]}')
    return None


def unescape(param):
    a = param.replace('#44;', ',')
    b = re.sub(r'&#91;', '[', a)
    c = re.sub(r'&#93;', ']', b)
    d = c.replace('\\/', '/')
    result = re.sub(r'&amp;', '&', d)
    return result


def match_msg(keyword, msg):
    return keyword in msg


@sv.on_message('group')
async def pulipuli(bot, event):
    gid = event.group_id
    msg = str(event.message)
    msg = unescape(msg)
    title = None
    is_match = re.findall(r'\[CQ:rich,.*\]?\S*', msg)
    keyword1 = '&#91;QQ小程序&#93;哔哩哔哩'
    keyword2 = '[[QQ小程序]哔哩哔哩]'
    if len(is_match) > 0:
        sv.logger.info('[pulipuli INFO] is_match is True')
        if match_msg(keyword1, msg) == True or match_msg(keyword2, msg) == True:
            sv.logger.info('[pulipuli INFO] fuck mini program')
            await bot.send(event, R.img('fuckapp.png').cqcode)
            search = re.findall(r'"desc":"(.+?)"', msg)
            if len(search) > 0:
                title = re.sub(r'/\\"/g', '"', search[1])
    param = getAvBvFromMsg(msg)
    if param is None:
        pass
    elif len(param) > 0:
        reply = getVideoInfo(param['aid'], param['bvid'])
        if reply is not None:
            await bot.send(event, reply)
            return
    isBangumi = re.search(
        r'bilibili\.com\/bangumi|(b23|acg)\.tv\/(ep|ss)', msg)
    if isinstance(title, str) and isBangumi:
        reply = getSearchVideoInfo(title)
        if reply is not None:
            await bot.send(event, reply)
            return
