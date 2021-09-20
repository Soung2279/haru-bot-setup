# -*- coding: utf-8 -*-
import json
import time
import os
import hoshino
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import escape
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

sv_help = '''
基于VDB数据库的虚拟主播查询功能

- [查询vtb/查询虚拟主播+名字]   根据名字查询是否为vtb，可模糊匹配
- [检查vtb名单]   检查本地文件收录情况
'''.strip()

sv = Service(
    name = 'vtb名单',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '查询', #属于哪一类
    help_ = sv_help #帮助文本
    )

JSON_VDB = "./hoshino/modules/vdb/vdb.json"  #此处填写 vdb.json 文件路径
JSON_LIST = "./hoshino/modules/vdb/list.json"  #此处填写 list.json 文件路径

module_update_time = "2021-9-21"    #手动填写插件更新的时间，可无视

@sv.on_fullmatch(["帮助vtb名单", "帮助vdb"])
async def bangzhu_vdb(bot, ev):
    await bot.send(ev, sv_help)

def search_platform_list(): #从list.json获取已收录的平台并生成列表
    path = JSON_LIST
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        meta = json.loads(content)
        platform = meta["meta"]["linkSyntax"]
        ls = platform.keys()
        return ls

def search_vtbname_list():  #从vdb.json获取已收录的虚拟主播并生成列表
    path = JSON_VDB
    f = open(path, 'r', encoding='utf-8')
    content = f.read()
    vdb_dict = json.loads(content)
    na = []
    nums = len(vdb_dict)
    x = 0
    while x < nums:
        x = x+1
        vtnames = vdb_dict[str(f"{x}")][0]
        na.append(vtnames)
    return na

async def get_vtb_info(name):   #汇总查询信息（使用 vdb.json）
    f = open(JSON_VDB, 'r', encoding='utf-8')
    content = f.read()
    vdb_dict = json.loads(content)
    vdb_data = vdb_dict[name]
    vtb_name = vdb_data[0]  #获取vtb原名
    #vtb_extraname = vdb_data[1]  #获取vtb别名（一般为空）
    vtb_de = vdb_data[2]  #获取名称的默认语言
    if vtb_de == "cn":
        vtb_default = str("中文区")
    elif vtb_de == "en":
        vtb_default = str("英文区")
    elif vtb_de == "jp":
        vtb_default = str("日文区")
    else:
        vtb_default = str("未收录")
    
    vtb_type = vdb_data[3]  #获取类型，可以是vtuber，group，fan或unknow
    vtb_bot = vdb_data[4]  #是否为机器人 vtuber/vup
    id = vdb_data[5] #获取账号id
    ac_type = vdb_data[6]  #获取账号类型
    if ac_type == "official":
        account_type = str("官方")
    elif ac_type == "relay":
        account_type = str("搬运")
    else:
        account_type = str("未知类型")
    
    account_platform = vdb_data[7]  #获取直播平台

    vtb_info_1 = f"※虚拟主播名：{vtb_name}\n※活动形式：{vtb_type}\n※活动区域：{vtb_default}"
    vtb_info_2 = f"※是否为AI主播：{vtb_bot}\n※直播/个人平台：{account_platform}\n※平台账号所属：{account_type}"
    platform = search_platform_list()
    if str(account_platform) in platform:   #如果从vdb.json获取到的直播平台在list.json中存在，就给出对应平台的链接
        if account_platform == "youtube":
            plat_url = f"https://www.youtube.com/channel/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "bilibili":
            plat_url = f"https://space.bilibili.com/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "twitter":
            plat_url = f"https://twitter.com/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "userlocal":
            plat_url = f"https://virtual-youtuber.userlocal.jp/user/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "pixiv":
            plat_url = f"https://www.pixiv.net/member.php?id={id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "afdian":
            plat_url = f"https://afdian.net/@{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "peing":
            plat_url = f"https://peing.net/zh-CN/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "ci-en":
            plat_url = f"https://ci-en.net/creator/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "github":
            plat_url = f"https://github.com/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "instagram":
            plat_url = f"https://www.instagram.com/{id}/"
            content = f"账号类型：{account_type}"
        elif account_platform == "booth":
            plat_url = f"https://{id}.booth.pm"
            content = f"账号类型：{account_type}"
        elif account_platform == "marshmallow":
            plat_url = f"https://marshmallow-qa.com/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "amazon.co.jp":
            plat_url = f"https://www.amazon.co.jp/hz/wishlist/ls/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "line":
            plat_url = f"https://line.me/R/ti/p/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "niconico":
            plat_url = f"https://www.nicovideo.jp/user/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "showroom":
            plat_url = f"https://www.showroom-live.com/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "fantia":
            plat_url = f"https://fantia.jp/fanclubs/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "twitch":
            plat_url = f"https://www.twitch.tv/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "tiktok":
            plat_url = f"https://www.tiktok.com/@{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "weibo":
            plat_url = f"https://www.weibo.com/u/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "web":
            plat_url = f"{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "facebook":
            plat_url = f"https://www.facebook.com/{id}/"
            content = f"账号类型：{account_type}"
        elif account_platform == "email":
            plat_url = f"{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "jvcmusic":
            plat_url = f"https://www.jvcmusic.co.jp/-/Artist/{id}.html"
            content = f"账号类型：{account_type}"
        elif account_platform == "telegram":
            plat_url = f"https://t.me/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "patreon":
            plat_url = f"https://www.patreon.com/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "teespring":
            plat_url = f"https://teespring.com/stores/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "popiask":
            plat_url = f"https://www.popiask.cn/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "163music":
            plat_url = f"https://music.163.com/#/user/home?id={id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "other":
            plat_url = f"{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "pomeet":
            plat_url = f"https://www.pomeet.com/{id}"
            content = f"账号类型：{account_type}"
        elif account_platform == "acfun":
            plat_url = f"https://www.acfun.cn/u/{id}"
            content = f"账号类型：{account_type}"
        else:
            plat_url = f"https://github.com/dd-center/vdb"
            content = f"已在list.json文件中获取到该平台，但bot暂未更新。请提醒管理员检查。"
    else:
        plat_url = f"https://github.com/dd-center/vdb"
        content = f"暂未收录该平台。"

    vtb_share = {
        "type": "share",
        "data": {
            "url": f"{plat_url}",
            "title": f"{vtb_name} 的 {account_platform}",
            "content": f"{content}",
            }
        }
    return vtb_info_1, vtb_info_2, vtb_share


