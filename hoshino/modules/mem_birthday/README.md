
# 注意

### （非常重要的部分标题已标明）

## **使用要求（请务必看完）**

* hoshino v2+

* 如果使用 go-cqhttp 的软件要求：反正不要远古版本应该都行（未经测试）

* 如果使用 mirai 的软件要求：请确保 onebot-mirai （也就是原 cqhttp-mirai ）的版本 >= 0.3.5
>说明：目前已发布的最新版本为 0.3.4 ，该版本不支持，若需要使用此插件，请前往 [点我前往](https://github.com/yyuueexxiinngg/onebot-kotlin/actions/runs/1008564711) 下载下方的未发布的 onebot-mirai ，该版本为 0.3.5 ，适配了部分 mirai v2.1 开始的API

* 需要生日提醒的群员，必须一直开启年龄所有人可见，且在插件初始化前开启所有人可见 或者 插件初始化后保持两天所有人可见及以上

* 插件首次初始化的当天不会有任何的生日提醒（当天是指在腾讯网络时间24：00之前），第二天开始才正常运作

## 部分问题解答(这个嫌长可以不看)

* Q：在文件 `create_config.py` 中的 `write_info()` 为什么要获取 member_list 再查一遍 stranger_info 呢？

>A：
这里对于go-cqhttp的小可爱可能就是无用步骤了，
但是对于部分因为 mirai-native 的原 酷Q用户来说，dll 类型的插件从酷Q用到现在一直不想换掉(~~dll是真的好用~~)。
但是 cqhttp-mirai 也就是现在的 onebot-mirai 的作者，
非常忙以至于没时间更新 onebot-mirai ，所以未跟进 mirai v2.1 后的部分API
仔细翻阅 Issue 后发现 0.3.5 版本虽然暂未发布(不知道他要啥时候发)，但其不完全的版本已经实现了
用 stranger_info 获取年龄和性别的API，才有这么一步对 onebot-mirai 来说不可或缺的多余步骤

## 插件后续

插件后续将继续在 github 不定期更新

欢迎提交 isuue 和 request ，尤其是我没有用 go-cqhttp 可能会产生一些 BUG

# 插件介绍

## 更新日志

21-08-23    v1.0    大概能用了？

## mem_birthday

一个适用hoshinobot的 群友生日祝贺 插件

由于 API 只提供了获取年龄的接口，没有获取生日的，因此编写了此插件

本插件仅供学习研究使用，插件免费，请勿用于违法商业用途，一切后果自己承担

## 项目地址：

已放至pcrbot仓库

https://github.com/pcrbot/mem_birthday

## **功能（请务必看完）**

```
命令如下：

[群员生日初始化] 初始化配置（限维护组，且仅限初始化一次，初始化时间受群数量和人数影响，总共两三百人大概要1分钟或者更久）

注：为防止误触，不提供群内删除文件的命令，若想重新初始化，请手动到本文件目录删除`config.yml`

（其余功能为自动触发）

<凌晨 2 点：自动更新群员年龄，预计用时和初始化时间一致>

<早上 8 点：自动分群里推送每个群里生日的群员祝福>
```


## 简单食用教程：

可看下方链接(引流一波我的主页)：

（↓还没写↓）

https://www.594594.xyz/2021/08/23/mem_birthday_for_hoshino/

或本页面：

1. 下载或git clone本插件：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/pcrbot/mem_birthday
    ```

2. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'mem_birthday'

    然后重启 HoshinoBot

3. 随便找个群

    在群里发送命令'群员生日初始化' ，进行初始化
