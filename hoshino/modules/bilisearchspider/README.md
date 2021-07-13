# SoungBot
***
## B站动态
**默认文件夹名：bilisearchspider**
**默认功能名：B站爬虫**
**目录组成如下：**
> modules
>> **bilidynamicpush**
>>> bilisearchspider.py  #主要运行文件
>>> README.md  #说明文件

### 功能介绍

这是B站视频搜索引擎的爬虫。在设定好爬取关键词后，每隔5分钟机器人会把这几分钟里以这些关键词搜索出来的新发布的视频推送到QQ群中。推送的内容包括：视频封面、视频标题、up主名字、链接。

这个插件主要是为了**会战**而生，比如如果设定关键词为“狮子座公会战”，那么会战期间所有在B站发布的轴都会推送到QQ群里。此外，也可以设置一些其他的关键词供娱乐使用。

需要注意的是，由于B站搜索引擎的特点，设定单一关键词“狮子座公会战”并不能把所有相关视频都搜出来。比如起名“狮子座工会战B2130W轴”的视频就没法靠这个关键词搜出来。这时需要再添加另一个关键词“狮子座会战”。插件支持任意多的关键词，这些关键词搜索出视频的并集会被推送到群里。

特别地，如果设置的关键词是up主名字，使用这个插件等价于自动收到这个up主新投稿的提醒。

只要存在关键词爬虫就会自动启动，如果想停用请使用指令把关键词**全删掉**。

### 指令

- **`[添加B站爬虫 关键词]`** 添加爬取关键词。每次添加一个，可添加多次
- **`[查看B站爬虫]`**  查看当前爬取关键词列表
- **`[删除B站爬虫 关键词]`** 删除指定爬取关键词

### 可自定义内容

在 **[bilisearchspider.py](hoshino/modules/bilidynamicpush/push.py)** 文件的第 **15-23** 行可以自行设置此功能的权限

```python
sv = Service(
    name = 'B站爬虫',  #功能名
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

此功能原作者：**[GWYOG](https://github.com/GWYOG)**
[原项目地址]https://github.com/GWYOG/GWYOG-Hoshino-plugins#3-b%E7%AB%99%E6%90%9C%E7%B4%A2%E7%88%AC%E8%99%ABbilisearchspider)
