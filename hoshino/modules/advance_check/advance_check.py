'''
made by Soung2279@github
业余写着玩玩，还望大佬海涵（能跑就行.jpg）
'''
import wmi  #需要依赖：wmi

import socket,time,datetime
import platform
import sys

import re
import asyncio
import hoshino

from hoshino import Service, priv, config, util
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.typing import CQEvent

forward_msg_exchange = config.FORWARD_MSG_EXCHANGE
forward_msg_name = config.FORWARD_MSG_NAME
forward_msg_uid = config.FORWARD_MSG_UID
recall_msg_set = config.RECALL_MSG_SET
RECALL_MSG_TIME = config.RECALL_MSG_TIME

_max = 3  #每天查看配置的次数
_nlmt = DailyNumberLimiter(_max)

_cd = 3  #每次查看配置的冷却时间(s)
_flmt = FreqLimiter(_cd)

WARNING_NOTICE = f"今天已经查看{_max}次了！"  #到达上限的提示语

w = wmi.WMI()  #不要动！

# 获取内存信息
cs = w.Win32_ComputerSystem()
pfu = w.Win32_PageFileUsage()
MemTotal = int(cs[0].TotalPhysicalMemory)/1024/1024
memsize = str(MemTotal)
memory_info_1 = f"总共物理内存: {memsize}M"
#MemFree = int(cs[0].FreePhysicalMemory)/1024
#mem_free_size = str(MemFree)
#memory_info_2 = f"可用物理内存: {mem_free_size}M"   #好像FreePhysicalMemory不好使了，总之先注释掉
SwapTotal = int(pfu[0].AllocatedBaseSize)
swapsize = str(SwapTotal)
memory_info_3 = f"总共虚拟内存: {swapsize}M"
#SwapFree = int(pfu[0].AllocatedBaseSize - pfu[0].CurrentUsage)
#swap_free_size = str(SwapFree)
#memory_info_4 = f"可用虚拟内存: {swap_free_size}M"   #同上

for memModule in w.Win32_PhysicalMemory():
    totalMemSize = int(memModule.Capacity)
    memory_info_0 = f"内存厂商: {memModule.Manufacturer}"

# 获取电脑使用者信息
for CS in w.Win32_ComputerSystem():
    computer_info_1 = f"电脑名称: {CS.Caption}"
    computer_info_2 = f"使用者: {CS.UserName}"
    computer_info_3 = f"制造商: {CS.Manufacturer}"
    computer_info_4 = f"系统信息: {CS.SystemFamily}"
    computer_info_5 = f"工作组: {CS.Workgroup}"
    computer_info_6 = f"机器型号: {CS.model}"

# 获取操作系统信息
for OS in w.Win32_OperatingSystem():
    operating_info_1 = f"操作系统: {OS.Caption}"
    operating_info_2 = f"语言版本: {OS.MUILanguages}"
    operating_info_3 = f"系统位数: {OS.OSArchitecture}"
    operating_info_4 = f"注册人: {OS.RegisteredUser}"
    operating_info_5 = f"系统驱动: {OS.SystemDevice}"
    operating_info_6 = f"系统目录: {OS.SystemDirectory}"

# 获取电脑IP和MAC信息
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
network_info_0 = f"计算机名称: {hostname}"
network_info_1 = f"IP地址: {ip}"

for address in w.Win32_NetworkAdapterConfiguration():
    network_info_2 = f"MAC地址: {address.MACAddress}"
    network_info_3 = f"网络描述: {address.Description}"

# 获取电脑CPU信息
for processor in w.Win32_Processor():
    processor_info_1 = f"CPU型号: {processor.Name}"
    processor_info_2 = f"CPU核数: {processor.NumberOfCores}"

# 获取BIOS信息
for BIOS in w.Win32_BIOS():
    bios_info_1 = f"使用日期: {BIOS.Description}"
    bios_info_2 = f"主板型号: {BIOS.SerialNumber}"
    bios_info_3 = f"当前语言: {BIOS.CurrentLanguage}"

# 获取磁盘信息
for disk in w.Win32_DiskDrive():
    disk_info_1 = f"磁盘名称: {disk.Caption}"
    disksize = int(disk.Size)/1024/1024/1024
    size = str(disksize)
    disk_info_2 = f"磁盘大小: {size}G"

# 获取显卡信息
for xk in w.Win32_VideoController():
    video_info_1 = f"显卡名称: {xk.name}"

