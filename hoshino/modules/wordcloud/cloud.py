from posixpath import supports_unicode_filenames
from time import time
import time
import datetime
import jieba
import re, os, shutil
import nonebot
import wordcloud
import random
import hoshino
from hoshino.typing import CQEvent
from hoshino import Service, priv
from nonebot import MessageSegment,NoticeSession
import base64
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

sv_help = '''
- [生成今日词云]  看看今天的群聊词云
- [生成昨日词云]  看看昨天的群聊词云
- [检查词云]
- [清理词云]
'''.strip()

sv = Service(
    name = '词云',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = True, #默认启用
    bundle = '通用', #分组归类
    help_ = sv_help #帮助说明
    )

loadpath = 'G:\\Gomirai\\logs\\'#此处填gocq的logs路径
self_id = '756160433'#此处填机器人的QQ号
load_in_path = 'G:\\Gomirai\\wordcloud'#此处填词云图片保存的路径
wd_img = 'G:\\qqbot\\hoshino\\modules\\wordcloud\\wd.png' #此处填词云的背景图片

@nonebot.scheduler.scheduled_job(
    'cron',
    day='*',
    hour='23',
    minute='55'
)
async def makecloud():
    bot=nonebot.get_bot()
    try:
        makeclouds()
    except Exception as e:
        today = datetime.date.today().__format__('%Y-%m-%d')
        await bot.send_private_msg(user_id=hoshino.config.SUPERUSERS[2], message=f'{today}词云生成失败,失败原因:{e}')
        

    
def random_color_func(word=None, font_size=None, position=None,
                      orientation=None, font_path=None, random_state=None):
  
    if random_state is None:
        random_state = Random()
    return "hsl(%d, 75%%, 62%%)" % random_state.randint(0, 225)#值，饱和度，色相
    
def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root,name))
                print("删除词云文件：" + os.path.join(root,name))

def makeclouds(gid):
    global loadpath
    global load_in_path
    bot = nonebot.get_bot()
    today = datetime.date.today().__format__('%Y-%m-%d')
    f = open(loadpath + f"\\{today}.log", "r", encoding="utf-8")
    f.seek(0)
    gida = str(gid)
    msg=''
    for line in f.readlines():          #删除前缀和自己的发言
        if self_id in line or gida not in line:
            continue
        try:                         
            o = line.split("的消息: ")[1]
            msg += o  
        except:
            pass
    msg = re.sub('''[a-zA-Z0-9'!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘'！[\\]^_`{|}~\s]+''', "", msg)
    msg = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+', '', msg)
    banword = []#此处为不显示的删除禁词
    ls = jieba.lcut(msg,cut_all=True)#制作分词
    stopwords = set()
    content = [line.strip() for line in open(load_in_path+f"\\tyc.txt",\
               encoding='utf-8').readlines()]
    stopwords.update(content)
    txt = " ".join(ls)
    bg_pic=np.array(Image.open(wd_img))
    w = wordcloud.WordCloud(mask=bg_pic,font_path=load_in_path+f"\\SimHei.ttf",\
                            max_words=10000, width=1000, height=700,\
                            background_color='white',stopwords=stopwords,\
                            relative_scaling=0.5,min_word_length=2,\
                            color_func=random_color_func#调色
        )
    w.generate(txt)
    del_files(load_in_path)
    w.to_file(f"{today}.png")
    shutil.move(f"{today}.png",load_in_path)
    srcFile = f"{load_in_path}\\{today}.png"
    dstFile = f"{load_in_path}\\{today}-{gid}.png"
    os.rename(srcFile,dstFile)
        
