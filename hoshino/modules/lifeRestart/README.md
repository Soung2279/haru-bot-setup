# LifeRestart for HoshinoBot
### [原作地址](https://github.com/VickScarlet/lifeRestart)
### [python版原地址](https://github.com/cc004/lifeRestart-py)
### [本项目地址](https://github.com/Daishengsheng/lifeRestart_bot)

## 安装方法
这是一个[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)的人生重来模拟器插件

这个项目使用的HoshinoBot的消息触发器，如果你了解其他机器人框架的api(比如nonebot)可以只修改消息触发器就将本项目移植到其他框架

下面介绍HoshinoBot的安装方法

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
```
git clone https://github.com/Daishengsheng/lifeRestart_bot.git
```
然后使用如下命令安装依赖
```
pip install -r requirements.txt
```
然后在 HoshinoBot\\hoshino\\config\\\__bot__.py 文件的 MODULES_ON 加入 lifeRestart_bot

重启 HoshinoBot

## 指令
命令 | 说明 | 例
------------- | ------------- | --------------
/remake 或 人生重来 | 触发指令 | /remake

## 效果演示
![效果演示](https://github.com/DaiShengSheng/lifeRestart_bot/blob/master/example/example.png) 
