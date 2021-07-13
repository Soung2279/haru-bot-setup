# Majsoul_bot

### This is a Majsoul plugin for [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
### 这是一个[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)的雀魂相关插件
### 本项目目前正在扩展，后续会扩展更多功能，敬请期待


# 前言 
项目地址：https://github.com/DaiShengSheng/Majsoul_bot

本插件数据来源于雀魂牌谱屋:https://amae-koromo.sapk.ch/

由于牌谱屋不收录铜之间以及银之间牌谱，故所有数据仅统计2019年11月29日后金场及以上场次的数据

PS：本插件暂时只支持四麻对局的查询，后续会完善三麻查询功能

# 安装方法

这个项目使用的HoshinoBot的消息触发器，如果你了解其他机器人框架的api(比如nonebot)可以只修改消息触发器就将本项目移植到其他框架

下面介绍HoshinoBot的安装方法

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
```
git clone https://github.com/Daishengsheng/Majsoul_bot.git
```
然后使用如下命令安装依赖
```
pip install -r requirements.txt
```
然后在 HoshinoBot\\hoshino\\config\\\__bot__.py 文件的 MODULES_ON 加入 Majsoul_bot

重启 HoshinoBot


# 相关指令
### 牌谱及个人数据查询
命令  | 说明 | 例
------------- | ------------- | --------------
雀魂信息/雀魂查询 昵称  | 查询该昵称的基本对局数据(所有场次) | 雀魂信息 天才麻将杏杏
三麻信息/三麻查询 昵称 | 查询该昵称的三麻的基本对局数据(所有场次) | 三麻信息 天才麻将杏杏
雀魂信息/雀魂查询 (金/金之间/金场/玉/王座) 昵称 | 查询该ID在金/玉/王座之间的详细数据 | 雀魂信息 王座 天才麻将杏杏
三麻信息/三麻查询 (金/金之间/金场/玉/王座) 昵称 | 查询该ID在三麻金/玉/王座之间的详细数据 | 三麻信息 王座 天才麻将杏杏
雀魂牌谱/牌谱查询 昵称 | 查询该ID下最近五场的四麻对局信息 |  雀魂牌谱 天才麻将杏杏
三麻牌谱 昵称 | 查询该ID下最近五场的三麻对局信息 |  三麻牌谱 天才麻将杏杏

### 雀魂对局订阅
命令 | 说明 | 例
------------- | ------------- | --------------
雀魂订阅 昵称 | 订阅该昵称在金之间以上的四麻对局信息 | 雀魂订阅 天才麻将杏杏
三麻订阅 昵称 | 订阅该昵称在金之间以上的三麻对局信息 | 三麻订阅 天才麻将杏杏
(取消/关闭)雀魂订阅 昵称| 将该昵称在本群的订阅暂时关闭 | 关闭雀魂订阅 天才麻将杏杏
(取消/关闭)三麻订阅 昵称| 将该昵称在本群的三麻订阅暂时关闭 | 关闭三麻订阅 天才麻将杏杏
开启雀魂订阅 昵称 | 将该昵称在本群的订阅开启 | 开启雀魂订阅 天才麻将杏杏
开启三麻订阅 昵称 | 将该昵称在本群的三麻订阅开启 | 开启三麻订阅 天才麻将杏杏
删除雀魂订阅 昵称 | 将该昵称在本群的订阅删除 | 删除雀魂订阅 天才麻将杏杏
删除三麻订阅 昵称 | 将该昵称在本群的三麻订阅删除 | 删除三麻订阅 天才麻将杏杏
雀魂订阅状态 | 查询本群的雀魂订阅信息的开启状态 | 雀魂订阅状态
三麻订阅状态 | 查询本群的雀魂三麻订阅信息的开启状态 | 三麻订阅状态

# 效果演示
### 基本数据查询
![基本数据查询](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/selectBasicInfo.png) 
### 详细数据查询
![详细数据查询](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/selectExtendInfo.png) 
### 近期对局查询
![近期对局查询](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/selectRecord.png) 
### 雀魂对局订阅
![雀魂对局订阅](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/OrderRecord.png)
### 订阅的开启与删除
![订阅的开启与删除](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/ControlRecord.png)

# 更新记录
### 2021-06-01
* 更新了三麻信息查询以及订阅功能

### 2021-05-31
* 修复了由于获取订阅超时造成的Bot卡顿问题
* 修复了长时间不启动对对局订阅更新失败的Bug
* 将对局订阅播报更新为图片形式发送
* 修复了订阅对局触发多条消息的Bug

### 2021-05-30
* 新增了金之间以上的四麻群友对局订阅(迫害)功能（群友又吃四了.jpg
* 修复了一些不为人知的bug

### 2021-05-27
* 雀魂插件出生啦！初步实现了角色四麻数据的查询以及其牌谱的查询
* 计划加入卡池(新建文件夹)以及三麻查询功能

# 已知问题
### 2021-06-02
* bot在某些特定情况下可能不回应请求(等待修复)

### 2021-05-30
* bot在雀魂订阅获取更新时可能会卡死（已修复）
* bot长时间不启动导致后续启动后对局订阅更新失败的bug（已修复）
* 订阅信息下一版本更新后将会使用图片发布（已优化）