def makecloudsb(gid):
    global loadpath
    global load_in_path
    bot = nonebot.get_bot()
    today = datetime.date.today().__format__('%Y-%m-%d')
    yesterday = (datetime.date.today() + datetime.timedelta(-1)).__format__('%Y-%m-%d')
    gida = str(gid)
    f = open(loadpath + f"\\{yesterday}.log", "r", encoding="utf-8")
    f.seek(0)
    msg=''
    for line in f.readlines():          #删除前缀和自己的发言
        if self_id in line or gida not in line:
            continue
        try:                         
            o = line.split("的消息: ")[1]
            msg += o  
        except:
            pass
    msg = re.sub('''[a-zA-Z0-9'!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘'！[\\]^_`{|}~\s]+''', "", msg)
    msg = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+', '', msg)
    banword = []#此处为不显示的删除禁词
    ls = jieba.lcut(msg)#制作分词
    stopwords = set()
    content = [line.strip() for line in open(load_in_path+f"\\tyc.txt",encoding='utf-8').readlines()]
    stopwords.update(content)
    txt = " ".join(ls)
    bg_pic=np.array(Image.open(wd_img))
    w = wordcloud.WordCloud(mask=bg_pic,font_path=load_in_path+f"\\SimHei.ttf",\
                            max_words=10000, width=1000, height=700,\
                            background_color='white',stopwords=stopwords,\
                            relative_scaling=0.5,min_word_length=2,\
                            color_func=random_color_func#词汇上限，宽，高,背景颜色去除停用词(tyc.txt),频次与大小相关度，最小词长,调色
        )
    w.generate(txt)
    del_files(load_in_path)
    w.to_file(f"{yesterday}.png")
    shutil.move(f"{yesterday}.png",load_in_path)
    srcFile = f"{load_in_path}\\{yesterday}.png"
    dstFile = f"{load_in_path}\\{yesterday}-{gid}.png"
    os.rename(srcFile,dstFile)


@sv.on_rex(f'^查询(.*)月(\d+)日词云$')
async def ciyun(bot, ev: CQEvent):
    match = ev['match']
    gid = ev['group_id']
    month = int(match.group(1))
    day = int(match.group(2))
    await bot.send(ev,MessageSegment.image(f'file:///{load_in_path}//2021-{month:02}-{day:02}.png'))

@sv.on_fullmatch('生成今日词云')
async def getciyun(bot, ev: CQEvent):
    gid = ev['group_id']
    if not hoshino.priv.check_priv(ev, hoshino.priv.ADMIN):
        await bot.send(ev,f"为避免频繁使用刷屏，只能群管理员使用哦~",at_sender = True)
        return
    await bot.send(ev,message = '正在生成本群今日词云，请耐心等待',at_sender = True)
    makeclouds(gid)
    today = datetime.date.today().__format__('%Y-%m-%d')
    await bot.send(ev,MessageSegment.image(f'file:///{load_in_path}//{today}-{gid}.png'))


@sv.on_fullmatch('生成昨日词云')
async def getciyunb(bot, ev: CQEvent):
    gid = ev['group_id']
    if not hoshino.priv.check_priv(ev, hoshino.priv.ADMIN):
        await bot.send(ev,f"为避免频繁使用刷屏，只能群管理员使用哦~",at_sender = True)
        return
    await bot.send(ev,message = '正在生成本群昨日词云，请耐心等待',at_sender = True)
    makecloudsb(gid)
    yesterday = (datetime.date.today() + datetime.timedelta(-1)).__format__('%Y-%m-%d')
    await bot.send(ev,MessageSegment.image(f'file:///{load_in_path}//{yesterday}-{gid}.png'))

def countFile(dir):
    tmp = 0
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, item)):
            tmp += 1
        else:
            tmp += countFile(os.path.join(dir, item))
    return tmp

@sv.on_fullmatch('检查词云')
async def checkwordcloud(bot, ev: CQEvent):
    image_api = await bot.can_send_image()
    image_check = image_api.get('yes')
    image_all_num = countFile(str(load_in_path))
    fnnum = image_all_num - 2
    text = f"【发送权限检查】：\n是否能发送图片:{image_check}\n当前已生成的词云图片数:{fnnum}\n词云背景图片："
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, '权限不足。')
        return
    else:
        await bot.send(ev, text)
        await bot.send(ev, MessageSegment.image(f'file:///{wd_img}'))

@sv.on_fullmatch(['清除词云','清理词云'])
async def del_wordcloud(bot, ev: CQEvent):
    image_all_num = countFile(str(load_in_path))
    fnnum = image_all_num - 2
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, '权限不足。')
        return
    else:
        if not fnnum == 0:
            del_files(load_in_path)
            await bot.send(ev, "词云图片清除成功！")
        else:
            await bot.send(ev, "无需清理")