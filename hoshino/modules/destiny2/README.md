
## 注意

## 03-09正式弃坑命运2，问就是现在沉迷赛马娘 OxO

## 代码比较冗杂，变量名还整点活，望见谅

查perk功能近期没啥想法，不想做了。蛛王信息更新受限于小黑盒，小黑盒有时候会没有人更新。

然后插件可能时不时会诈尸更新，本github页面会同步，其他地方可能不会都发布

v2.0开始为了方便将图片下载至本地了，以为未来可能有啥的功能方便用

## 更新日志

21-03-02    v2.0    重构部分代码，弃用onebot相关代码，使之适配Mirai v2.2.2及 以上的版本

21-01-26    v1.2.1  同步网络时间，并修改部分代码，现在可以不用定时任务，直接用了

20-12-06    v1.2    重构了获取数据的方法，现在可以稳定的自动更新周报等数据了，并且无需获取cookies。另外增加了更新提醒功能，开启方法见教程

20-11-26    v1.1    修改了周报和老九功能，现在也能正常的自动更新数据了

20-11-25    v1.0    优化了部分描述

## destiny2_hoshino_plugin

一个适用hoshinobot的命运2插件，用于查询周报/老九等信息（自动更新）

数据来自小黑盒，各种功能已分别标记出处，这里鸣谢 @seanalpha 提供了图片

本插件仅供学习研究使用，插件免费，请勿用于商业用途，一切后果自己承担

## 项目地址：
https://github.com/azmiao/destiny2_hoshino_plugin/

## 功能

正式功能：

[周报] 查看命运2周报

[老九] 查看老九位置和装备

[试炼] 查看试炼周报

[蛛王] 查看蛛王商店

[光尘] 查看光尘商店

[百科] 小黑盒百科链接（只是一个链接而已）

## 简单食用教程：

可看下方链接：

https://www.594594.xyz/2020/11/19/destiny2_hoshino_plugin/

或本页面：

1. 下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
```
git clone https://github.com/azmiao/destiny2_hoshino_plugin
```
2. 安装依赖：

到HoshinoBot\hoshino\modules\destiny2_hoshino_plugin目录下，打开powershell运行
```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'destiny2_hoshino_plugin'

然后重启 HoshinoBot即可使用

4. 额外功能：（自动提醒）

在某个群里发消息输入下文以开启周报更新提醒（默认设置周三凌晨3点，可自行更改）
```
开启 zhoubao-reminder
```
在某个群里发消息输入下文以开启老九更新提醒（默认设置周六凌晨3点，可自行更改）
```
开启 laojiu-reminder
```
在某个群里发消息输入下文以开启试炼更新提醒（默认设置周三凌晨3点，可自行更改）
```
开启 shilian-reminder
```
在某个群里发消息输入下文以开启蛛王更新提醒（默认设置每天凌晨3点，可自行更改）
```
开启 zhuwang-reminder
```
可以通过发消息输入"lssv"查看这几个功能前面是不是⚪来确认是否开启成功
