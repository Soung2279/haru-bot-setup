# coding=utf-8
from .compareData import *
from hoshino import Service,priv
from hoshino.typing import HoshinoBot,CQEvent
from nonebot import get_bot

sv_help = '''
- 雀魂订阅
- 关闭雀魂订阅
- 开启雀魂订阅
- 雀魂订阅状态
- 删除雀魂订阅
- 三麻订阅
- 关闭三麻订阅
- 开启三麻订阅
- 三麻订阅状态
- 删除三麻订阅
'''.strip()

sv = Service(
    name = '雀魂对局订阅',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '雀魂', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_prefix("雀魂订阅")
async def orderInfo(bot, ev: CQEvent):
    nickname = ev.message.extract_plain_text()
    IDdata = getID(nickname)
    message = ""
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次再进行订阅")
    else:
        if len(IDdata) > 1:
            gid = ev["group_id"]
            playerRecord = selectRecord(IDdata[0]["id"])  # 获取对局记录
            if jsonWriter(playerRecord, gid, IDdata[0]["id"]):
                message = message + "查询到多条角色昵称呢~，若订阅不是您想订阅的昵称，请补全昵称后重试\n"
                message = message + "昵称:" + str(IDdata[0]["nickname"]) + " 的对局已订阅成功\n"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)
        else:
            gid = ev["group_id"]
            playerRecord = selectRecord(IDdata[0]["id"]) #获取对局记录
            if jsonWriter(playerRecord,gid,IDdata[0]["id"]):
                message = message + "昵称:" + str(IDdata[0]["nickname"])+" 的对局已订阅成功\n"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)

