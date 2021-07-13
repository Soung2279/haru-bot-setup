
## 注意

其他功能慢慢来吧，大佬们别养马了，快来写插件，我想白嫖

虽然不一定经常更新，但要不点个star支持一下？

## 更新日志

21-05-31    v1.2    05-15修复了插件卡死的bug，05-30修复了推送Bug(issues#2)，之前考试周+公会战没空测试，所以现在才更新

21-05-05    v1.1    代码重写，修复了播报不能用的BUG，现按时间戳排序，今天才发现官网新闻居然不是按照时间顺序排序的

21-05-01    v1.0    首次测试

## umamusume_news

一个适用hoshinobot的赛马娘新闻插件，用于提供马娘新闻播报功能

数据来自马娘官网

本插件仅供学习研究使用，插件免费，请勿用于商业用途，一切后果自己承担

## 项目地址：
https://github.com/azmiao/umamusume_news/

## 功能

正式功能：

[马娘新闻] 查看最近五条新闻

（自动推送） 该功能没有命令

## 简单食用教程：

可看下方链接：

https://www.594594.xyz/2021/05/01/umamusume_news_for_hoshino/

或本页面：

1. 下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
```
git clone https://github.com/azmiao/umamusume_news
```

2. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'umamusume_news'

然后重启 HoshinoBot

3. 额外功能：（自动提醒）

在某个群里发消息输入下文以开启新闻播报
```
开启 umamusume-news-poller
```
可以通过发消息输入"lssv"查看这个功能前面是不是⚪来确认是否开启成功