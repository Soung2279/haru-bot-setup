# EXPLOSION-惠惠爆裂魔法语音

→→→ [前往更新日志](#更新日志)

*****

## 简介
“エクスプロージョン（Explosion）！”
和[惠惠](https://zh.moegirl.org.cn/%E6%83%A0%E6%83%A0)每天练习爆裂魔法吧！

适用于 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot) 的娱乐插件，随机发送一则[惠惠](https://zh.moegirl.org.cn/%E6%83%A0%E6%83%A0)使用爆裂魔法吟唱时的咒文与语音

*****

## 安装
- **步骤一** : 直接下载/克隆本项目，将文件夹放入 ``hoshino/modules`` 路径下, 在 ``hoshino/config/__bot__.py`` 里的 ``MODULES_ON`` 中添加 "explosion"

```python
# 启用的模块
MODULES_ON = {
    'xxx',
    'explosion',  #注意英文逗号
    'xxx',
}
```

- **步骤二** : 在Releases处下载语音资源包，并将语音资源放在**Hoshinobot的资源库文件夹**下，该文件夹可在在 ``hoshino/config/__bot__.py`` 里的 ``RES_DIR`` 处修改

```python
# 资源库文件夹，需可读可写，windows下注意反斜杠转义
RES_DIR = r'X:/xxx/'
```

如果Release下载速度不理想，可尝试下列途径：
<details>
  <summary>百度网盘</summary>

- [爆裂魔法语音资源](https://pan.baidu.com/s/1xhOnGD5d9sz5rmT6OmGxxg)
> 提取码：2279

</details>

<details>
  <summary>qq群文件</summary>

[SoungBot交流群（free edition](https://jq.qq.com/?_wv=1027&k=rKLpjTPz)
> 推荐在百度网盘不可用 or 下载过于缓慢的时候使用

</details>

<br>如果按照步骤正常安装，重启 HoshinoBot 即可开始使用爆裂魔法功能。</br>

*****

## 指令表

- **爆裂魔法**  ：和 bot 随机练习一发爆裂魔法
- **补魔**  ：补充魔力（重置日上限），需@bot
- **帮助爆裂魔法**  ：查看帮助说明

*****

## 注意

在 ``explosion.py`` 的第18，19行，引入了 ``hoshino/config/__bot__.py`` 中设置的呢称 ``NICKNAME`` ，如果您的 ``NICKNAME`` 不是[元组](https://baike.baidu.com/item/%E5%85%83%E7%BB%84/3190018?fr=aladdin)形式，则可能导致发送文本错乱。若出现此类情况，则应该**手动**修改此处为设定的 bot呢称。

```python
bot_name = config.NICKNAME
show_name = bot_name[0]  #如果不是元组请直接在此处填写你的bot呢称，示例：show_name = "野中晴"
```

语音文件的路径设置在 ``explosion.py`` 的第47行，若未按照上述步骤安装，请检查此处是否为您**存放语音文件的路径**。

```python
        explosion_rec = R.get('explosion/', voice_name)  # 在此处修改语音文件存放的路径（放置在Hoshinobot的资源路径下）
```

*****

### 其它

本人非专业程序员，业余写着玩玩，代码很菜，大佬们看看就好QwQ。

made by [Soung2279@Github](https://github.com/Soung2279/)

### 鸣谢

[HoshinoBot项目地址](https://github.com/Ice-Cirno/HoshinoBot)

### 更新日志

##### 2021/8/20

代码重构，优化逻辑，去除杂糅代码。去除了大量绝对路径，将语音对应文本独立出来方便后续添加
利用API：can_send_record，在发送语音之前将先检查是否能发送语音
使用MessageSegment.record发送语音而非直接使用[CQ:record,file=xxx]

注意：新旧版本的explosion**不互通**，且**语音文件路径**有所变化，请注意。

##### 2021/4/4

首次上传
