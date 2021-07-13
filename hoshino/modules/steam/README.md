# steam_crawler_bot
这是一个基于HoshinoBot的steam爬虫插件，可以根据命令来爬取相关信息，并以合并消息的形式发送。目前所拥有的功能有：

注：**与steam相关的查询数据来源于steam官网，与小黑盒相关的查询数据来源于小黑盒官网**

- **查询今日特惠以及今日新品信息（默认返回50条）**
> 命令：今日特惠 or 今日新品

<img src="https://z3.ax1x.com/2021/06/29/RdOwkV.jpg" width = "35%" height = "35%" align=center />

- **根据输入的标签查询结果，所有steam标签详见tag.json（默认返回50条，标签需要全匹配,会过滤没匹配到的标签）**
> 命令：st搜标签 后接格式：页数(阿拉伯数字) 标签1 标签2，(记得用空格隔开)例：st搜标签1 动作 射击

<img src="https://z3.ax1x.com/2021/06/29/RdOsl4.jpg" width = "35%" height = "35%" align=center />

- **根据输入的游戏名字查询结果（能搜到多少条游戏信息就返回多少条）**
> 命令：st搜游戏 后接游戏名字

<img src="https://z3.ax1x.com/2021/06/29/RdORTx.jpg" width = "35%" height = "35%" align=center />

- **小黑盒数据查询，包含了爬取到的游戏是否处于史低以及是否新史低的信息**
> 命令：小黑盒查询/小黑盒查询页（后接阿拉伯数字）

<img src="https://z3.ax1x.com/2021/07/04/Rfrq7q.jpg" width = "35%" height = "35%" align=center />

**更多详细请发送"st机器人帮助"获取**

**使用方法：**

在HoshinoBot的modules文件夹下新建一个steam_crawler_bot文件夹，并将本项目的文件复制进去，然后在hoshino/config/\_\_bot\_\_.py中的MODULES_ON中添加'steam_crawler_bot'

HoshinoBot的部署详见[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)

# 更新

_2021.7.4 新增了小黑盒数据爬取功能，优化了一些报错的提示，以及使代码规范化了一些_

# 计划

或许会加入更多奇奇怪怪的功能，欢迎提交pr或issue来告诉我你们希望能加入什么功能
