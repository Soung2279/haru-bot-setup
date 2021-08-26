# aichat
该项目源自https://github.com/pcrbot/Hoshino-plugin-transplant/tree/master/aichat
由于此项目使用的旧api已无法使用，所以用新api重写一下

## 使用说明

在 https://console.cloud.tencent.com/nlp/openconfirm 页面开通服务

在 https://console.cloud.tencent.com/cam/capi 页面创建密钥

在 `aichat.py`中填入你的`SecretId`和`SecretKey`

使用 `pip install --upgrade tencentcloud-sdk-python`指令安装依赖

把文件夹放入`modules`中并在`__bot__.py`中添加该插件