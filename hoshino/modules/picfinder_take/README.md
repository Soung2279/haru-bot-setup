# picfinder_take
个人~~缝合~~修改的Hoshino bot搜图插件。

这个插件的主要思路其实是在hoshino上还原隔壁 [@Tsuk1ko](https://github.com/Tsuk1ko) 大佬家的[竹竹](https://github.com/Tsuk1ko/cq-picsearcher-bot)的搜图交互体验（所以插件名是たけ）

代码主体部分参考了 [@Watanabe-Asa](https://github.com/Watanabe-Asa)大佬的 [搜图](https://github.com/pcrbot/Salmon-plugin-transplant#%E6%90%9C%E5%9B%BE)与 [@Cappuccilo](https://github.com/Cappuccilo)大佬的 [以图搜图](https://github.com/pcrbot/cappuccilo_plugins#%E4%BB%A5%E5%9B%BE%E6%90%9C%E5%9B%BE)，感谢各位大佬的代码）

---

6.1更新：增加私聊搜图、截屏识别和代理功能

6.24更新：增加回复搜图功能，搜图请求更换为异步（感谢 [@蓝红心](https://github.com/LHXnois)大佬）

7.9更新：增加自定义HOST功能，在qiang内又不想用全局代理的用户(?)可以单独为SauceNao和ascii2d配置反代或ip直连）（继续感谢 [@蓝红心](https://github.com/LHXnois)大佬）

7.26更新：回复搜图增加at支持

## 特点  

- 搜索SauceNao，在相似率过低时自动补充搜索ascii2d，相似率阈值可在config中调整。搜索结果显示数量可在config中调整。  

- 解析SauceNao和ascii2d搜索结果的作品详细信息。SauceNao全部42个index格式解析都已完成；ascii2d常见格式应该也能解析，一些奇怪格式的外部登录不敢保证）  

- 获取SauceNao和ascii2d的结果缩略图，缩略图可在config中关闭。  

- 搜图结果可由普通回复切换为合并转发回复，减少刷屏情况。发送模式可在config中调整。

- 增加批量搜图模式，解决移动端文字命令+图片发送麻烦的问题。

- 增加搜图每人每日限额，可在config中调整限额。要懂得节制噢.jpg

- 增加简单的手机截屏识别功能，判断为整屏手机截屏时会拒绝搜索 ~~（你会截你马个图.jpg）~~

- 增加私聊搜图功能，有效缓解腾讯吞图（但反之临时会话下搜索结果大概率被吞无法发送，若要稳定使用需加bot好友）

- 增加代理设置，方便qiang内使用

- New！增加回复搜图功能，可直接对群友发送的图片进行回复搜索，省去转发过程）


## 用法

- 申请并在config中配置SauceNao的API key

- 发送 ``@bot+图片`` 或 ``[bot昵称]搜图+图片`` 进行单张搜索。

- 发送 ``[bot昵称]搜图`` 进入连续搜图模式，连续搜图模式下同一用户所发送所有图片都将直接搜索；

  发送 ``谢谢[bot昵称]`` 退出连续搜图模式，或停止发图等待超时后自动退出连续搜图模式。

- 对他人发送的图片回复 ``@bot 搜图`` 或``[bot昵称]搜图`` 进行回复搜索。

- 私聊下直接发送图片即可进行搜索。
