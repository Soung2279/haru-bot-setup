Haru-Bot-Setup
===========================
#### 原项目地址：[haru-bot-setup](https://github.com/Soung2279/haru-bot-setup/)

#### 更新日志

##### 2022/7/12  v2.0 >>> v3.0 (python 3.9 x64/HoshinoBot V2)  恢复更新。此次更新有较大改动，HaruBot V3 已进行全面客制化，与原 V2 版本不兼容，请根据 [V2-V3升级向导](https://github.com/Soung2279) 进行版本迭代。

##### 2022/5/15  v1.5.8 >>> v2.0  因本人学业繁忙，暂时宣布跑路，更新与维护无限期延迟。

##### 2021/9/21  v1.5.7 >>> v1.5.8

新增：[百度一下](https://github.com/Soung2279/baidu_search)，[vtuber查询功能](https://github.com/Soung2279/vdb_list)

##### 2021/9/17  v1.5.6 >>> v1.5.7

新增七海娜娜米语音

##### 2021/9/17  v1.5.5 >>> v1.5.6

修复词云，新增人生重来

##### 2021/9/10  v1.5 >>> v1.5.5

更新插件，修复依赖文件不完整的问题(使用了pipreqs导出项目依赖)

更新README, 删除了错误的描述

更新资源包

##### 2021/8/27  v1.0 >>> v1.5

新增&更新多个插件并做Haru适配（魔改），增加hoshino原生语音调用支持

目前遗留问题：requirements.txt不完整，部分依赖缺失

##### 2021/8/15  v0.start_up >>> v1.0

更新musedashwiki

计划更新：全局自定义回复语，更生动 ~~moe~~ 的语言库

****

HoshinoBot-Harubot是基于[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)的**娱乐型QQ机器人**

~~因本人已从 pcr AFK，且日常使用会战功能频率不高~~。故本bot**未搭载**任何会战相关的功能。但本bot仍可与[yobot](http://yobot.win/)兼容。

![1_看图王.png](https://i.loli.net/2021/07/14/OkYsCXeq4vpbEZP.png "harubot")

目前，harubot仍使用`python 3.8.5+`环境和`nonebot1`运行

与市面上大多数HoshinoBot及其衍生不同的是，harubot具有以下独特的功能。
- [x] **（伪）全局消息合并转发**
- [x] **（伪）全局消息定时撤回**
- [x] **原生Hoshino的语音调用支持**
- [x] 风格统一，完善的指令说明
- [x] 统一文件配置参数
- [ ] 自定义适配的功能模块（逐步魔改中）
- [ ] 汇总统一自定义bot菜单提示信息
- [ ] ……

**感谢[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)项目 ，[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)项目和 众多[bot插件](https://github.com/pcrbot) 的开发者们！**

**本README具有时效性，请注意。**

**本项目正处于频繁快速的更新迭代中，README可能更新不及时**

****
#### Author:Soung2279
#### E-mail:Hirasawasu@foxmail.com

##### 如果您已经搭建bot，可直接查看harubot的 _全局消息合并转发，全局消息定时撤回_ 功能并适配到您自己的bot上。
##### [点击传送](#修改功能模块)
****
## 目录
* [前期准备](#前期准备)
* [功能介绍](#功能介绍)
* [安装](#安装go-cqhttp)
    * 安装go-cqhttp
    * 安装依赖
    * 配置_bot_.py文件
    * 设置端口与通信方式
    * 试运行
    * 完成
* [维护](#维护)
    * 修改功能模块
    * 添加新的功能模块
* [自定义](#自定义) 
* [其它](#其它)
* [Q&A](#Q&A)
* [鸣谢](#鸣谢)

---
### 前期准备

**仅提供Windows系统的部署指南。**

> 此处部署步骤可参考[我的另一篇部署指南](https://github.com/Soung2279/Mirai-Bot-Setup)，~~该篇指南已失效，但前期部署的准备步骤是相通的。~~

- 准备一台Windows系统的服务器（或个人本地电脑）

- 登录服务器控制台，在防火墙/安全组等界面，放通**80，8080，8090**端口
> 以腾讯云为例：  
  在 云服务器 - 安全组 - 安全组规则 里 添加 入站与出站规则

> 以阿里云为例：  
  在 云服务器 - 防火墙 里 添加规则

> 以本地个人电脑为例：（Windows 10）  
  在 控制面板 - 系统和安全 - Windows Defender 防火墙 - 高级设置 里 添加 入站规则 与 出站规则  
  建议在用服务器搭建前，先尝试运行在本地个人电脑上。

- 在任意位置打开任意一个文件夹，点击左上方的`查看`-`显示/隐藏`页面中，勾选`文件扩展名`

- （可选）使用Bot 的QQ号登录网页[QQ安全中心](https://aq.qq.com/cn2/index)并保持登录。或使用常用QQ（小号）作为bot。~~(即使不执行此步骤，Bot 仍然可正常搭建运行，但部分群聊消息可能会被tx吞，且异地登录有冻结风险)~~

#### Windows 10 部署

1. 安装下列软件/工具

    - Python ：https://www.python.org/downloads/windows/
    - Git ：https://git-scm.com/download/win
    - Notepad++ ：https://notepad-plus-plus.org/downloads/

    > 国内网络可能访问缓慢，这里提供已整合好的压缩文件 (**2020/9/14**）
    > ~~百度网盘：**[安装资源整合包](https://pan.baidu.com/s/1HwD-Z0f7msXKXLR0_Bec9Q)**~~
    > ~~提取码：***4396***~~  **注意：资源包仍可下载，但不保证其中的文件适配当前版本bot（好像我也没更过新啥的，应该能用。）**  
    > 以上软件/工具可在整合包里的**backups/software**里找到

2. 在合适的文件目录`新建文件夹`并双击打开，点击文件夹左上角的 `文件 -> 打开Windows Powershell`，输入以下命令

    ```powershell
    git clone https://github.com/Soung2279/haru-bot-setup.git
    ```

    或者直接下载本分支文件[Haru-Bot-Setup-master.zip](https://github.com/Soung2279/haru-bot-setup/archive/refs/heads/master.zip)


3. 在合适的文件目录新建文件夹，建议重命名为`Resources` 
    将收集到的 图片/语音资源 放入该文件夹，注意文件目录结构
    ```
    应当具有以下路径（Windows环境下）
    X:\Resources
    X:\Resources\img        总的图片资源
    X:\Resources\explorion   爆裂魔法语音（历史遗留问题单独存放）
    X:\Resources\record   总的语音文件
    ......
    ```
    **推荐**使用本人已经打包好的资源包。
    
    > 百度网盘：**[harubot资源2021-9-10.zip](https://pan.baidu.com/s/1JEJcbA4igbeqJzWnpUxuPQ)**
    > 提取码：***2279*** 
    > 约3个G，包含了当前Harubot运行所需的所有资源文件。
    > 已含本人自用setu库
    
    （Windows环境下）如果使用资源包，建议解压到 `C://Resources` 

 ---   
### 功能介绍

根据本指南部署的bot默认搭载以下模块：

##### 太长不看版：

`B站爬虫`, `Arcaea查询`, `服务器检查`, `大司马发病评论`, `命运2`, `原神相关`, `网抑云`, `表情包生成`, `谜语人翻译`, `pcr小游戏`, `在线涩图`, `本地涩图`, `识别图片`等

##### 完整：

```python
# 启用的模块
MODULES_ON = {
    '300hero', #300英雄出租查询
    '5000choyen', #5000兆元（红白字）图片生成器
    'advance_check', #服务器增强自检
    'aichat', #腾讯智能闲聊（新）
    'aircon', #群空调
    #'anticoncurrency', #反并发
    'arcaea', #Arcaea查询
    'asill', #A-SOUL发病小作文
    'bandori', #邦邦车站
    'bh3_calendar', #崩坏3日历
    #'bilidynamicpush', #B站动态
    #'bilisearchspider', #B站爬虫
    #'botchat', #语言库
    'botmanage', #bot功能性管理
    'cp', #土味情话
    'check', #服务器自检
    #'CQTwitter', #推特推送
    'dasima', #大司马发病评论
    #'destiny2', #命运2
    'dice', #骰子
    'emergeface', #换脸
    #'epixiv', #pixiv搜图
    'eqa', #问答
    'explosion', #爆裂魔法
    'falali', #-------------------
    'fishf14', #ff14钓鱼
    'flac', #无损音乐
    'functions', #小功能合集
    'generator', #文章生成器
    'Genshin', #原神相关
    'groupmaster', #bot群功能相关
    'guaihua', #涩涩的翻译
    'hedao', #合刀计算
    'hiumsentences', #网抑云
    'holiday', #假期查询
    #'horsenews', #赛马娘新闻
    #'hourcall', #整点时报
    'image_generate', #表情包生成
    'KFCgenshin', #原神二刺螈语音
    'maimaiDX', #maimaiDX查询
    'majsoul', #雀魂查询
    'mem_birthday', #群友生日提醒
    'memberguess', #猜群友
    #'mikan', #蜜柑推送
    'musedash', #MuseDash百科
    'music', #点歌
    'nbnhhsh', #谜语人翻译
    'nmsl', #抽象话转换
    'nowtime', #锁屏报时
    #'pcr_calendar', #pcr日历
    #'pcrbirth', #pcr生日提醒
    'pcrmemorygames', #pcr记忆游戏
    #'pcrmiddaymusic', #pcr午间音乐
    #'pcrsealkiller', #pcr海报杀手
    #'pcrwarn', #pcr定时提醒
    'picfinder_take', #搜图
    'pokemanpcr', #pcr戳一戳
    'portune', #pcr运势
    'priconne', #pcr小游戏相关
    'pulipuli', #反bilibili小程序
    #'r6_anti_hacker', #---------------------
    'revgif', #倒放gif
    'setu', #本地涩图
    'setu_renew', #在线涩图
    'shaojo', #今天是什么少女
    #'snitchgenerator', #Nokia内鬼图
    'steam', #steam查询
    'tarot', #塔罗牌占卜
    'tracemoe', #识别番剧截图
    'translate', #翻译
    'voiceguess', #猜语音
    'weather', #天气查询
    'whattoeat', #今天吃什么
    #'wordcloud', #词云
    'zhihu', #知乎日报
    #'test',
}
```

---
### 安装

#### 安装go-cqhttp

**访问go-cqhttp的[releases](https://github.com/Mrs4s/go-cqhttp/releases)**，找到v1.0.0-beta4下的Assets里**go-cqhttp_windows_amd64.exe**，点击下载。（**推荐**）

或直接使用网盘资源

> 百度网盘：**[go-cqhttp.exe](https://pan.baidu.com/s/1j9eTz94fNphHN6rnn_EeNg)**
> 提取码：***2279***  

同时，下载ffmpeg放到go-cqhttp目录。

> 百度网盘：**[ffmpeg](https://pan.baidu.com/s/1pYKN_-8O7k5rlwXoHGriSg)**
> 提取码：***2279***

之后运行一次go-cqhttp.exe，弹出窗口即可，关闭窗口，**稍后进行配置**。

#### 安装依赖

在`X:\haru-bot-setup-master\`目录下~~或者你自己放置的bot目录~~，点击文件夹左上角的 `文件 -> 打开Windows Powershell`，输入以下命令

```python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
或者直接运行`双击安装依赖.bat`，若此过程中有报错信息，请重新运行一次，若仍有报错，请复制报错信息到搜索引擎获得帮助

#### 配置_bot_.py文件

**修改以下文件的配置**

`hoshino/config/_bot_.py`
```python
PORT = 8090  # 建议设置为8090
HOST = '127.0.0.1'      # 本地部署使用此条配置

SUPERUSERS = [2279134404]    # 填写超级用户（你）的QQ号，
NICKNAME = ('小晴','野中晴','haru','@756160433')  #  设置机器人的呢称，呼叫昵称等同于@bot，请使用 ``元组 tuple`` 进行配置

# 资源库文件夹，需可读可写，windows下注意反斜杠转义，注意最后一根斜杠
RES_DIR = r'C:/Resources/'

lolicon_api = ''  # 填写api（因Lolicon更新，无需使用apikey，可不填）
acggov_api = ''  # 填写api
saucenao_api = ''  # 填写api
aichat_ID = ''  # 填写api
aichat_KEY = ''  # 填写api


FORWARD_MSG_EXCHANGE = 1  #全局消息转发。1为启用，0为禁用
FORWARD_MSG_NAME = 'bot主人：2279134404'  #转发消息显示的呢称
FORWARD_MSG_UID = 756160433  #转发消息使用的qq画像（头像）

RECALL_MSG_SET = 1  #全局定时撤回，1为启用，0为禁用，推荐启用规避风控
RECALL_MSG_TIME = 30  #撤回等待时长(单位s)

```

关于API，可参考：

[ACG-GOV](https://acg-gov.com/)

[Lolicon](https://lolicon.app/)

[腾讯AI开放平台](https://ai.qq.com)

[SauceNAO识别图片](https://saucenao.com/index.php)的API[申请](https://saucenao.com/user.php)

#### 设置端口与通信方式

请参考[go-cqhttp 帮助中心](https://docs.go-cqhttp.org/guide/quick_start.html#%E4%BD%BF%E7%94%A8)

在go-cqhttp目录中的**config.yml**文件中进行配置

```yaml
account: # 账号相关
  uin: 1233456 # QQ账号
  password: '' # 密码为空时使用扫码登录

servers:
  - ws-reverse:
      # 是否禁用当前反向WS服务
      disabled: false
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://127.0.0.1:8090/ws/
      # 反向WS API 地址
      api: ws://your_websocket_api.server
      # 反向WS Event 地址
      event: ws://your_websocket_event.server
      # 重连间隔 单位毫秒
      reconnect-interval: 3000
```

#### 试运行

在haru-bot-setup文件夹中，运行`双击运行HoshinoBot.bat`启动hoshinobot

在go-cqhttp文件夹中，使用cmd或powershell启动`go-cqhttp.exe` (直接双击启动也可)

若成功运行，窗口将出现如下结果：

- hoshinobot
```powershell
[2021-07-14 04:51:28,370 nonebot] INFO: Running on 127.0.0.1:8090
Running on http://127.0.0.1:8090 (CTRL + C to quit)
[2021-07-14 04:51:28,380 nonebot] INFO: Scheduler started
[2021-07-14 04:51:28,381] Running on http://127.0.0.1:8090 (CTRL + C to quit)
[2021-07-14 04:51:32,810] 127.0.0.1:4741 GET /ws/ 1.1 101 - 541
```
- go-cqhttp
```powershell
[2021-07-14 04:51:24] [INFO]: Protocol -> connect to server: 193.112.231.60:8080
[2021-07-14 04:51:27] [INFO]: 收到服务器地址更新通知, 将在下一次重连时应用.
[2021-07-14 04:51:31] [INFO]: 登录成功 欢迎使用: 野中晴
[2021-07-14 04:51:31] [INFO]: 开始加载好友列表...

[2021-07-14 04:51:32] [INFO]: 开始尝试连接到反向WebSocket Universal服务器: ws://127.0.0.1:8090/ws/
[2021-07-14 04:51:33] [INFO]: 检查更新完成. 当前已运行最新版本.
```

若该过程中hoshinobot窗口闪退，则请点击文件夹左上角的 `文件 -> 打开Windows Powershell`，输入以下命令
```python
py run.py
```

查看**红色报错信息。**（大多数时候是某依赖未安装。请复制粘贴报错信息到百度）

#### 完成

在未修改启用的模块前提下（即config.py里的**MODULES_ON**无变动）

在bot所在群聊中发送：

- @bot 自检

- @bot 进阶检查

- @bot 服务器检查

- @bot bot状态

若有回应，则说明bot已搭建完成。

此时请发送`lssv`来确认当前群启用的服务。

----
### 维护

#### 修改功能模块

为了实现 **全局消息合并转发** 和 **全局消息定时撤回**，bot的最终输出与原本hoshinobot有所不同。请看下面示范：

HoshinoBot原版
```python
@sv.on_fullmatch('老公')
async def chat_laogong(bot, ev):
    await bot.send(ev, '人不能，至少不应该', at_sender=True)

# 效果：当发送“老公”时，直接回复“人不能，至少不应该”
```

Harubot
```python
@sv.on_fullmatch('老公')
async def function_a(bot, ev):
    if forward_msg_exchange == 1:  # 合并判断
        data_all = []
        msg1 = '人不能，至少不应该'
        data1 = {
            "type": "node",
            "data": {
                "name": f"{forward_msg_name}",
                "uin": f"{forward_msg_uid}",
                "content": msg1
            }
        }
        if recall_msg_set == 1:  #撤回判断
            recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")
                
            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
    else:
        if recall_msg_set == 1:  #撤回判断
            recall_1 = await bot.send(ev, '人不能，至少不应该')
            notice = await bot.send(ev, f"将在{RECALL_MSG_TIME}s后将撤回消息")

            await asyncio.sleep(RECALL_MSG_TIME)

            await bot.delete_msg(message_id=recall_1['message_id'])
            await bot.delete_msg(message_id=notice['message_id'])
        else:
            await bot.send(ev, '人不能，至少不应该')
    
# 效果：当发送“老公”时，首先判断是否合并转发，其次判断是否撤回，最后回复“人不能，至少不应该”。
```

在原版中，回复将**直接原样输出**，而harubot中首先判断**是否合并转发**，若为是，先转换为合并消息，然后判断**是否撤回**。

但是，**并不是所有**的输出消息都需要转发，或者不适合用转发。依据此，harubot修改了**大部分长消息和可能有风险的消息**最终的输出判断，使其可以控制是否转发和撤回。但对于短消息，单图等不适合用的输出则未做改动。（~~所以是伪全局~~）

可以自行斟酌。若不需要此功能，请自行找到最终输出的地方进行还原。

```diff
+ await bot.send(ev, '人不能，至少不应该')
- if forward_msg_exchange == 1:
- if recall_msg_set == 1:
- recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
- …………
```
此外，有些插件自带转发和撤回功能（例如贵族决斗pcr_duel）。在harubot中对**贵族决斗**进行了适配处理，harubot的贵族决斗转发撤回设置受全局参数控制。

**全局参数设置位置：**
`hoshino/config/_bot_.py`

```python
# 全局配置相关
# - 是否启用全局消息合并转发（部分短消息不受影响）
### 本来是想做所有消息不论长短都可以设定转发的，但是要改的地方太多了（我懒）+有些消息很短根本没必要转发，所以这里控制的只有部分我认为需要用到转发的长消息或者图文=  =
### 有一些功能的转发不受此处控制，需单独设置，例如[本地色图]等。
FORWARD_MSG_EXCHANGE = 1  #1为启用，0为禁用，推荐启用规避风控
FORWARD_MSG_NAME = 'harubot'  #转发消息显示的呢称
FORWARD_MSG_UID = 123456  #转发消息使用的qq画像（头像）
# - 是否启用全局风险消息（带大量数字消息，带敏感信息消息，部分图片等）撤回，1为启用，0为禁用[此处不控制本地涩图"setu"的撤回，"setu"的撤回需单独设置]
### 本来是想做所有消息不论长短都可以定时撤回的，但是要改的地方太多了（我懒）+有些消息例如帮助指令信息没必要撤回，还有考虑到消息合并和撤回要配合一起使用。所以这里控制的只有部分我认为需要用到撤回的长消息或者图文=  =
### 有一些功能的撤回不受此处控制，需单独设置，例如[本地色图]等。
RECALL_MSG_SET = 1  #1为启用，0为禁用，推荐启用规避风控
RECALL_MSG_TIME = 30  #撤回等待时长(单位s)
```

#### 添加新的功能模块

**harubot**本质是HoshinoBot的魔改版，所以适用于HoshinoBot的插件均可以在harubot上使用。

若是需要引入 **全局消息合并转发** 和 **全局消息定时撤回**，则需要对新装插件进行修改。

首先需引入参数
```python
import asyncio  #撤回用
import hoshino
from hoshino import config #读取配置文件
```

在bot最终输出的地方添加
```diff
- await bot.send(ev, '人不能，至少不应该')
+ if forward_msg_exchange == 1:
+ if recall_msg_set == 1:
+ recall = await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data_all)
+ …………
```
bot最终输出的地方可以简单通过查找`bot.send`,`bot.finish`等查看。具体请参考[消息触发器](https://github.com/pcrbot/hoshinobot-development-documentation/blob/master/trigger.md)

**完整**的添加代码可在模板文件`hoshino/modules/_example_/_example_.py`中查看。


======
如果需要使用增强的**原生Hoshino语音调用**功能，请将您的语音文件放置在 ``资源库文件夹/record/`` 路径下，资源库文件夹填写位置：``hoshino/config/_bot_.py`` 的 ``RES_DIR``

以下是一个简单例子：

```python
import hoshino
from hoshino import R

xxx = R.rec(xxx/xxx.mp3).cqcode
...
await bot.send(ev, xxx)
```

具体可前往 [HoshinoBot功能性增强-语音调用支持](Https://github.com/Soung2279/advance_R)


======
在 Harubot 中，部分地方使用 “NICKNAME[0]” 来获取bot呢称，若您的bot呢称数据结构不为 元组 或 字典，则可能导致无法调用，请自行于 ``hoshino/config/_bot_.py`` 修改 ``NICKNAME`` 为元组形式。

以下是一个简单例子：

```python
NICKNAME = ('小晴','野中晴','haru','@756160433')          # 机器人的昵称。呼叫昵称等同于@bot，可用元组配置多个昵称
```

---
### 自定义

- 若Bot 运行正常，可考虑开启更多模块以丰富bot的功能。

- 在 `HoshinoBot/hoshino/config/_bot_.py` 文件里，将需要开启的模块前面的"`#井号`"删除。

- 若想给Bot 添加更多功能，可以自行收集插件放入 `HoshinoBot/hoshino/modules` 文件夹中。（请仔细阅读该插件的说明文档，某些插件的添加方式有所不同）

- 若Bot 添加群过多，需要引入授权系统，请启用[authMS](https://github.com/pcrbot/authMS)插件。

**参考[HoshinoBot(v2) 插件开发指南（社区版）](https://github.com/pcrbot/hoshinobot-development-documentation)**

---
### 其它

harubot的孪生bot：
[早坂爱bot](http://wpa.qq.com/msgrd?v=3&uin=2143512954&site=qq&menu=yes)，[惠惠bot](http://wpa.qq.com/msgrd?v=3&uin=3403478643&site=qq&menu=yes)，[贝拉bot](http://wpa.qq.com/msgrd?v=3&uin=3207117254&site=qq&menu=yes)
~~均已停用~~

~~harubot目前正在招收试用人群，可在q群1121815503向群主申请免费试用。~~

**made by Soung2279**

---
### Q&A

##### Q：为什么我的Bot 发不出图片/语音？
##### A：请检查资源路径`RES_DIR`是否设置正确，目录`Resources`下该图片/语音是否存在  

##### Q：为什么我的Bot 没有反应？
##### A：请查看窗口显示的日志。  
- ###### 若日志显示正常，请查看在[**准备工作**]()步骤中是否放通端口。
- ###### 若日志有报错信息，请复制报错信息到搜索引擎解决。
- ###### 若日志无反应，请在该窗口输入回车`(按下Enter键)`，查看日志是否有反应。若日志仍无反应，请查看配置文件是否正确配置
- ###### 若端口已经放通，请尝试其它指令；若部分指令有回应，说明bot 正常运行中，只是部分消息被tx吞了。若所有指令都无回应，请重新运行`双击安装依赖`
- ###### 若所有方式都无法让Bot 做出反应，请尝试重新部署Bot。

##### Q：Bot 的权限是怎么设定的？
- ##### A：基于HoshinoBot的功能，设定主人为**最高**权限`priv.SUPERUSER`，群主为仅次于主人的第二权限`priv.OWNER`，群管理为更次一等的权限`priv.ADMIN`，群员为最低权限`priv.NORMAL`。(黑/白名单不考虑在内) 可以在`_bot_.py`里设定多个主人 

##### Q：以后的更新维护？
##### A：您可以自行访问[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)项目 ，[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)项目和众多[bot插件](https://github.com/pcrbot) 来进行更新。

##### Q：还有什么注意事项？
##### A：请勿滥用Bot。

---

### 鸣谢

#### 骨干部分

**HoshinoBot**：https://github.com/Ice-Cirno/HoshinoBot  作者：[@Ice-Cirno](https://github.com/Ice-Cirno)

**go-cqhttp**：https://github.com/Mrs4s/go-cqhttp  作者：[@Mrs4s](https://github.com/Mrs4s/)

#### 插件部分

- [Dihe Chen](https://github.com/Chendihe4975)  

- [var](https://github.com/var-mixer)  

- [xhl6699](https://github.com/xhl6666)  

- [Watanabe-Asa](https://github.com/Watanabe-Asa)  

- [-LAN-](https://github.com/laipz8200)  

- [Cappuccilo](https://github.com/Cappuccilo)  

- [yuyumoko](https://github.com/yuyumoko)  

- [H-K-Y](https://github.com/H-K-Y)  

- [ZhouYuan](https://github.com/zyujs)  
...

#### 资源部分

**干炸里脊资源站**: https://redive.estertion.win/

**Pcrbot - pcrbot相关仓库**: https://www.pcrbot.com/

---
#####   本项目基于[GNU通用公共授权3.0](http://www.gnu.org/licenses/) 开源
