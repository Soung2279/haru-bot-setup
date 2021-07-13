import requests
import html2text
import re
from hoshino import Service, R
from hoshino.util import FreqLimiter
from aiocqhttp.message import MessageSegment


sv = Service('pulipuli-query', enable_on_default=True)
_freq_limiter = FreqLimiter(5)


def humanNum(num):
    if num < 10000:
        return num
    else:
        a = int(num)/10000
        b = re.findall(r"\d{1,}?\.\d{1}", str(a))
        return f'{b[0]}万'


def getSearchVideoInfo(keyword):
    url = f'https://api.bilibili.com/x/web-interface/search/all/v2?keyword={keyword}'
    try:
        with requests.get(url, timeout=20) as resp:
            res = resp.json()
            data = res['data']['result']
            videos = [x for x in data if x['result_type'] == 'video']
            if len(videos) == 0:
                return ''
            video_list = videos[0]['data']
            if len(video_list) > 10:
                video_list = video_list[0:10]
            result = ''
            for item in video_list:
                aid = item['aid']
                bvid = item['bvid']
                pic = item['pic']
                desc = html2text.html2text(item['description'])
                play = humanNum(item['play'])
                danku = humanNum(item['video_review'])
                title = html2text.html2text(item['title'])
                title = title.strip()
                cover = MessageSegment.image(f'https:{pic}')
                author = item['author']
                result += f'''{cover}
{title}
{desc}
av{aid}
UP：{author}
{play}播放  {danku}弹幕
源地址：https://www.bilibili.com/video/{bvid}
===========>
                '''.strip()
            result += '\n搜索结束，冷却时间120秒'
            return result
    except Exception as ex:
        sv.logger.error(f'[getSearchVideoInfo ERROR]:{ex}')
        return f'搜索{keyword}出错，请稍后再试~'


@sv.on_prefix('搜索')
async def pulipuli_query(bot, event):
    msg = event.message.extract_plain_text().strip()
    uid = event.user_id
    if not msg:
        await bot.send(event, '没有找到关键词...')
        return
    if not _freq_limiter.check(uid):
        await bot.send(event, '查询时间冷却中...')
        return
    await bot.send(event, f'正在搜索{msg}，请稍等...')
    reply = getSearchVideoInfo(msg)
    if reply == '':
        reply = f'没有找到包含关键词{msg}的相关视频~'
    await bot.send(event, reply)
    if reply != '':
        _freq_limiter.start_cd(uid, 120)
