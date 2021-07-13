# SoungBot
***
## B站动态
**默认文件夹名：bilidynamicpush**
**默认功能名：B站动态**
**目录组成如下：**
> modules
>> **bilidynamicpush**
>>> push.py  #主要运行文件
>>> config.json  #配置文件
>>> README.md  #说明文件

### 功能介绍

一个用于推送哔哩哔哩动态的HoshinoBot插件,支持动态、视频、文章的推送（含图片），支持将6、9宫格图片自动合成单张图片。

### 指令

- **`[订阅动态+空格+需要订阅的UID]`** 订阅动态
- **`[取消订阅动态+空格+需要取消订阅的UID]`** 取消订阅
- **`[重新载入动态推送配置]`** 重载刷新配置文件
- **`[常用UID一览]`** 查看内置的常用UID

### 可自定义内容

在 **[push.py](hoshino/modules/bilidynamicpush/push.py)** 文件的第 **27-35** 行可以自行设置此功能的权限

```python
sv = Service(
    name = 'B站动态',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = False, #是否默认启用
    bundle = '订阅', #属于哪一类
    help_ = sv_help #帮助文本
    )
```

在 **[config.json](hoshino/modules/bilidynamicpush/config.json)** 文件的第 **4-9** 行添加启用的群和订阅的UID
~~也可以自行在群内通过指令一个一个添加~~

```json
        "34763008": [  #这一行是UID
            "1028088241",  #这一行是群号
            "490578923"
        ],
        "UID": [
            "群号"
```

### 其它

无额外说明。

### 鸣谢

此功能原作者：**[Sora233](https://github.com/Sora233)**
[原项目地址](https://github.com/Sora233/bilidynamicpush)