COMPUTER_INFO_ALL = f"{computer_info_1}\n{computer_info_2}\n{computer_info_3}\n{computer_info_4}\n{computer_info_5}\n{computer_info_6}"
OPERATING_INFO_ALL = f"{operating_info_1}\n{operating_info_2}\n{operating_info_3}\n{operating_info_4}\n{operating_info_5}\n{operating_info_6}"
NETWORK_INFO_ALL = f"{network_info_0}\n{network_info_1}\n{network_info_2}\n{network_info_3}"
PROCESSOR_INFO_ALL = f"{processor_info_1}\n{processor_info_2}"
BIOS_INFO_ALL = f"{bios_info_1}\n{bios_info_2}\n{bios_info_3}"
MEMORY_INFO_ALL = f"{memory_info_1}\n{memory_info_3}"
DISK_INFO_ALL = f"{disk_info_1}\n{disk_info_2}"
VIDEO_INFO_ALL = f"{video_info_1}"



sv_help = '''
简单的查看电脑/服务器各项硬件信息。
- [@bot看看配置]  查看
'''.strip()

sv = Service(
    name = 'advance_check',  #功能名
    use_priv = priv.ADMIN, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'advance', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助advance_check", "advance_check帮助"])
async def bangzhu_adck(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_fullmatch(('adcheck', '鲁大师', '看看配置', '看看服务器', 'adck'), only_to_me=True)  #需要@bot是为了防误触发，可以自行修改
async def advance_check_set(bot, ev: CQEvent):
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, WARNING_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, f"查询冷却中：{_cd}秒", at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    if not priv.check_priv(ev, priv.SUPERUSER):   #建议使用priv.SUPERUSER
        util.log(f"{ev.user_id}尝试查看服务器配置, 已拒绝")
        not_allowed_msg = f"权限不足。"  #权限不足时回复的消息
        await bot.send(ev, not_allowed_msg, at_sender=True)
    else:
        if forward_msg_exchange == 1:  #简易的判断是否使用合并转发
            data_all = []
            text1 = COMPUTER_INFO_ALL
            data1 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text1
                }
            }
            text2 = OPERATING_INFO_ALL
            data2 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text2
                }
            }
            text3 = NETWORK_INFO_ALL
            data3 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text3
                }
            }            
            text4 = PROCESSOR_INFO_ALL
            data4 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text4
                }
            }            
            text5 = BIOS_INFO_ALL
            data5 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text5
                }
            }            
            text6 = MEMORY_INFO_ALL
            data6 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text6
                }
            }            
            text7 = DISK_INFO_ALL
            data7 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text7
                }
            }            
            text8 = VIDEO_INFO_ALL
            data8 = {
                "type": "node",
                "data": {
                    "name": f"{forward_msg_name}",
                    "uin": f"{forward_msg_uid}",
                    "content": text8
                }
            }
            data_all=[data1,data2,data3,data4,data5,data6,data7,data8]
            if recall_msg_set == 1:  #简易的判断是否定时撤回
                recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
                notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")
                
                await asyncio.sleep(RECALL_MSG_TIME)

                await bot.delete_msg(message_id=recall['message_id'])
                await bot.delete_msg(message_id=notice['message_id'])
            else:
                await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
        else:
            if recall_msg_set == 1:  #简易的判断是否定时撤回
                recall_1 = await bot.send(ev, COMPUTER_INFO_ALL)
                recall_2 = await bot.send(ev, OPERATING_INFO_ALL)
                recall_3 = await bot.send(ev, NETWORK_INFO_ALL)
                recall_4 = await bot.send(ev, PROCESSOR_INFO_ALL)
                recall_5 = await bot.send(ev, BIOS_INFO_ALL)
                recall_6 = await bot.send(ev, MEMORY_INFO_ALL)
                recall_7 = await bot.send(ev, DISK_INFO_ALL)
                recall_8 = await bot.send(ev, VIDEO_INFO_ALL)
                notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

                await asyncio.sleep(RECALL_MSG_TIME)

                await bot.delete_msg(message_id=recall_1['message_id'])
                await bot.delete_msg(message_id=recall_2['message_id'])
                await bot.delete_msg(message_id=recall_3['message_id'])
                await bot.delete_msg(message_id=recall_4['message_id'])
                await bot.delete_msg(message_id=recall_5['message_id'])
                await bot.delete_msg(message_id=recall_6['message_id'])
                await bot.delete_msg(message_id=recall_7['message_id'])
                await bot.delete_msg(message_id=recall_8['message_id'])
                await bot.delete_msg(message_id=notice['message_id'])
            else:
                await bot.send(ev, COMPUTER_INFO_ALL)
                await bot.send(ev, OPERATING_INFO_ALL)
                await bot.send(ev, NETWORK_INFO_ALL)
                await bot.send(ev, PROCESSOR_INFO_ALL)
                await bot.send(ev, BIOS_INFO_ALL)
                await bot.send(ev, MEMORY_INFO_ALL)
                await bot.send(ev, DISK_INFO_ALL)
                await bot.send(ev, VIDEO_INFO_ALL)

'''
原项目地址：
作者主页：https://github.com/Soung2279
'''

