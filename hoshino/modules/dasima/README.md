# 大司马发病评论

→→→ [前往更新日志](#更新日志)

*****

## 功能介绍

随机发送大司马B站评论区的**发病评论**，嘿嘿，嘿嘿嘿，金轮我的金轮

无需依赖，安装即用。

## 安装

在 ``hoshino/modules`` 文件夹中，打开 ``cmd`` 或者 ``powershell`` ，输入以下代码 按回车执行：

```powershell
git clone https://github.com/Soung2279/dasima.git
```

之后关闭 ``cmd`` 或 ``powershell`` ，在 ``hoshino/config/__bot__.py`` 文件中， ``MODULES_ON``里添加 "dasima"
```python
# 启用的模块
MODULES_ON = {
    'xxx',
    'dasima',  #注意英文逗号！
    'xxx',
}
```

### 指令

- **发病**  ：随机一条评论
- **注入金轮**  ：(需@bot)每天到达上限次数后重置上限

### 其它

本人非专业程序员，业余写着玩玩，代码很菜，大佬们看看就好QwQ。

made by [Soung2279@Github](https://github.com/Soung2279/)

### 鸣谢

[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)

### 更新日志

##### 2021/8/20

代码重构，优化逻辑，使用 列表 存储评论

##### 2021/7/13

首次上传

