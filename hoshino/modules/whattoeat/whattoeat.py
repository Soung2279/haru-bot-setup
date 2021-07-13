import hoshino, random, os, re, filetype
from hoshino import Service, R, priv, aiorequests
from hoshino.config import RES_DIR
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter

sv_help = '''
- [今天吃什么]  看看今天吃啥
- [添加菜品+图片]  加菜
'''.strip()

sv = Service(
    name = '今天吃什么',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = True, #默认启用
    bundle = '娱乐', #分组归类
    help_ = sv_help #帮助说明
    )

_lmt = DailyNumberLimiter(5)
imgpath = os.path.join(os.path.expanduser(RES_DIR), 'img', 'foods')

@sv.on_rex(r'^(今天|[早中午晚][上饭餐午]|夜宵)吃(什么|啥|点啥)')
async def net_ease_cloud_word(bot,ev:CQEvent):
    uid = ev.user_id
    if not _lmt.check(uid):
        await bot.finish(ev, '你今天吃的已经够多的了！', at_sender=True)
    match = ev['match']
    time = match.group(1).strip()
    food = random.choice(os.listdir(imgpath))
    name = food.split('.')
    to_eat = f'{time}去吃{name[0]}吧~\n'
    try:
        foodimg = R.img(f'foods/{food}').cqcode
        to_eat += str(foodimg)
    except Exception as e:
        hoshino.logger.error(f'读取食物图片时发生错误{type(e)}')
    await bot.send(ev, to_eat, at_sender=True)
    _lmt.increase(uid)

async def download_async(url: str, name: str):
    resp= await aiorequests.get(url, stream=True)
    if resp.status_code == 404:
        raise ValueError('文件不存在')
    content = await resp.content
    try:
        extension = filetype.guess_mime(content).split('/')[1]
    except:
        raise ValueError('不是有效文件类型')
    abs_path = os.path.join(imgpath, f'{name}.{extension}')
    with open(abs_path, 'wb') as f:
        f.write(content)

@sv.on_prefix(('添菜','添加菜品'))
@sv.on_suffix(('添菜','添加菜品'))
async def add_food(bot,ev:CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        return
    food = ev.message.extract_plain_text().strip()
    ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(ev.message))
    if not ret:
        await bot.send(ev,'请附带美食图片~')
        return
    url = ret.group(2)
    await download_async(url, food)
    await bot.send(ev,'食谱已增加~')
