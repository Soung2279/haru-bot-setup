import os
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import aiohttp
import asyncio
import math

# type 0 普通常驻任务深渊 1 新闻 2 蛋池 3 限时活动H5

event_data = {
    'cn': [],
}

event_updated = {
    'cn': '',
}

lock = {
    'cn': asyncio.Lock(),
}

ignored_key_words = [
    "封号",
    "修复",
    "爱酱&帮助",
    "公平运营",
    "防沉迷",
    "客服",
    "隐私",
    "米游社",
    "攻略",
    "社区"
]

ignored_ann_ids = [

]


async def query_data(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()
    except:
        pass
    return None


async def load_event_cn():
    result = await query_data('https://api-takumi.mihoyo.com/common/bh3_cn/announcement/api/getAnnList?game=bh3&game_biz=bh3_cn&lang=zh-cn&bundle_id=bh3_cn&platform=pc&region=ios01&level=1&channel_id=1&uid=51000000')
    if result and 'retcode' in result and result['retcode'] == 0:
        event_data['cn'] = []
        datalist = result['data']['list']
        for data in datalist:
            for item in data['list']:
                # 20 活动公告 21 游戏公告
                if item['type'] != 20:
                    ignore = False
                    for ann_id in ignored_ann_ids:
                        if ann_id == item["ann_id"]:
                            ignore = True
                            break
                    if ignore:
                        continue

                    for keyword in ignored_key_words:
                        if keyword in item['title']:
                            ignore = True
                            break
                    if ignore:
                        continue

                start_time = datetime.strptime(
                    item['start_time'], r"%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(
                    item['end_time'], r"%Y-%m-%d %H:%M:%S")
                event = {'title': item['title'],
                         'start': start_time,
                         'end': end_time,
                         'forever': False,
                         'type': 0}
                if item['type'] == 20:
                    event['type'] = 1
                    if '补给' in item['title'] or '精准' in item['title']:
                        event['type'] = 2
                event_data['cn'].append(event)
        return 0
    return 1


async def load_event(server):
    if server == 'cn':
        return await load_event_cn()
    return 1


def get_pcr_now(offset):
    pcr_now = datetime.now()
    if pcr_now.hour < 4:
        pcr_now -= timedelta(days=1)
    pcr_now = pcr_now.replace(
        hour=18, minute=0, second=0, microsecond=0)  # 用晚6点做基准
    pcr_now = pcr_now + timedelta(days=offset)
    return pcr_now


async def get_events(server, offset, days):
    events = []
    pcr_now = datetime.now()
    if pcr_now.hour < 4:
        pcr_now -= timedelta(days=1)
    pcr_now = pcr_now.replace(
        hour=18, minute=0, second=0, microsecond=0)  # 用晚6点做基准

    await lock[server].acquire()
    try:
        t = pcr_now.strftime('%y%m%d')
        if event_updated[server] != t:
            if await load_event(server) == 0:
                event_updated[server] = t
    finally:
        lock[server].release()

    start = pcr_now + timedelta(days=offset)
    end = start + timedelta(days=days)
    end -= timedelta(hours=18)  # 晚上12点结束

    for event in event_data[server]:
        if end > event['start'] and start < event['end']:  # 在指定时间段内 已开始 且 未结束
            event['start_days'] = math.ceil(
                (event['start'] - start) / timedelta(days=1))  # 还有几天开始
            event['left_days'] = math.floor(
                (event['end'] - start) / timedelta(days=1))  # 还有几天结束
            events.append(event)
    # 按type从大到小 按剩余天数从小到大
    events.sort(key=lambda item: item["type"]
                * 100 - item['left_days'], reverse=True)
    return events


if __name__ == '__main__':
    async def main():
        await load_event_cn()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
