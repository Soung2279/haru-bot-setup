import os
from typing import final
import urllib.request
from json import load, dump
import time
import re
from aiohttp.client_exceptions import ServerDisconnectedError
from copy import deepcopy
from asyncio import Lock
from os.path import dirname, join, exists

from hoshino import Service,priv
from urllib.parse import quote
from nonebot import get_bot
from aiohttp import ClientSession
import nest_asyncio
nest_asyncio.apply()

sv_help = '''
300英雄查询
- [绑定角色XXX|大区名]  绑定角色ID和所在大区，角色名和大区用|分开写
- [查询300角色]  查询指定ID是否存在或者绑定在谁那
- [启用/停止自动推送]  开启或关闭出租信息自动推送
- [删除角色绑定]  删除掉自己的角色绑定信息
- [角色绑定状态]  查询自己的角色绑定信息
- [查胜场]  查询自己绑定角色的胜场信息，用@可以查询他人的信息
- [查出租]  查询自己绑定角色的出租信息，用@可以查询他人的信息
'''.strip()

sv = Service(
    name = '300英雄查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )
    
@sv.on_fullmatch(["帮助300英雄查询", "帮助300英雄"])
async def bangzhu_hero300(bot, ev):
    await bot.send(ev, sv_help)
    
curpath = dirname(__file__)
config = join(curpath, 'gid_pool.json')
root = {
    'arena_bind' : {}
}
lck = Lock()
if exists(config):
    with open(config,encoding='UTF-8') as fp:
        root = load(fp)
binds = root['arena_bind']
bot = get_bot()

def save_binds():
    with open(config,'w',encoding='UTF-8') as fp:
        dump(root,fp,indent=4,ensure_ascii=False)

@sv.on_prefix(('绑定角色'))
async def bangqu(bot, ev):
    global binds, lck,cache
    async with lck:
        uid = str(ev['user_id'])
        last = binds[uid] if uid in binds else {}
        get_message=str(ev.message.extract_plain_text().strip())
        try:
            get_name=get_message.split("|")[0]
            get_region=get_message.split("|")[1]
        except IndexError as e:
            await bot.finish(ev,'\n请用|在角色ID后写入大区，例如绑定角色XXX|圣杯战争',at_sender=True)
            return
        binds[uid] = {
            'id': get_name,
            'Region':get_region,
            'uid': uid,
            'gid': str(ev['group_id']),
            'push_on': last.get('push_on',False),
            'state':'off',
            'win':'0'
        }
        save_binds()
    await bot.finish(ev, '\n角色：{}\n大区：{}\n绑定成功！'.format(get_name,get_region), at_sender=True)
    

@sv.on_prefix(('查询300角色'))
async def chajue(bot, ev):
    global binds, lck,cache
    get_name = ev.message.extract_plain_text().strip()
    async with lck:
        bind_cache = {}
        cun=[]
        bind_cache = deepcopy(binds)
        for user in bind_cache:
            info = bind_cache[user]
            if get_name == info['id']:
                cun.append('true')
                get_qq=info['uid']
                get_gid=info['gid']
            else:
                cun.append('false')
        if 'true' in cun:
            await bot.finish(ev, f'\n角色：{get_name}\n已被QQ：{get_qq}于群：{get_gid}里绑定', at_sender=True)
        else:
            await bot.finish(ev, f'\n该角色ID未被任何人绑定', at_sender=True)

@sv.on_rex('(启用|停止)自动推送')
async def change_arena_sub(bot, ev):
    global binds, lck
    key = 'push_on'
    uid = str(ev['user_id'])
    async with lck:
        if not uid in binds:
            await bot.send(ev,'您还未绑定角色',at_sender=True)
        else:
            binds[uid][key] = ev['match'].group(1) == '启用'
            save_binds()
            await bot.finish(ev, f'{ev["match"].group(0)}成功', at_sender=True)
            

@sv.on_prefix('删除角色绑定')
async def delete_arena_sub(bot,ev):
    global binds, lck
    uid = str(ev['user_id'])
    if ev.message[0].type == 'at':
        if not priv.check_priv(ev, priv.SUPERUSER):
            await bot.finish(ev, '删除他人绑定请联系维护', at_sender=True)
            return
        uid = str(ev.message[0].data['qq'])
    elif len(ev.message) == 1 and ev.message[0].type == 'text' and not ev.message[0].data['text']:
        uid = str(ev['user_id'])
    if not uid in binds:
        await bot.finish(ev, '未绑定角色', at_sender=True)
        return
    async with lck:
        binds.pop(uid)
        save_binds()
    await bot.finish(ev, '删除角色绑定成功', at_sender=True)
    
    
@sv.on_fullmatch('角色绑定状态')
async def send_arena_sub_status(bot,ev):
    global binds, lck
    uid = str(ev['user_id'])
    if not uid in binds:
        await bot.send(ev,'您还未绑定角色', at_sender=True)
    else:
        info = binds[uid]
        state=info['state']
        if state=='on':
            msg='出租中'
        if state=='off':
            msg='待租'
        await bot.finish(ev,
    f'''
当前绑定信息：
角色：{info['id']}
大区：{info['Region']}
状态：{msg}
推送：{'开启' if info['push_on'] else '关闭'}''',at_sender=True)

@sv.on_prefix(('查胜场'))
async def shengchang(bot, ev):
    uid = str(ev['user_id'])
    try:
        id1 = str(ev.message[0].data['qq'])
    except:
        id1 = str(ev.user_id)

    if not id1 in binds and id1==uid:
        await bot.finish(ev, '您未绑定角色', at_sender=True)
        return

    elif not id1 in binds and id1!=uid:
        await bot.finish(ev, '目标未绑定角色', at_sender=True)
        return
    try:
        now_time=time.strftime('%Y-%m-%d')
        info = binds[id1]
        key=info['id']
        url='http://300.electricdog.net/300hero/{}'.format(quote(key))
        data=await getjson(url)
        data1=data.get("data")
        last=data1.get("zcLastMatchTime")
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",last)
        last_time=mat.group(0)
        if last_time != now_time:
            msg='\n该用户今日未曾进行游戏'
        else:
            data2=data1.get("zcWin")
            data3=str(data2)
            msg = f'\n用户名：{key}\n今日胜场：{data3}\n最后对局：{last}'
    except ServerDisconnectedError as e:
        msg='\n胜场网出现故障，暂时无法使用'
    except Exception as e:
        msg='\n未绑定角色或角色不存在，请使用指令：绑定角色XXX|大区名'
    await bot.send(ev, msg,at_sender=True)


@sv.on_prefix(('查出租'))
async def chuzu(bot, ev):
    uid = str(ev['user_id'])
    try:
        id1 = str(ev.message[0].data['qq'])
    except:
        id1 = str(ev.user_id)

    if not id1 in binds and id1==uid:
        await bot.finish(ev, '您未绑定角色', at_sender=True)
        return

    elif not id1 in binds and id1!=uid:
        await bot.finish(ev, '目标未绑定角色', at_sender=True)
        return
    info = binds[id1]
    key=info['Region']
    ID=info['id']
    if key in daqu:
        qu='电信区'
    else:
        qu='网通区'
    url='http://api.300mbdl.cn/%E6%8E%A5%E5%8F%A32/%E7%A7%9F%E5%8F%B7/%E7%A7%9F%E5%8F%B7%E5%A4%A7%E5%8E%85?%E9%A1%B5=1&%E9%A1%B5%E9%95%BF=10&%E5%87%BA%E7%A7%9F%E4%B8%AD=true&&%E5%B7%B2%E9%80%89%E5%8C%BA%E6%9C%8D={}%2F{}'.format(quote(qu),quote(key))
    try:
        now_time=time.strftime('%Y-%m-%d')
        url1='http://300.electricdog.net/300hero/{}'.format(quote(ID))
        surl=await getjson(url1)
        surl1=surl.get("data")
        last=surl1.get("zcLastMatchTime")
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",last)
        last_time=mat.group(0)
        if last_time != now_time:
            binds[id1]['win']='0'
            save_binds()
        else:
            surl2=surl1.get("zcWin")
            surl3=str(surl2)
            binds[id1]['win']=surl3
            save_binds()
        true_url=await getjson(url)
        total=true_url.get("total")
        if total==0:
            now=0
        else:
            data=true_url.get("data")
            cun=[]
            for cz in data:
                pd=cz.values()
                if ID not in pd:
                    cun.append('false')
                else:
                    cun.append('true')
            if 'true' in cun:
                for ces in data:
                    get_id=ces.get('F角色名')
                    if get_id ==ID:
                        now=1
                        zhuangtai=ces.get('F状态')
                        shijian=ces.get('F订单时间')
            else:
                now=0
        if now==1:
            msg='\n用户名:{}\n目前状态:{}\n出租时间:{}\n当前胜场:{}'.format(ID,zhuangtai,shijian,binds[id1]['win'])
        else:
            msg='\n用户名:{}\n目前状态:待租\n当前胜场:{}'.format(ID,binds[id1]['win'])
    except Exception as e:
        print(e)
        msg='\n查询出错'
    await bot.finish(ev,msg,at_sender=True)
cache = {}
zhuangtai=''
shijian=''

async def getjson(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json(content_type=None)
            return response

daqu=['风林火山','刀剑神域','圣杯战争','学园都市','威风堂堂','进击巨人','天降之物','邪王真眼','天壤劫火','魔女之夜','失落圣诞','加速世界','恋姬无双','旭日之心','绝灭天使','破军歌姬','境界彼方','镇守府','WCA比赛','极乐净土','甲铁城','赤红之瞳','叛逆骑士','真理之门','万华镜','荣耀','冠位指定','无限剑制','梦想封印','序列之争','镇魂街','十二试炼','序列之争','天之杯','理想乡','超越天堂','群星闪耀']

@sv.scheduled_job('interval', minutes=5)
async def chuzu_schedule():
    global zhuangtai,shijian,cache,binds, lck,daqu
    bot = get_bot()
    bind_cache = {}
    async with lck:
        bind_cache = deepcopy(binds)
    for user in bind_cache:
        info = bind_cache[user]
        key=info['Region']
        ID=info['id']
        uid=info['uid']
        gid=info['gid']
        push_on=info['push_on']
        if push_on ==False:
            continue
        else:
            if key in daqu:
                qu='电信区'
            else:
                qu='网通区'
            url='http://api.300mbdl.cn/%E6%8E%A5%E5%8F%A32/%E7%A7%9F%E5%8F%B7/%E7%A7%9F%E5%8F%B7%E5%A4%A7%E5%8E%85?%E9%A1%B5=1&%E9%A1%B5%E9%95%BF=10&%E5%87%BA%E7%A7%9F%E4%B8%AD=true&&%E5%B7%B2%E9%80%89%E5%8C%BA%E6%9C%8D={}%2F{}'.format(quote(qu),quote(key))
            try:
                sv.logger.info(f'querying {info["id"]} for {info["uid"]}')
                try:
                    now_time=time.strftime('%Y-%m-%d')
                    url1='http://300.electricdog.net/300hero/{}'.format(quote(ID))
                    surl=await getjson(url1)
                    surl1=surl.get("data")
                    last=surl1.get("zcLastMatchTime")
                    mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",last)
                    last_time=mat.group(0)
                    if last_time != now_time:
                        binds[uid]['win']='0'
                        save_binds()
                    else:
                        surl2=surl1.get("zcWin")
                        surl3=str(surl2)
                        binds[uid]['win']=surl3
                        save_binds()
                except Exception as e:
                    print(e)
                wint=binds[uid]['win']
                swint=int(wint)
                res = info['state']
                true_url=await getjson(url)
                total=true_url.get("total")
                if total==0:
                    now=0
                else:
                    data=true_url.get("data")
                    cun=[]
                    for cz in data:
                        pd=cz.values()
                        if ID not in pd:
                            cun.append('false')
                        else:
                            cun.append('true')
                    if 'true' in cun:
                        for ces in data:
                            get_id=ces.get('F角色名')
                            if get_id ==ID:
                                now=1
                                print(now)
                                zhuangtai=ces.get('F状态')
                                shijian=ces.get('F订单时间')
                    else:
                        now=0
                if now==1:
                    if res=='off' or swint>=49:
                        gb='on'
                        binds[uid]['state']=gb
                        save_binds()
                        if swint >=49:
                            tixing='\n\n目前角色胜场已大于49吧，请及时下架！'
                        else:
                            tixing=''
                        await bot.send_group_msg(
                            group_id = int(gid),
                            message = f'[CQ:at,qq={uid}]\n用户名：{ID}\n出租状态：{zhuangtai}\n出租时间：{shijian}\n当前胜场：{wint}'+tixing
                    )
                else:
                    gb='off'
                    binds[uid]['state']=gb
                    save_binds()
            except Exception as e:
                print(e)

                