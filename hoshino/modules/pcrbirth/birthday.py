from hoshino import Service, logger, priv
from hoshino.modules.priconne import chara
import json

import datetime
import hoshino
import re
import os
import random
import requests

CHARA_DATA_DIR = "./hoshino/modules/pcrbirth/unitdata.json" # 请自行修改
CHARA_DATA_API = "https://api.purinbot.cn/chara"
MAIN_DATA_SOURCE = 1 # 首选角色数据源：0.本地数据 1.在线api（不用手动更新数据）
UPDATE_LOCAL_DATA = ('更新本地数据') # 更新本地角色数据的命令

bdrm_help = '''
生日提醒
'''.strip()

bdrm = Service(
    name = 'pcr生日提醒',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '订阅', #属于哪一类
    help_ = bdrm_help #帮助文本
    )

@bdrm.on_fullmatch(["帮助pcr生日提醒"])
async def bangzhu_pcrbirth_rem(bot, ev):
    await bot.send(ev, bdrm_help, at_sender=True)


svbdsrh_help = '''
- [谁的生日是+日期] 看看这天哪位老婆过生日
- [谁的生日是今天] 看看今天哪位老婆过生日   
- [角色+生日是哪天] 看看老婆哪天过生日
'''.strip()

svbdsrh = Service(
    name = 'pcr生日查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = svbdsrh_help #帮助文本
    )

@svbdsrh.on_fullmatch(["帮助pcr生日查询"])
async def bangzhu_pcrbirth_sear(bot, ev):
    await bot.send(ev, svbdsrh_help, at_sender=True)


def download_chara_dara():
    try:
        chara_data = requests.request('GET', CHARA_DATA_API, timeout=5).json()
    except requests.exceptions.ConnectTimeout:
        hoshino.logger.error('`pcr生日提醒` 角色数据API TIMEOUT')
        chara_data = 'error'
    return chara_data

def read_local_chara_data():
    if os.path.exists(CHARA_DATA_DIR):
        with open(CHARA_DATA_DIR,"r",encoding='utf-8') as dump_f:
            try:
                chara_data = json.load(dump_f)
            except:
                hoshino.logger.error('`pcr生日提醒` 本地角色数据文件读取失败')
                chara_data = 'error'
    else:
        hoshino.logger.error('`pcr生日提醒` 本地角色数据文件不存在')
        chara_data = 'error'
    return chara_data

def save_chara_data(data):
    with open(CHARA_DATA_DIR,"w",encoding='utf-8') as dump_f:
        json.dump(data,dump_f,indent=4,ensure_ascii=False)
    return 

def update_local_data():
    chara_data = download_chara_dara()
    if chara_data != 'error':
        save_chara_data(chara_data)
    return

def load_chara_data():
    if MAIN_DATA_SOURCE:
        chara_data = download_chara_dara()
        if chara_data == 'error':
            chara_data = read_local_chara_data()
    else: # MAIN_DATA_SOURCE == 0
        chara_data = read_local_chara_data()
        if chara_data == 'error':
            chara_data = download_chara_dara()
            if chara_data != 'error':
                save_chara_data(chara_data)
    if chara_data == 'error':
        hoshino.logger('`pcr生日提醒` 本地和在线数据源均出错，救不了了')
        return
    return chara_data

def uid2card(uid, user_card_dict):
    return str(uid) if uid not in user_card_dict.keys() else user_card_dict[uid]

def get_cqcode(chara_id):
    dir_path = os.path.join(os.path.expanduser(hoshino.config.RES_DIR), 'img', 'priconne', 'unit')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    c = chara.fromid(chara_id)
    cqcode = '' if not c.icon.exist else c.icon.cqcode
    return c.name, cqcode
    
def date_convert(date_text_origin):
    if '今天' in date_text_origin:
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
    else:
        tmp = re.sub(r'\D',' ',date_text_origin)
        date_num_list = re.findall(r'\d{1,2}',tmp)
        if len(date_num_list) != 2:
            return date_num_list[0]
        month = date_num_list[0]
        day = date_num_list[1]
    date_text_format = f'{month}月{day}日'
    return date_text_format

@bdrm.scheduled_job('cron', hour='00', minute='01')
async def birthday_reminder():
    unitdata = load_chara_data()
    chara_id_list = list(unitdata.keys())
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    birthdate = str(month)+'月' + str(day) + '日'
    birthday_chara_id = 0
    #测试用
    #birthdate = '2月2日'
    birthday_chara_id_lst = []
    for i in range(len(chara_id_list)):
        if unitdata[chara_id_list[i]]['生日'] == birthdate:
            birthday_chara_id_lst.append(int(chara_id_list[i]))
    ninsuu = len(birthday_chara_id_lst)
    if ninsuu == 0:
        return
    else:
        msg = f'今天有{ninsuu}人过生日：\n'
        for caraId in birthday_chara_id_lst:
            name, cqcode = get_cqcode(caraId)
            msg = msg + f'{name}ちゃん{cqcode}在今天过生日哦~\n'
        await bdrm.broadcast(msg, 'birthday_reminder', 0.2)

@svbdsrh.on_suffix(('生日是那天','生日是哪天','生日那天','生日哪天','生日在那天','生日在哪天','那天过生日','哪天过生日','那天生日','哪天生日'))
async def birthday_search_chara(bot, ev):
    unitdata = load_chara_data()
    name = ev.message.extract_plain_text().strip()
    if not name:
        await bot.send(ev, f'没有找到“{name}”的生日信息呢...')
        return
    chara_id = chara.name2id(name)
    confi = 100
    if chara_id == chara.UNKNOWN:
        chara_id, guess_name, confi = chara.guess_id(name)
    if confi > 60:
        chara_birthday = unitdata[str(chara_id)]['生日']
        if not chara_birthday:
            await bot.send(ev, f'没有找到“{name}”的生日信息呢...')
            return
        else:
            chara_name, cqcode = get_cqcode(chara_id)
            await bot.send(ev, f'{chara_name}ちゃん{cqcode}在{chara_birthday}过生日哦~')

@svbdsrh.on_prefix(('谁的生日','谁生日'))
@svbdsrh.on_suffix(('谁生日','谁的生日'))
async def birthday_search_date(bot, ev):
    unitdata = load_chara_data()
    chara_id_list = list(unitdata.keys())
    date_text = ev.message.extract_plain_text().strip()
    birthdate = date_convert(date_text)
    if re.match(r"(\d{1,2}月\d{1,2}日)",birthdate) == "":
        await bot.send(ev, f'请输入正确的日期哦~如"0723"或者"7月23日"')
        return
    birthday_chara_id_lst = []
    for i in range(len(chara_id_list)):
        if unitdata[chara_id_list[i]]['生日'] == birthdate:
            birthday_chara_id_lst.append(int(chara_id_list[i]))
    ninsuu = len(birthday_chara_id_lst)
    if ninsuu == 0:
        await bot.send(ev, f'{birthdate}没有人过生日哦~')
        return
    else:
        msg = f'{birthdate}有{ninsuu}人过生日：\n'
        for caraId in birthday_chara_id_lst:
            name, cqcode = get_cqcode(caraId)
            msg = msg + f'{name}ちゃん{cqcode}在{birthdate}过生日哦~\n'
        await bot.send(ev, msg)

@svbdsrh.on_fullmatch(UPDATE_LOCAL_DATA)
async def birthday_update_local_data(bot, ev):
    if priv.check_priv(ev,priv.SUPERUSER):
        update_local_data()
        await bot.send(ev, '已更新角色数据', at_sender=True)
