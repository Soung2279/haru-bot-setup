# README.md Chinese Ver

# HoshinoBot 原神 x KFC 语音插件

[Click here to read README.md English Ver](https://github.com/GirlKiller512/HoshinoBot_GenshinKFC#readmemd-english-ver)

[こちらをクリックしてREADME.md日本語版を読みます](https://github.com/GirlKiller512/HoshinoBot_GenshinKFC#readmemd-japanese-ver)

### 上次更新日期：2021年4月3日

HoshinoBot, a QQ bot for Princess Connect! Re:Dive: https://github.com/Ice-Cirno/HoshinoBot

能让星乃发出来自二次元的声音！（雾）

**（异世相遇，尽享美味！）**

（强烈建议将音量调大播放语音！）

**碎碎念：**

我写个README.md都是边写边笑的，草

味，冲了出来（D区）

**功能说明：**

在QQ群发送指定的指令，Bot会随机从`record`目录中选择一条语音回复

![Screenshot](./Screenshot1.jpg)

（这是刻晴CV的音源）

**目前拥有的音源：**

|       音源        |         格式          |          上传日期          |                           相关链接                           |
| :---------------: | :-------------------: | :------------------------: | :----------------------------------------------------------: |
|       莉莎        |  FLAC 24位PCM 48KHz   | （不可能上传的，别做梦了） | https://space.bilibili.com/1723811 https://bbs.nga.cn/nuke.php?func=ucp&uid=60581499 |
|  刻晴CV（谢莹）   | MP3 192Kbps 48KHz CBR |       2021年3月13日        | https://space.bilibili.com/44243 https://www.bilibili.com/video/BV1ef4y147vK |
| 莫娜CV（陈婷婷）  | MP3 192Kbps 48KHz CBR |       2021年3月13日        | https://space.bilibili.com/612788 https://www.bilibili.com/video/BV1Ny4y1E7dw |
|   香菱CV（小N）   | MP3 192Kbps 48KHz CBR |       2021年3月16日        | https://space.bilibili.com/249118 https://space.bilibili.com/5126045 https://www.bilibili.com/video/BV1WV411Y782 |
| 派蒙CV（多多poi） | MP3 192Kbps 48KHz CBR |       2021年3月16日        | https://space.bilibili.com/11253297 https://space.bilibili.com/534963525 https://www.bilibili.com/video/BV1s5411K7mX |
|  甘雨CV（林簌）   | MP3 192Kbps 48KHz CBR |       2021年3月22日        | https://space.bilibili.com/7223194 https://www.bilibili.com/video/BV1v5411P7eR |
| 安柏CV（蔡书瑾）  | MP3 192Kbps 48KHz CBR |       2021年3月30日        | https://space.bilibili.com/519566923 https://www.bilibili.com/video/BV12p4y1b76s |
|      keii萤       | MP3 192Kbps 48KHz CBR |       2021年3月17日        | https://space.bilibili.com/437786939 https://www.bilibili.com/video/BV1hh411Q7Fa |
|       一焰        | MP3 192Kbps 48KHz CBR |       2021年3月17日        | https://space.bilibili.com/2055691 https://www.bilibili.com/video/BV14A411T74t |
|     钉宫妮妮      | MP3 192Kbps 48KHz CBR |       2021年3月17日        | https://space.bilibili.com/8881297 https://www.bilibili.com/video/BV1WA411T76k |
|       铃音        | MP3 192Kbps 48KHz CBR |       2021年3月17日        | https://space.bilibili.com/39267739 https://www.bilibili.com/video/BV18z4y117q5 |
|       早凉        | MP3 192Kbps 48KHz CBR |       2021年3月17日        | https://space.bilibili.com/518817 https://www.bilibili.com/video/BV185411K7sq |
|     白银莉莉      | MP3 192Kbps 48KHz CBR |       2021年3月17日        | https://space.bilibili.com/494850406 https://www.bilibili.com/video/BV1gi4y1K738 |
|    蜜桃味kiki     | MP3 192Kbps 48KHz CBR |       2021年3月19日        | https://space.bilibili.com/7881923 https://www.bilibili.com/video/BV1d5411A7z9 |
|       小柔        | MP3 192Kbps 48KHz CBR |       2021年3月24日        | https://space.bilibili.com/1734978373 https://space.bilibili.com/473764233 https://www.bilibili.com/video/BV1GK4y1T7uV |
|    步玎Pudding    | MP3 192Kbps 48KHz CBR |        2021年4月3日        | https://space.bilibili.com/416622817 https://www.bilibili.com/video/BV1Jh411U77w |

**TODO：**

- 寻找可莉CV（花玲）音源

## 安装方法

1. 安装ffmpeg

   Ubuntu：`apt install ffmpeg`

   CentOS：

   ```shell
   yum install epel-release
   
   rpm -v --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
   rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
   
   yum install ffmpeg ffmpeg-devel
   ```

2. 将`genshinkfc`目录放入`hoshino/modules`目录中

3. 打开`hoshino/config/__bot__.py`，在`MODULES_ON`中加入`genshinkfc`并保存

4. 重启HoshinoBot

## 指令

|       指令       |            说明            |
| :--------------: | :------------------------: |
|       KFC        | 大小写均可，必须全大或全小 |
|     原神KFC      |            同上            |
|    二次元KFC     |            同上            |
| 异世相遇尽享美味 |                            |

## 原文

ねねね，服务员おにいちゃん~~

えっとねえっとね，わたし就是那个，二次元です~~

二次元的美好，みなさん都知道的吧！

だから，人家ほしい~~

对，那个二次元的徽章~~

おねがい，わたしすごくすきすきだ，すき那个徽章~~

なに？一定要那个口号吗？呜呜呜，はずかしい……

でも，为了超级想要的二次元徽章……わたし会がんばって！

**异世相遇，尽享美味！**

ありがとうおにいちゃん，だいすきです！

## 原文（添加颜文字和动作描写）

ねねね，服务员おにいちゃん(>ω<)~~（超级肉麻）

えっとねえっとね，わたし就是那个，二次元です(｡ò ∀ ó｡)~~（超级得意）

二次元的美好，みなさん都知道的吧！(≧∇≦)/（转身超级大声跟店里的顾客说了这句话）

だから，人家ほしい~~

对，那个二次元的徽章~~

おねがい(;｀O´)o，わたしすごくすきすきだ，すき那个徽章~~

なにヾ(Ő∀Ő๑)ﾉ？一定要那个口号吗,,Ծ^Ծ,,？呜呜呜，はずかしい……

でも，为了超级想要的二次元徽章……わたし会がんばって(>﹏<)！

异世相遇(>ω<)，（华丽转圈圈）尽享美味(\*≧ｍ≦\*)！（转圈停下来然后跳起来对着服务员左手叉腰右手比着）

ありがとうおにいちゃん，だいすきです！

## 原文（假名转汉字）

呐呐呐，服务员欧尼酱~~

诶多捏诶多捏，瓦塔西就是那个，二次元得斯~~

二次元的美好，米娜桑都知道的吧！

达卡拉，人家厚洗一~~

对，那个二次元的徽章~~

哦捏该，瓦塔西斯国库斯ki斯ki达，斯ki那个徽章~~

纳尼？一定要那个口号吗？呜呜呜，哈子卡西一……

得莫，为了超级想要的二次元徽章……瓦塔西会干巴爹！

**异世相遇，尽享美味！**

阿里嘎多欧尼酱，带斯ki得斯！

# README.md English Ver

# HoshinoBot Genshin Impact x KFC Voice Plugin

[点击这里阅读README.md中文版](https://github.com/GirlKiller512/HoshinoBot_GenshinKFC#readmemd-chinese-ver)

[こちらをクリックしてREADME.md日本語版を読みます](https://github.com/GirlKiller512/HoshinoBot_GenshinKFC#readmemd-japanese-ver)

### Last Update Date: April 3, 2021 (UTC+8)

HoshinoBot, a QQ bot for Princess Connect! Re:Dive: https://github.com/Ice-Cirno/HoshinoBot

Let Hoshino utter the voice from the ACG world!

**（Meet In Another World, Savour Deliciousness!）**

(It is strongly recommended to play the voice with the volume turned up!)

**Function Description:**

Send specified commands in the QQ group and Bot will randomly select a voice from `record` directory to reply

![Screenshot](./Screenshot1.jpg)

(This is Keqing's CV's voice)

**Currently Held Voice:**

|                Source                |        Format         |           Upload Date (UTC+8)            |                         Related Link                         |
| :----------------------------------: | :-------------------: | :--------------------------------------: | :----------------------------------------------------------: |
|                 Liza                 | FLAC 24-bit PCM 48KHz | (Upload is impossible and stop dreaming) | https://space.bilibili.com/1723811 https://bbs.nga.cn/nuke.php?func=ucp&uid=60581499 |
|        Keqing's CV (Xie Ying)        | MP3 192Kbps 48KHz CBR |              March 13, 2021              | https://space.bilibili.com/44243 https://www.bilibili.com/video/BV1ef4y147vK |
|      Mona's CV (Chen Tingting)       | MP3 192Kbps 48KHz CBR |              March 13, 2021              | https://space.bilibili.com/612788 https://www.bilibili.com/video/BV1Ny4y1E7dw |
|  Xiangling's CV (Xiao N, Jiang Li)   | MP3 192Kbps 48KHz CBR |              March 16, 2021              | https://space.bilibili.com/249118 https://space.bilibili.com/5126045 https://www.bilibili.com/video/BV1WV411Y782 |
| Paimon's CV (Duoduo poi, Shi Xinlei) | MP3 192Kbps 48KHz CBR |              March 16, 2021              | https://space.bilibili.com/11253297 https://space.bilibili.com/534963525 https://www.bilibili.com/video/BV1s5411K7mX |
|   Ganyu's CV (Lin Su, Tang Suling)   | MP3 192Kbps 48KHz CBR |              March 22, 2021              | https://space.bilibili.com/7223194 https://www.bilibili.com/video/BV1v5411P7eR |
|       Amber's CV (Cai Shujin)        | MP3 192Kbps 48KHz CBR |              March 30, 2021              | https://space.bilibili.com/519566923 https://www.bilibili.com/video/BV12p4y1b76s |
|               keiiying               | MP3 192Kbps 48KHz CBR |              March 17, 2021              | https://space.bilibili.com/437786939 https://www.bilibili.com/video/BV1hh411Q7Fa |
|                Makuma                | MP3 192Kbps 48KHz CBR |              March 17, 2021              | https://space.bilibili.com/2055691 https://www.bilibili.com/video/BV14A411T74t |
|                Ninico                | MP3 192Kbps 48KHz CBR |              March 17, 2021              | https://space.bilibili.com/8881297 https://www.bilibili.com/video/BV1WA411T76k |
|                Suzune                | MP3 192Kbps 48KHz CBR |              March 17, 2021              | https://space.bilibili.com/39267739 https://www.bilibili.com/video/BV18z4y117q5 |
|               Zaoliang               | MP3 192Kbps 48KHz CBR |              March 17, 2021              | https://space.bilibili.com/518817 https://www.bilibili.com/video/BV185411K7sq |
|             Baiyin Lili              | MP3 192Kbps 48KHz CBR |              March 17, 2021              | https://space.bilibili.com/494850406 https://www.bilibili.com/video/BV1gi4y1K738 |
|            Mitaowei kiki             | MP3 192Kbps 48KHz CBR |              March 19, 2021              | https://space.bilibili.com/7881923 https://www.bilibili.com/video/BV1d5411A7z9 |
|               Xiaorou                | MP3 192Kbps 48KHz CBR |              March 24, 2021              | https://space.bilibili.com/1734978373 https://space.bilibili.com/473764233 https://www.bilibili.com/video/BV1GK4y1T7uV |
|            Buding Pudding            | MP3 192Kbps 48KHz CBR |              April 3, 2021               | https://space.bilibili.com/416622817 https://www.bilibili.com/video/BV1Jh411U77w |

**TODO：**

- Find the voice of Klee's CV (Hualing)

## How To Install

1. Install ffmpeg

   Ubuntu: `apt install ffmpeg`

   CentOS:

   ```shell
   yum install -y epel-release
   
   rpm -v --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
   rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
   
   yum install ffmpeg ffmpeg-devel
   ```

2. Put  `genshinkfc` directory into `hoshino/modules` directory

3. Open `hoshino/config/__bot__.py` file , add `genshinkfc` to `MODULES_ON` set and save

4. Restart HoshinoBot

## Command

|     Command      |                         Description                          |
| :--------------: | :----------------------------------------------------------: |
|       KFC        | Upper case and lower case are both OK, but the letters have to be all upper or all lower |
|     原神KFC      |                        Same as above                         |
|    二次元KFC     |                        Same as above                         |
| 异世相遇尽享美味 |                                                              |

## Original Text

ねねね，服务员おにいちゃん~~

えっとねえっとね，わたし就是那个，二次元です~~

二次元的美好，みなさん都知道的吧！

だから，人家ほしい~~

对，那个二次元的徽章~~

おねがい，わたしすごくすきすきだ，すき那个徽章~~

なに？一定要那个口号吗？呜呜呜，はずかしい……

でも，为了超级想要的二次元徽章……わたし会がんばって！

**异世相遇，尽享美味！**

ありがとうおにいちゃん，だいすきです！

## Original Text (With Kaomoji And Action Description)

ねねね，服务员おにいちゃん(>ω<)~~ (Speak very nauseatingly)

えっとねえっとね，わたし就是那个，二次元です(｡ò ∀ ó｡)~~ (Feel very elated)

二次元的美好，みなさん都知道的吧！(≧∇≦)/ (Turn round and shout it to customers here)

だから，人家ほしい~~

对，那个二次元的徽章~~

おねがい(;｀O´)o，わたしすごくすきすきだ，すき那个徽章~~

なにヾ(Ő∀Ő๑)ﾉ？一定要那个口号吗,,Ծ^Ծ,,？呜呜呜，はずかしい……

でも，为了超级想要的二次元徽章……わたし会がんばって(>﹏<)！

异世相遇(>ω<)，(Spin gaily) 尽享美味(\*≧ｍ≦\*)！（Stop spinning, jump and gesture to the waiter with the right hand and with the left hand akimbo）

ありがとうおにいちゃん，だいすきです！

## Original Text (All Romanized)

Nenene, fuwuyuan oniichan~~

Ettone ettone, watashi jiushi neige, erciyuan desu~~

Erciyuan de meihao, minasan dou zhidao de ba!

Dakara, renjia hoshii~~

Dui, neige erciyuan de huizhang~~

Onegai, watashi sugoku suki suki da, suki neige huizhang~~

Nani? Yiding yao neige kouhao ma? Wuwuwu, hazukashii......

Demo, weile chaoji xiangyao de erciyuan huizhang......Watashi hui ganbatte!

**Yishi xiangyu, jinxiang meiwei!**

Arigatou oniichan, daisuki desu!

# README.md Japanese Ver

# HoshinoBot 原神 x KFC ボイスプラグイン

[点击这里阅读README.md中文版](https://github.com/GirlKiller512/HoshinoBot_GenshinKFC#readmemd-chinese-ver)

[Click here to read README.md English Ver](https://github.com/GirlKiller512/HoshinoBot_GenshinKFC#readmemd-english-ver)

### 前回更新日：2021年4月3日 (UTC+8)

HoshinoBot, a QQ bot for Princess Connect! Re:Dive: https://github.com/Ice-Cirno/HoshinoBot

星乃に二次元からの声を出させて！

**（異世界で巡り会い、美食をともに楽しもう！）**

（大きな音量でボイスを再生したらもっと素晴らしいと思います！）

**機能説明：**

QQグループに指定されたコマンドを送信して、Botはランダムに`record`ディレクトリから選択されたボイスを返信する

![Screenshot](./Screenshot1.jpg)

（これは刻晴（コクセイ）のCVのボイスです）

**現在持っているボイス：**

|            ボイス             |     フォーマット      |        アップロード日 (UTC+8)        |                          関連リンク                          |
| :---------------------------: | :-------------------: | :----------------------------------: | :----------------------------------------------------------: |
|             莉莎              | FLAC 24-bit PCM 48KHz | （アップロードは不可能、夢を見るな） | https://space.bilibili.com/1723811 https://bbs.nga.cn/nuke.php?func=ucp&uid=60581499 |
| 刻晴（コクセイ）のCV（謝瑩）  | MP3 192Kbps 48KHz CBR |            2021年3月13日             | https://space.bilibili.com/44243 https://www.bilibili.com/video/BV1ef4y147vK |
|      モナのCV（陳婷婷）       | MP3 192Kbps 48KHz CBR |            2021年3月13日             | https://space.bilibili.com/612788 https://www.bilibili.com/video/BV1Ny4y1E7dw |
| 香菱（シャンリン）のCV（小N） | MP3 192Kbps 48KHz CBR |            2021年3月16日             | https://space.bilibili.com/249118 https://space.bilibili.com/5126045 https://www.bilibili.com/video/BV1WV411Y782 |
|    パイモンのCV（多多poi）    | MP3 192Kbps 48KHz CBR |            2021年3月16日             | https://space.bilibili.com/11253297 https://space.bilibili.com/534963525 https://www.bilibili.com/video/BV1s5411K7mX |
|  甘雨（カンウ）のCV（林簌）   | MP3 192Kbps 48KHz CBR |            2021年3月22日             | https://space.bilibili.com/7223194 https://www.bilibili.com/video/BV1v5411P7eR |
|    アンバーのCV（蔡書瑾）     | MP3 192Kbps 48KHz CBR |            2021年3月30日             | https://space.bilibili.com/519566923 https://www.bilibili.com/video/BV12p4y1b76s |
|            keii蛍             | MP3 192Kbps 48KHz CBR |            2021年3月17日             | https://space.bilibili.com/437786939 https://www.bilibili.com/video/BV1hh411Q7Fa |
|             一焔              | MP3 192Kbps 48KHz CBR |            2021年3月17日             | https://space.bilibili.com/2055691 https://www.bilibili.com/video/BV14A411T74t |
|            Ninico             | MP3 192Kbps 48KHz CBR |            2021年3月17日             | https://space.bilibili.com/8881297 https://www.bilibili.com/video/BV1WA411T76k |
|             鈴音              | MP3 192Kbps 48KHz CBR |            2021年3月17日             | https://space.bilibili.com/39267739 https://www.bilibili.com/video/BV18z4y117q5 |
|             早涼              | MP3 192Kbps 48KHz CBR |            2021年3月17日             | https://space.bilibili.com/518817 https://www.bilibili.com/video/BV185411K7sq |
|           白銀莉莉            | MP3 192Kbps 48KHz CBR |            2021年3月17日             | https://space.bilibili.com/494850406 https://www.bilibili.com/video/BV1gi4y1K738 |
|          蜜桃味kiki           | MP3 192Kbps 48KHz CBR |            2021年3月19日             | https://space.bilibili.com/7881923 https://www.bilibili.com/video/BV1d5411A7z9 |
|             小柔              | MP3 192Kbps 48KHz CBR |            2021年3月24日             | https://space.bilibili.com/1734978373 https://space.bilibili.com/473764233 https://www.bilibili.com/video/BV1GK4y1T7uV |
|          步玎Pudding          | MP3 192Kbps 48KHz CBR |             2021年4月3日             | https://space.bilibili.com/416622817 https://www.bilibili.com/video/BV1Jh411U77w |

**TODO：**

- クレーのCVのボイスを探す

## インストール方法

1. ffmpegをインストールします

   Ubuntu：`apt install ffmpeg`

   CentOS：

   ```shell
   yum install -y epel-release
   
   rpm -v --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
   rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
   
   yum install ffmpeg ffmpeg-devel
   ```

2. `hoshino/modules`ディレクトリに`genshinkfc`ディレクトリを入れます

3. `hoshino/config/__bot__.py`ファイルを開き、`MODULES_ON`集合に`genshinkfc`を入力して保存します

4. HoshinoBotを再起動します

## コマンド

|     コマンド     |                             説明                             |
| :--------------: | :----------------------------------------------------------: |
|       KFC        | 大文字も小文字もいいです、しかしアルファベットが全て大文字または全て小文字のことは必要です |
|     原神KFC      |                             同上                             |
|    二次元KFC     |                             同上                             |
| 异世相遇尽享美味 |                                                              |

## 原文

ねねね，服务员おにいちゃん~~

えっとねえっとね，わたし就是那个，二次元です~~

二次元的美好，みなさん都知道的吧！

だから，人家ほしい~~

对，那个二次元的徽章~~

おねがい，わたしすごくすきすきだ，すき那个徽章~~

なに？一定要那个口号吗？呜呜呜，はずかしい……

でも，为了超级想要的二次元徽章……わたし会がんばって！

**异世相遇，尽享美味！**

ありがとうおにいちゃん，だいすきです！

## 原文（顔文字と動作描写付き）

ねねね，服务员おにいちゃん(>ω<)~~（歯が浮く）

えっとねえっとね，わたし就是那个，二次元です(｡ò ∀ ó｡)~~（したり顔で）

二次元的美好，みなさん都知道的吧！(≧∇≦)/（向き直って大声で客とこの話をする）

だから，人家ほしい~~

对，那个二次元的徽章~~

おねがい(;｀O´)o，わたしすごくすきすきだ，すき那个徽章~~

なにヾ(Ő∀Ő๑)ﾉ？一定要那个口号吗,,Ծ^Ծ,,？呜呜呜，はずかしい……

でも，为了超级想要的二次元徽章……わたし会がんばって(>﹏<)！

异世相遇(>ω<)，（くるくる回る）尽享美味(\*≧ｍ≦\*)！（回りを止め、跳ね、左手を腰に当て、店員に右手で手まねをする）

ありがとうおにいちゃん，だいすきです！

## 原文（漢字を仮名へ翻字する）

ねねね、ふうゆえんおにいちゃん~~

えっとねえっとね、わたしじゅしねいご、ああつゆえんです~~

ああつゆえんでめいはお、みなさんどうじだおでば！

だから、れんじゃほしい~~

どい、ねいごああつゆえんでふいじゃん~~

おねがい、わたしすごくすきすきだ、すきねいごふいじゃん~~

なに？いでぃんやおねいごこうはおま？ううう、はずかしい……

でも、うえいれちゃおじしゃんやおでああつゆえんふいじゃん……わたしふいがんばって！

**いししゃんゆ、じんしゃんめいうえい！**

ありがとうおにいちゃん、だいすきです！

## 原文（ローマ字化）

Nenene, fuwuyuan oniichan~~

Ettone ettone, watashi jiushi neige, erciyuan desu~~

Erciyuan de meihao, minasan dou zhidao de ba!

Dakara, renjia hoshii~~

Dui, neige erciyuan de huizhang~~

Onegai, watashi sugoku suki suki da, suki neige huizhang~~

Nani? Yiding yao neige kouhao ma? Wuwuwu, hazukashii......

Demo, weile chaoji xiangyao de erciyuan huizhang......Watashi hui ganbatte!

**Yishi xiangyu, jinxiang meiwei!**

Arigatou oniichan, daisuki desu!
