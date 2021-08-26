# 5000choyen
适用hoshino的5000兆円欲しい! style图片生成器插件

在[SAGIRI-kawaii](https://github.com/SAGIRI-kawaii)大佬的 Graia-Saya [插件](https://github.com/SAGIRI-kawaii/saya_plugins_collection/tree/master/modules/5000zhao)基础上修改而来的适用hoshino的5000兆円欲しい! style图片生成器插件。

## 配置

5000choyen文件夹放进module文件夹，__bot__.py增加5000choyen配置

~~需要自己找到想用的字体文件，并配置generator.py下upper_font_path（上半句字体）和downer_font_path（下半句字体）变量！我调试用的默认字体是经典粗黑简和方正粗宋简体，字体文件以防万一就没放进来（版权流氓惹不起.jpg），可以自己找下，也可以自己换喜欢的用~~

8.18更新：项目现在已自带谷歌开发的[Noto](https://www.google.com/get/noto/)开源免费字体作为默认字体，如有需要也可自行配置换成自己喜欢的字体。

----

（不同字体设置相同字号draw.text画出来的实际大小也不同，默认参数是参照默认字体调整的，换别的字体会有一定的偏差，如果换自己的字体建议根据自行按需调整相应参数以达到最佳效果。）

如字体显示不全请在[这里](https://github.com/pcrbot/5000choyen/blob/8f76d7efa95be60a02a293b7054c654413c9d078/generator.py#L141)调整字号缩放参数，如渐变色范围有误请在[这里](https://github.com/pcrbot/5000choyen/blob/9ced92cb045dc4c132c7e9ee1c0f65345adda459/generator.py#L63)调整渐变色位置参数。

----

默认字体默认参数生成效果，仅供参考：
![temp](https://user-images.githubusercontent.com/55473115/129829256-da258563-23c9-4aa9-9ba2-0a76f6a445be.png)

## 用法

使用方法：发送“5000兆元 (上半句)|(下半句)”
