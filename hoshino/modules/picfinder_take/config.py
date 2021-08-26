import hoshino
from hoshino import config

threshold =70      # SauceNAO相似度阈值，低于该相似度自动追加ascii2d搜索

SAUCENAO_KEY = config.saucenao_api     # SauceNAO 的 API key

SAUCENAO_RESULT_NUM = 4      # SauceNAO搜索结果显示数量

ASCII_RESULT_NUM = 4      # ascii2d搜索结果显示数量

SEARCH_TIMEOUT = 60      # 连续搜索模式超时时长

DAILY_LIMIT = 10      # 搜图每日限额

CHAIN_REPLY = True      # 是否启用合并转发回复模式

THUMB_ON = True      # 是否启用缩略图

CHECK = True      # 是否开启手机截屏判定

HOST_CUSTOM = {
                  # 自定义Host，不使用留空即可
                  # 格式示例：'https://ascii2d.net' , 'http://localhost:12345'   
                  'SAUCENAO': '',
                  'ASCII': ''
              }

proxies={ 
               'http':'',
               'https':''
              }        # 网络代理

helptext='''
- [@bot+图片] 单张/多张搜图
- [@bot识图] 进入批量识图模式，可直接回复要搜的图片
- [谢谢@bot] 退出批量识图模式
- [私聊 +图片] 私聊识图
'''.strip()
