# SoungBot
***
## 邦邦车站查询
**默认文件夹名：bandori**
**默认功能名：邦邦车站查询&邦邦车站推送**
**目录组成如下：**
> modules
>> **bandori**
>>> station.py  #主要运行文件
>>> config.json  #配置文件
>>> README.md  #说明文件
>>> LICENSE  #GPL3.0许可

### 功能介绍

邦邦上车插件。

### 指令

- **`[车站人数]`** 查询邦邦车站在线人数
- **`[查询房间]`** 查询房间
- **`[开启通知]`** 开启通知
- **`[关闭通知]`** 关闭通知

### 可自定义内容

在 **[station.py](hoshino/modules/bandori/station.py)** 文件的第 **15-23** 行可以自行设置 **邦邦车站查询** 的权限

```python
sv1 = Service(
    name = '邦邦车站查询',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv1_help #帮助文本
    )
```

在 **[station.py](hoshino/modules/bandori/station.py)** 文件的第 **34-42** 行可以自行设置 **邦邦车站推送** 的权限

```python
sv2 = Service(
    name = '邦邦车站推送',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv2_help #帮助文本
    )
```

在 **[config.json](hoshino/modules/bandori/config.json)** 文件的第 **1-3** 行添加启用通知的群号

```json
{
    "station_notice": {}
}
```

### 其它

无额外说明。

### 鸣谢

此功能原作者：**[Watanabe-Asa](https://github.com/Watanabe-Asa)**
[原项目地址](https://github.com/Watanabe-Asa/Salmon-BandoriStation)

数据源
[邦邦车牌/房间收集平台](https://github.com/maborosh/BandoriStation)