@sv.on_prefix(("关闭雀魂订阅","取消雀魂订阅"))
async def cancelOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    gid = ev["group_id"]
    message = ""
    record = localLoad()
    flag = False
    IDdata = getID(nickname)
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    datalist=[]
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = False
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +" 在本群的四麻订阅已成功关闭\n")
        else:
            await bot.finish(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试\n")

@sv.on_prefix("开启雀魂订阅")
async def openOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    gid = ev["group_id"]
    record = localLoad()
    flag = False
    IDdata = getID(nickname)
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    message = ""
    datalist=[]
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = True
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +"在本群的四麻订阅已成功开启\n")
        else:
            await bot.send(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试\n")

@sv.scheduled_job('interval', minutes=3)
async def record_scheduled():
    bot = get_bot()
    record = localLoad()
    for i in range(0,len(record)):
        playerRecord = selectRecord(record[i]["id"])
        if playerRecord == -1:
            sv.logger.info("获取" + str(record[i]["id"]) + "的对局数据超时已自动跳过")
            continue
        compareRecord = json.loads(playerRecord)
        sv.logger.info("正在检测更新"+str(record[i]["id"])+"的对局数据")
        if int(record[i]["endTime"]) < int(compareRecord[0]["endTime"]):
            message = updateData(playerRecord,record[i]["gid"],record[i]["id"])
            await bot.send_group_msg(group_id=int(record[i]["gid"]),message=message)

@sv.on_fullmatch("雀魂订阅状态")
async def orderSituation(bot,ev):
    gid = ev["group_id"]
    datalist = []
    message = ""
    record = localLoad()
    for i in range(0,len(record)):
        if int(record[i]["gid"]) == int(gid):
            datalist.append(record[i])
    if datalist == []:
        await bot.finish(ev,"本群还没有雀魂对局的订阅哦\n")
    else:
        message = message + "已查询到群"+str(gid)+"的订阅状态:\n"
        for i in range(0,len(datalist)):
            data = selectNickname(datalist[i]["id"])
            sv.logger.info("正在获取"+str(datalist[i]["id"])+"的昵称信息")
            if data == -1:
                await bot.finish(ev, "获取昵称信息失败，请重试")
            else:
                message = message + "昵称：" + selectNickname(datalist[i]["id"]) + "   "
            if datalist[i]["record_on"]:
                message = message + "开启\n"
            else:
                message = message + "关闭\n"
        await bot.send(ev,message)

@sv.on_prefix("删除雀魂订阅")
async def delInfo(bot,ev):
    nickname = ev.message.extract_plain_text()
    gid = ev["group_id"]
    record = localLoad()
    flag = False
    IDdata = getID(nickname)
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    datalist = []
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0, len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"] == record[i]["id"]:
                flag = True
                continue
            else:
                datalist.append(record[i])
        if flag:
            with open(join(path, 'account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev, "该昵称在本群的四麻订阅已删除\n")
        else:
            await bot.send(ev, "没有找到该昵称在本群的订阅记录哦，请检查后重试\n")

@sv.on_prefix("三麻订阅")
async def orderTriInfo(bot, ev: CQEvent):
    nickname = ev.message.extract_plain_text()
    IDdata = getTriID(nickname)
    message = ""
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次再进行订阅")
    else:
        if len(IDdata) > 1:
            gid = ev["group_id"]
            playerRecord = selectTriRecord(IDdata[0]["id"])  # 获取对局记录
            if jsonTriWriter(playerRecord, gid, IDdata[0]["id"]):
                message = message + "查询到多条角色昵称呢~，若订阅不是您想订阅的昵称，请补全昵称后重试\n"
                message = message + "昵称:" + str(IDdata[0]["nickname"]) + " 的对局已订阅成功\n"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)
        else:
            gid = ev["group_id"]
            playerRecord = selectTriRecord(IDdata[0]["id"]) #获取对局记录
            if jsonTriWriter(playerRecord,gid,IDdata[0]["id"]):
                message = message + "昵称:" + str(IDdata[0]["nickname"])+" 的对局已订阅成功\n"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)

@sv.on_prefix(("关闭三麻订阅","取消三麻订阅"))
async def cancelTriOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    gid = ev["group_id"]
    message = ""
    record = localTriLoad()
    flag = False
    IDdata = getTriID(nickname)
    datalist=[]
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = False
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'tri_account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +" 在本群的三麻订阅已成功关闭\n")
        else:
            await bot.send(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试\n")

@sv.on_prefix("开启三麻订阅")
async def openTriOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    gid = ev["group_id"]
    record = localTriLoad()
    flag = False
    IDdata = getTriID(nickname)
    message = ""
    datalist=[]
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = True
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'tri_account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +"在本群的三麻订阅已成功开启\n")
        else:
            await bot.send(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试\n")

@sv.scheduled_job('interval', minutes=3)
async def Trirecord_scheduled():
    bot = get_bot()
    record = localTriLoad()
    for i in range(0,len(record)):
        playerRecord = selectTriRecord(record[i]["id"])
        if playerRecord == -1:
            sv.logger.info("获取" + str(record[i]["id"]) + "的三麻对局数据超时已自动跳过")
            continue
        compareRecord = json.loads(playerRecord)
        sv.logger.info("正在检测更新"+str(record[i]["id"])+"的三麻对局数据")
        if int(record[i]["endTime"]) < int(compareRecord[0]["endTime"]):
            message = updateTriData(playerRecord,record[i]["gid"],record[i]["id"])
            await bot.send_group_msg(group_id=int(record[i]["gid"]),message=message)

@sv.on_fullmatch("三麻订阅状态")
async def orderSituation(bot,ev):
    gid = ev["group_id"]
    datalist = []
    message = ""
    record = localTriLoad()
    for i in range(0,len(record)):
        if int(record[i]["gid"]) == int(gid):
            datalist.append(record[i])
    if datalist == []:
        await bot.finish(ev,"本群还没有雀魂三麻对局的订阅哦\n")
    else:
        message = message + "已查询到群"+str(gid)+"的订阅状态:\n"
        for i in range(0,len(datalist)):
            data = selectTriNickname(datalist[i]["id"])
            sv.logger.info("正在获取" + str(datalist[i]["id"]) + "的昵称信息")
            if data == -1:
                await bot.finish(ev, "获取昵称信息失败，请重试")
            else:
                message = message + "昵称：" + selectTriNickname(datalist[i]["id"]) + "    "
            if datalist[i]["record_on"]:
                message = message + "开启\n"
            else:
                message = message + "关闭\n"
        await bot.send(ev,message)

@sv.on_prefix("删除三麻订阅")
async def delTriInfo(bot,ev):
    nickname = ev.message.extract_plain_text()
    gid = ev["group_id"]
    record = localTriLoad()
    flag = False
    IDdata = getTriID(nickname)
    datalist = []
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0, len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"] == record[i]["id"]:
                flag = True
                continue
            else:
                datalist.append(record[i])
        if flag:
            with open(join(path, 'tri_account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev, "该昵称在本群的三麻订阅已删除\n")
        else:
            await bot.send(ev, "没有找到该昵称在本群的订阅记录哦，请检查后重试\n")