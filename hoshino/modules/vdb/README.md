# VTuber名单查询

→→ [查看更新](#更新日志)

*****

## 简介

基于 [VTuber Database](https://github.com/dd-center/vdb) 的名单查询功能，适用于 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)。

利用整理好的 [VDB - JSON](https://vdb.vtbs.moe/json/list.json) 文件重新生成便于查询的词典供bot使用

在已收录的名单中查询某人是否为 **VTuber / VUP**（虚拟主播），（如果是）并给出相关信息。

可模糊匹配名字

![example_for_vdb.jpg](https://i.loli.net/2021/09/21/7SFfHZ1geMIADw5.jpg)

不知道 **VTuber / VUP** 是什么？

→[百度一下-vtuber](https://www.baidu.com/s?wd=vtuber)←

→[Bing一下-vtuber](https://cn.bing.com/search?q=vtuber)←

→[Google一下-vtuber](https://google.com/search?q=vtuber)←

*****

## 安装
- **步骤一** : 直接下载/克隆本项目，将文件夹放入 ``hoshino/modules`` 路径下, 在 ``hoshino/config/__bot__.py`` 里的 ``MODULES_ON`` 中添加 "vdb"

```python
# 启用的模块
MODULES_ON = {
    'xxx',
    'vdb',  #注意英文逗号
    'xxx',
}
```

- **步骤二(可忽略)** : 检查当前文件夹下有无 ``list.json`` 和 ``vdb.json`` 两个文件

若有，重启 ``HoshinoBot`` 则可直接开始使用。

**若无，请按照以下步骤操作。**

→[简短版说明](#手动更新)←

- 1. 将 ``update.sample`` 文件的**后缀名**改为 ``.py``

- 2. 在当前路径下打开 ``cmd`` 或 ``powershell``，输入下列代码运行 ``update.py``

```python
py update.py
```
> 如果有错误信息，请复制到百度等搜索引擎查看
> 如果出现 *[WinError 10054]* 报错字样，请等待一会儿或手动重置网络环境后，重新运行。

- 3. 运行完成后，检查当前文件夹下有无 ``list.json`` 和 ``vdb.json`` 两个文件

若有：

- 将 ``update.py`` 文件的**后缀名**改为 ``.sample`` (或任意名)

- 打开 ``vdb.json`` 文件，**查找所有的 “}{” ，替换为英文逗号 “,”**

> ~~如果你不是很在意Notepad++作者的政治立场~~，可使用 Notepad++ 打开该文件，Ctrl+F 进行批量查找和替换
> 注意：只需要查找 “}{” 就可以了，不是所有的括号都需要进行替换。

若无：检查报错信息，重新运行

重启 ``HoshinoBot`` 则可直接开始使用。


*****

## 指令表

- **查询vtb/查询虚拟主播+名字** ：根据名字查询是否为vtb，可模糊匹配

- **检查vtb名单** ：检查本地文件收录情况

- **帮助vtb名单/帮助vdb** ：查看指令列表

*****

## 额外说明

在 ``vdb.py`` 的第29、30行，填写 ``list.json`` 和 ``vdb.json`` 两个文件的路径（默认已填好）

```python
JSON_VDB = "./hoshino/modules/vdb/vdb.json"  #此处填写 vdb.json 文件路径
JSON_LIST = "./hoshino/modules/vdb/list.json"  #此处填写 list.json 文件路径
```

如果要进行后续更新，除了查看本仓库更新以外，插件还提供**手动更新**，更新方式同 **安装-步骤二**

##### 手动更新

- 重命名 ``update.sample`` 为 ``update.py``

- 运行 ``update.py``

- 将 ``vdb.json`` 里的所有的 ``}{`` 替换为 ``,``

- 还原命名 ``update.sample``

*****

### 其它

本人非专业程序员，业余写着玩玩，代码很菜，大佬们看看就好QwQ。

made by [Soung2279@Github](https://github.com/Soung2279/)

### 鸣谢

[HoshinoBot项目地址](https://github.com/Ice-Cirno/HoshinoBot)

[VTuber Database项目地址](https://github.com/dd-center/vdb)

### 更新日志

##### 2021/9/21

首次上传

完善文件检查功能，文件路径作 Linux 适配

##### 2021/9/20

完善查询功能

添加模糊匹配功能