def keyword_search(keyword):    #通过vtb名字查询
    f = open(JSON_VDB, 'r', encoding='utf-8')
    content = f.read()
    vdb_dict = json.loads(content)
    result = []
    for names in vdb_dict:
        if keyword in vdb_dict[names][0]:#or keyword in vdb_dict[names][1]
            #此条是获取vtb的别名，但由于list.json本身绝大多数别名均为空，所以没有使用。
            result.append(names)
    return result

def timestamp_datatime(value):  #转换UNIX时间戳为普通时间格式
    format = '%Y-%m-%d %H:%M'
    value = time.localtime(value)
    dt = time.strftime(format,value)
    return dt

@sv.on_suffix(('是vtb吗', '是虚拟主播吗'))
@sv.on_prefix(('查询vtb', '查询虚拟主播'))
async def search_vdb(bot, ev: CQEvent):
    names_vtb_list = search_vtbname_list()
    input = ev.message.extract_plain_text()
    if not input:
        await bot.send(ev, "不告诉我名字要怎么查询啦！")
        return

    input_name = escape(ev.message.extract_plain_text().strip())
    #guess_data = process.extractOne(input_name, names_vtb_list)    #此条为返回模糊匹配精度最高的一条，若需使用请注释下一行
    guess_data = process.extract(input_name, names_vtb_list, limit=3)

    if input in names_vtb_list:
        search_name_list = keyword_search(input)
        vtb_info_1, vtb_info_2, vtb_share = await get_vtb_info(search_name_list[0])
        final = vtb_info_1 + '\n' + vtb_info_2
    else:
        #guess_num = guess_data[1]
        #guess_word = guess_data[0] #此条为从模糊匹配精度最高的一条中获取精度百分比和匹配文本，若需使用请将下面的注释掉
        guess_num1 = guess_data[0][1]
        guess_word1 = guess_data[0][0]
        guess_num2 = guess_data[1][1]
        guess_word2 = guess_data[1][0]
        guess_num3 = guess_data[2][1]
        guess_word3 = guess_data[2][0]
        final1 = f"暂未查找到叫 {input} 的人哦！\n"
        final2 = f"您有{guess_num1}%的可能在找“{guess_word1}”。\n"
        final3 = f"您有{guess_num2}%的可能在找“{guess_word2}”。\n"
        final4 = f"您有{guess_num3}%的可能在找“{guess_word3}”。\n"
        #默认返回3条结果，如果想返回更多请按上面格式在此处添加新项
        final = final1 + '\n' + final2 + final3 + final4
        #如果修改了返回数量请在此处同步修改

        vtb_share = False
        if int(guess_num1+guess_num2+guess_num3) < 100: #默认三条精度百分比总和小于100时判定为未收录
        #如果修改了返回数量请在此处同步修改
            final = f"暂未收录该虚拟主播哦！"
            await bot.send(ev, final)
            return

    await bot.send(ev, final)
    if not vtb_share is False:
        await bot.send(ev, vtb_share)

@sv.on_fullmatch(["检查vtb名单", "检查vdb"])
async def check_vdb(bot, ev):
    names_vtb_list = search_vtbname_list()
    platform = search_platform_list()
    vtb_counts = len(names_vtb_list)
    plat_counts = len(platform)
    path = JSON_LIST
    warning = ''
    warn_update = ''
    warn_list = ''
    warn_vdb = ''
    warn_main = ''
    receiver = hoshino.config.SUPERUSERS[0]

    if True:
        if not(os.path.exists("./hoshino/modules/vdb/update.sample")):
            warn_update = f"更新所需文件：update.sample缺失\n"
        if not(os.path.exists(JSON_LIST)):
            warn_list = f"vdb数据文件：list.json缺失\n"
        if not(os.path.exists(JSON_VDB)):
            warn_vdb = f"收录条目文件：vdb.json缺失\n"
        if not(os.path.exists("./hoshino/modules/vdb/vdb.py")):   #如果没了这个文件这行代码也没有了捏（但是为了好看还是写上了）
            warn_main = f"运行主文件：vdb.py缺失\n"
        warning = warn_update + warn_list + warn_vdb + warn_main

    if not warning == '':
        final_msg = f"vtb名单检测到文件缺失：\n{warning}"
        await bot.send(ev, final_msg)
        await bot.send_private_msg(user_id=receiver, message=final_msg)  #如果出现文件缺失，bot将私聊第一位超级管理员
    else:
        await bot.send(ev, f"文件检查完整。")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        meta = json.loads(content)
        updateunix = meta["meta"]["timestamp"]
        normal_time = timestamp_datatime(updateunix)
        await bot.send(ev,f"当前收录了{vtb_counts}位虚拟主播，当前收录了{plat_counts}个直播/个人平台")
        await bot.send(ev, f"插件最近更新时间：{module_update_time}\n收录条目最近更新时间：{normal_time}")


