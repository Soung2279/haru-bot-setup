# 300英雄出租自动推送
## 功能介绍
基于hoshino机器人，在群内绑定300英雄角色ID，实现群内自动推送助手出租信息，战场胜场信息。
## 具体操作
1、在<code>hoshino/modules</code>文件夹中，打开<code>cmd</code>，输入以下代码 按回车执行：
<pre>git clone https://github.com/jiyemengmei/300hero.git</pre>
2、在<code>hoshino/config/__bot__.py</code>文件中，<code>MODULES_ON</code>里添加 "300hero"
## 功能指令
|  指令   | 说明  | 具体  |
|  ----  | ----  | ----  |
| <b>绑定角色XXX\|大区名</b>  | 绑定角色ID和所在大区，角色名和大区用\|分开写 | 绑定角色<b>刀剑小肥龙</b>\|<b>刀剑神域</b>  |
| 查询角色/角色查询  | 查询指定ID是否存在或者绑定在谁那  | 查询角色<b>刀剑小肥龙</b>  |
| <b>启用/停止自动推送</b>  | 开启或关闭出租信息自动推送，默认为停止，推送间隔为5分钟 |
| 删除角色绑定  | 删除掉自己的角色绑定信息  |
| 角色绑定状态  | 查询自己的角色绑定信息  |
| 查胜场  | 查询自己绑定角色的胜场信息，用@可以查询他人的信息  | 查胜场@123456789  |
| 查出租  | 查询自己绑定角色的出租信息，用@可以查询他人的信息  | 查出租@123456789  |
## 其他
本插件逻辑写的很烂，在众多大佬的帮助下才完成的。
## 鸣谢
<a href="https://github.com/Mrs4s/go-cqhttp" target="_BLANK">go-cqhttp</a>\
<a href="https://github.com/Ice-Cirno/HoshinoBot" target="_BLANK">HoshinoBot</a>\
<a href="http://static.300mbdl.cn/box/index.html#/home" target="_BLANK">300助手</a>\
<a href="http://300.electricdog.net/300hero" target="_BLANK">300英雄胜场查询网</a>
## API
<a href="http://api.300mbdl.cn/%E6%8E%A5%E5%8F%A32/%E7%A7%9F%E5%8F%B7/%E7%A7%9F%E5%8F%B7%E5%A4%A7%E5%8E%85?%E9%A1%B5=1&%E9%A1%B5%E9%95%BF=200" target="_BLANK">出租信息</a>\
<a href="http://300.electricdog.net/300hero/" target="_BLANK">胜场信息</a>
## 更新日志
### 2021/8/20
首次上传
