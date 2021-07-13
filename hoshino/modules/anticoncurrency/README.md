# SoungBot
***
## 反并发
**默认文件夹名：anticoncurrency**
**默认功能名：反并发**
**目录组成如下：**
> modules
>> **anticoncurrency**
>>> \__init__.py  #函数运行
>>> anti_concurrency.py  #指令处理
>>> README.md  #说明文件

### 功能介绍

在大群中使用多个不同的插件时容易出现非计划内的并发：比如群友A想玩猜角色、群友B想玩猜语音，他们不小心同时发送了指令，这时机器人会同时开始两个不同的游戏，而小游戏一般持续时间都比较长，这样会造成混乱。

**anticoncurrency插件**解决了这一问题。给插件设置好不想并发的指令后，只有当一个指令执行完毕，另一个指令才会被机器人接受并开始执行，否则会自动忽略。

从理论上来说，在设置好相关参数后，这个插件可以防止任何插件(哪怕被魔改过)的指令出现并发，适用范围很广。

### 指令
本身无主动指令
- **`[启用 反并发]`** 打开服务（默认禁用）
- **`[禁用 反并发]`** 关闭服务
- **`[帮助反并发]`** 查看详情

### 可自定义内容

在 **[anti_concurrency.py](hoshino/modules/anticoncurrency/anti_concurrency.py)** 文件的第 **17** 行可以自行添加指令

```python
ANTI_CONCURRENCY_GROUPS = [['猜头像', '猜角色', 'cygames','猜群友','猜语音','完美配对','神经衰弱']]
```

在 **[anti_concurrency.py](hoshino/modules/anticoncurrency/anti_concurrency.py)** 文件的第 **29-37** 行可以自行设置此功能的权限

```python
sv = Service(
    name = '反并发',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.SUPERUSER, #管理权限
    visible = False, #服务名是否可见
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )
```

### 其它

无额外说明。

### 鸣谢

此功能原作者：**[GWYOG](https://github.com/GWYOG/)**
[原项目地址](https://github.com/GWYOG/GWYOG-Hoshino-plugins#7-%E5%8F%8D%E5%B9%B6%E5%8F%91%E6%8F%92%E4%BB%B6anticoncurrency)