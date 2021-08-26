<p align="center">
  <a href="https://sm.ms/image/gptjxEmihya6nr4">
    <img src="https://i.loli.net/2021/08/14/gptjxEmihya6nr4.png" alt="musewiki">
  </a>
</p>

<div align="center">

MuseDashWiki
===========================
<div align="left">


→→ **[查看更新日志](#更新日志)**

### 功能介绍

适用于``Hoshinobot``的 **MuseDash Wiki插件**

~~不知道 MuseDash 是啥？ [喵斯快跑_百度百科](https://baike.baidu.com/item/%E5%96%B5%E6%96%AF%E5%BF%AB%E8%B7%91/57515152)；[MuseDash官网](http://www.peroperogames.com/)~~

搭载的功能有如下：
- **查询歌曲信息**，包括歌曲BPM，作者，时长等(数据来源[MuseDash官方英文Wiki](https://musedash.fandom.com/wiki/Muse_Dash_Wiki))，并支持模糊查询(输入查询的歌曲名时 若名字不对可以进行猜测 并提供正确的歌曲名，*改编自 Hoshinobot 原版的 chara*)
- **每日随机推荐歌曲**
- **角色语音试听**，包括触摸语音，受击语音等
- **peropero标题语音试听**  ~~peropero\~games\~~~
- **游戏demo试听**  ~~就是选歌界面播放的歌曲片段~~
- **游戏音效试听**  ~~各种游戏使用的音效，来源拆包数据~~
- **游戏资料查询**，包括分数公式，隐藏曲目，偏移值，表情包等
- **每日运势**  ~~简易实现的md版每日运势抽签~~
- **查询角色与精灵**  ~~muses and elfins~~
- **插图/动画/场景查询**  
- **单曲成就 or 游戏成就查询**
- ……

在以下环境下，插件已经过测试：
- [x] ``Windows 10``
- [x] ``Windows 11``
- [x] ``python 3.8.5 32&64bit``
- [x] ``python 3.8.9 32&64bit``
- [x] ``Hoshinobot V2.0``
- [ ] 理论上支持 ``nonebot 1.6.0+``，``python 3.9``

> 由于本人不熟悉Linux环境，且插件全程都是在Windows环境下编写的，在Linux上使用可能有bug，请见谅（理论上来说是没有的）

**不适用于 ``nonebot2`` ！** ~~（其实是不知道咋从nb1迁移到nb2）~~

### 插件安装

<details>
  <summary>通过github克隆</summary>

在**hoshino/modules**文件夹中，打开cmd或者powershell，输入以下代码按回车执行：

```powershell
git clone https://github.com/Soung2279/musewiki.git
```

之后关闭cmd或powershell，打开**hoshino/config**的`__bot__.py`文件，在**MODULES_ON** = {}里添加 ``musewiki``
```python
# 启用的模块
MODULES_ON = {
    'xxx',
    'xxx',
    'musewiki',  #注意英文逗号！
    'xxx',
}
```

之后将本文件夹中的 ``R.py`` 移动至 ``hoshino`` 路径下（覆盖原来的 R.py）

如果未在本文件夹下找到 ``R.py`` ，可前往 [HoshinoBot功能性增强-语音调用支持](https://github.com/Soung2279/advance_R)

</details>

<details>
  <summary>直接安装</summary>

直接下载本插件[musewiki](https://github.com/Soung2279/musewiki/archive/refs/heads/master.zip)，解压至**hoshino/modules**

之后打开**hoshino/config**的`__bot__.py`文件，在**MODULES_ON** = {}里添加advance_check
```python
# 启用的模块
MODULES_ON = {
    'xxx',
    'xxx',
    'advance_check',  #注意英文逗号！
    'xxx',
    'xxx',
}
```

之后将本文件夹中的 ``R.py`` 移动至 ``hoshino`` 路径下（覆盖原来的 R.py）

如果未在本文件夹下找到 ``R.py`` ，可前往 [HoshinoBot功能性增强-语音调用支持](https://github.com/Soung2279/advance_R)

</details>

插件安装完成后，可使用基本的**歌曲/角色/精灵查询**功能。但由于本插件使用了 大量图片/语音资源 ，需要进行资源包的补充。
<details>
  <summary>百度网盘</summary>
</details>

### 指令

##### 歌曲查询
- **详细查询+歌名**  详细查询单曲的各种信息，并发送对应的demo
- **随机歌曲信息**  随机查看一条歌曲信息
- **帮助百科歌曲推送**  配置每日的md歌曲推送
##### 角色语音查询
- **摸摸+角色皮肤名**  摸摸角色的头(。・・)ノ
- **打打+角色名**  打一下角色（好过分ヽ(*。>Д<)o゜）
- **随机角色语音**  随便听一句
##### demo查询
- **peropero**  随机播放一条起始(peropero~games~)语音
- **随机demo**  随便听一首demo
##### 游戏音效查询
- **随机游戏音效**  随便听听
- **听听好东西**  听一点MD玩家都喜欢听的
##### 资料查询
- **查询隐藏曲目**  查询隐藏曲目的解锁方式
- **偏移值参考**  查询游戏偏移值设定参考
- **游戏冷知识**  游戏相关的一些小知识
- **md表情包**  来一张musedash相关的表情包
- **md运势**  查看今天的md运势吧！
##### 角色&精灵查询
- **查询角色**  查询游戏内角色
- **查询精灵**  查询游戏内精灵
##### 插图查询
- **查询插图**  进入插图查询菜单
- **单/全图查询**  不同模式的插图查询
- **动画查询**  查询游戏Live2D插画
- **随机插画/封面**  随机查看一张图片
##### 场景查询
- **查询游戏场景**  进入游戏场景查询菜单
- **纯/合成场景**  查看不同的场景图片
- **随机纯场景/合成场景**  随机查看一张图片
##### 成就查询
- **查询成就**  进入查询菜单
- **单曲成就查询**  查询单曲关卡成就
- **游戏成就查询**  查询游戏成就
##### 运行
- **检查百科文件**  管理员 or 维护用，检查资源文件存储情况


### 说明

**语音资源包** 与 **图片资源包** 请放在HoshinoBot的 ``record`` 和 ``img`` 目录下

例如：你在**hoshino/config**的 `__bot__.py` 文件中填写的 **资源库文件夹**
```python
RES_DIR = "C:/Resources/"
```
那么你存放 语音资源包 的路径应该为
``C:/Resources/record/``
图片同理

> 2021/8/26，增加R模块更新，去除绝对路径的使用
> 调用方式： *xxx = R.rec(xxx.wav).cqcode*
> 还有一些其它的可以自己改的我都写在文件注释里面了。

<details>
  <summary>文件说明（可略）</summary>

大致说明一下插件文件：

``_chip_data.py`` 是游戏角色&精灵 的录入数据(字典)

``_record_data.py`` 是语音字幕与角色语音的对应  也是字典

``_song_data.py``  是歌曲/小贴士的录入数据  字典（因为不会用数据库，所以就用字典凑合凑合=  =）

``chara.py``  是Hoshinobot原版chara的改编，与歌名猜测功能相关

``musewiki_achievement.py``  查询成就的主文件

``musewiki_artwork.py``  查询插画的主文件

``musewiki_character.py``  查询角色的主文件

``musewiki_luck.py``  md运势的主文件

``musewiki_query.py``  资料库主文件

``musewiki_record.py``  游戏语音的主文件

``musewiki_song.py`` 是查询歌曲的主文件

``wiki_log.py``  检查百科文件的主文件

``R.py`` R模块增强版，支持语音调用

</details>


### 其它

资源文件出自个人游戏拆包。文件名有所修改
本人非专业程序员，业余写着玩玩，代码很菜，大佬们看看就好QwQ。
made by [Soung2279@Github](https://github.com/Soung2279/)

### 鸣谢

数据来源：
[MuseDash官方英文Wiki](https://musedash.fandom.com/wiki/Muse_Dash_Wiki)
[MuseDash.moe](https://musedash.moe/)
[PeroPeroGames！](http://www.peroperogames.com/)
[远哥制造](https://lab.yuangezhizao.cn/musedash)

骨干：
[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)


****

### 更新日志

#### 2021/8/26  v1.1.0

增加对 R模块 语音调用的支持。[[#HoshinoBot功能性增强-语音调用支持](https://github.com/Soung2279/advance_R)]
去除发送语音绝对路径的使用。

#### 2021/8/15  v1.0.0

正式上传至Github仓库

#### 2021/8/14  v0.0.9

补充demo资源

#### 2021/8/11  v0.0.6

修复部分 资料查询 文本缺失
补充部分图片资源
修复动画查询

#### 2021/8/7  v0.0.5

新增：【md运势】  简易实现md每日运势
补充了游戏解包资源，固定文件目录结构

