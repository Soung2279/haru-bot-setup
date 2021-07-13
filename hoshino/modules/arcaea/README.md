# SoungBot
***
## Arcaea查询
**默认文件夹名：arcaea**
**默认功能名：Arcaea查询**
**目录组成如下：**
> modules
>> **arcaea**
>>> arcaea.py  #指令处理
>>> arcaea_crawler.py  #函数运行
>>> README.md  #说明文件

### 功能介绍

关于音游Arcaea的相关查询。

### 指令

- **`[ds <曲名/等级>]`** 查询定数
- **`[arc <玩家名/好友码>]`** 查询玩家的ptt、r10/b30和最近游玩的歌曲
- **`[best <玩家名/好友码>]`** 查询玩家ptt前n的歌曲(best命令具有刷屏风险，大于10请尽量私聊查询)

### 可自定义内容

在 **[arcaea.py](hoshino/modules/arcaea/arcaea.py)** 文件的第 **18-26** 行可以自行设置此功能的权限

```python
sv = Service(
    name = 'Arcaea查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )
```

### 其它

无额外说明。

### 鸣谢

此功能原作者：**[Watanabe-Asa](https://github.com/Watanabe-Asa)**
[原项目地址](https://github.com/pcrbot/Hoshino-plugin-transplant#arcaea%E6%9F%A5%E8%AF%A2)