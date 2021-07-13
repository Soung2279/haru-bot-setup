"""这是一份实例配置文件

将其修改为你需要的配置，并将文件夹config_example重命名为config
"""

# hoshino监听的端口与ip
PORT = 8090
HOST = '127.0.0.1'      # 本地部署使用此条配置（QQ客户端和bot端运行在同一台计算机）
# HOST = '0.0.0.0'      # 开放公网访问使用此条配置（不安全）

DEBUG = False           # 调试模式

WHITE_LIST = []      #白名单用户
SUPERUSERS = [123456789]    # 填写超级用户的QQ号，可填多个用半角逗号","隔开
NICKNAME = r'小晴|野中晴|haru|at,qq=756160433'          # 机器人的昵称。呼叫昵称等同于@bot，可用元组配置多个昵称

#不需要改动
COMMAND_START = {''}
COMMAND_SEP = set()

# 发送图片的协议。可选 http, file, base64
RES_PROTOCOL = 'file'
# 资源库文件夹，需可读可写，windows下注意反斜杠转义
RES_DIR = r'C:/Resources/'
# 使用http协议时需填写，原则上该url应指向RES_DIR目录
RES_URL = 'http://127.0.0.1:5000/static/'

# 需要用到的API
# - 涩图相关
lolicon_api = ''
acggov_api = ''

# - 搜图相关
shitu_api = ''
pixiv_id = ''
pixiv_password = ''

#【Error】因API失效，已弃用
aichat_api_ID = ''
aichat_api_KEY = ''


# 启用的模块
MODULES_ON = {
    'advance_check',
    #'aichat', #腾讯智能闲聊
    'aircon', #群空调
    #'anticoncurrency', #反并发
    'arcaea', #Arcaea查询
    'bandori', #邦邦车站
    'bilidynamicpush', #B站动态
    'bilisearchspider', #B站爬虫
    'botchat', #语言库
    'botmanage', #bot功能性管理
    'check', #服务器自检
    'CQTwitter', #推特推送
    'dasima', #大司马发病评论
    'destiny2', #命运2
    'dice', #骰子
    'emergeface', #换脸
    #'epixiv', #pixiv搜图
    'eqa', #问答
    'explosion', #爆裂魔法
    'fishf14', #ff14钓鱼
    'flac', #无损音乐
    'functions', #小功能合集
    'generator', #文章生成器
    'Genshin', #原神相关
    'groupmaster', #bot群功能相关
    'guaihua', #涩涩的翻译
    'hedao', #合刀计算
    'hiumsentences', #网抑云
    'horsenews', #赛马娘新闻
    'hourcall', #整点时报
    'image_generate', #表情包生成
    'KFCgenshin', #原神二刺螈语音
    'majsoul', #雀魂查询
    'memberguess', #猜群友
    'mikan', #蜜柑推送
    'music', #点歌
    'nbnhhsh', #谜语人翻译
    'nmsl', #抽象话转换
    'nowtime', #锁屏报时
    'pcr_calendar', #pcr日历
    'pcrbirth', #pcr生日提醒
    'pcrmemorygames', #pcr记忆游戏
    'pcrmiddaymusic', #pcr午间音乐
    'pcrsealkiller', #pcr海报杀手
    'pcrwarn', #pcr定时提醒
    'pokemanpcr', #pcr戳一戳
    'portune', #pcr运势
    'priconne', #pcr小游戏相关
    'pulipuli', #反bilibili小程序
    'revgif', #倒放gif
    'saucenao', #识别图片
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
    'wordcloud', #词云
    'zhihu' #知乎日报
}


# 全局配置相关
# - 是否启用全局消息合并转发（部分短消息不受影响）
### 本来是想做所有消息不论长短都可以设定转发的，但是要改的地方太多了（我懒）+有些消息很短根本没必要转发，所以这里控制的只有部分我认为需要用到转发的长消息或者图文=  =
### 有一些功能的转发不受此处控制，需单独设置，例如[本地色图]等。
FORWARD_MSG_EXCHANGE = 1  #1为启用，0为禁用，推荐启用规避风控
FORWARD_MSG_NAME = 'harubot'  #转发消息显示的呢称
FORWARD_MSG_UID = 123456  #转发消息使用的qq画像（头像）

'''提供如下官方UID：
-- 数据来源QQ官方机器人 --
Q群管家：2854196310
QQ官方：2854196320
QQ小店助手：2854196925
小冰：2854196306
Eva-创造恋人：2854205672
小世界情报菌：2854200454
小微欢乐多：2854196324
表情包老铁：2854196312
王者荣耀小狐狸：2854196311
看点直播小助理：2854215747
DNF小酱油：2854214473
英雄联盟 撸妹儿：2854209507
占卜师喵吉：2854196318
火影忍者-豚豚：2854211389
CODM-瘦普：2854214941
腾讯灯塔：2854200812
……
'''

# - 是否启用全局风险消息（带大量数字消息，带敏感信息消息，部分图片等）撤回，1为启用，0为禁用[此处不控制本地涩图"setu"的撤回，"setu"的撤回需单独设置]
### 本来是想做所有消息不论长短都可以定时撤回的，但是要改的地方太多了（我懒）+有些消息例如帮助指令信息没必要撤回，还有考虑到消息合并和撤回要配合一起使用。所以这里控制的只有部分我认为需要用到撤回的长消息或者图文=  =
### 有一些功能的撤回不受此处控制，需单独设置，例如[本地色图]等。
RECALL_MSG_SET = 1  #1为启用，0为禁用，推荐启用规避风控
RECALL_MSG_TIME = 30  #撤回等待时长(单位s)


# 自检信息相关
VERSION = '1.0.0'
GO_VERSION = 'go-cqhttp_1.0.0-beta4_windows_amd64'
PYTHON_VERSION = 'Python 3.8.5 64-bit'
LAST_UPDATE = 'time'