# SoungBot
***
## 智能闲聊
**默认文件夹名：aichat**
**默认服务名：智能闲聊**
**目录组成如下：**
> modules
>> **aichat**
>>> aichat.py  #主要运行文件
>>> ai_config.json  #配置文件
>>> README.md  #说明文件

### 功能介绍

利用 [腾讯智能闲聊接口](https://ai.qq.com/) 让bot具有聊天功能

~~AI很蠢，经常不说人话~~

需要 **@bot** ，且概率性抽风

### 指令
本身无主动指令
- **`[启用 智能闲聊]`** 打开服务（默认禁用）
- **`[禁用 智能闲聊]`** 关闭服务
- **`[帮助智能闲聊]`** 查看详情

### 可自定义内容

在 **[aichat.py](hoshino/modules/aichat/aichat.py)** 文件的第 **31-39** 行可以自行设置此功能的权限

```python
sv = Service(
    name = '智能闲聊',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #服务名是否可见
    enable_on_default = False, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )
```

在 **[aichat.py](hoshino/modules/aichat/aichat.py)** 文件的第 **51-55** 行可以自行添加无法获取回复时的表达

```python
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～',
    '唔……等会再告诉你'
)
```

在 **[aichat.py](hoshino/modules/aichat/aichat.py)** 文件的第 **58-59** 行需提供所申请的API

```python
app_id = hoshino.config.tenxun_api_ID
app_key = hoshino.config.tenxun_api_KEY
```

- 也可以不在此处填写API，而是在统一配置文件夹的 [\_bot_.py](hoshino/config/__bot__.py)里填写。**（推荐）**

在 **[ai_config.json](hoshino/modules/aichat/ai_config.json)** 文件里添加启用的群号 **（一般无需改动）**

```json
{
 "open_groups": [
     123456,7890
 ]
}
```

### 其它

无额外说明。

### 鸣谢

此功能原作者：**[Watanabe-Asa](https://github.com/Watanabe-Asa?tab=repositories)**
[原项目地址](https://github.com/pcrbot/Hoshino-plugin-transplant#%E4%BA%BA%E5%B7%A5%E6%99%BA%E9%9A%9C)