# eqa
可用于nonebot或者hoshino的问答插件

eqa文件夹复制到nonebot的模块目录就可

然后配置启用的模块添加 'eqa'

> 需要安装依赖
>
> pip install pyyaml -i https://pypi.tuna.tsinghua.edu.cn/simple
>
> pip install sqlitedict -i https://pypi.tuna.tsinghua.edu.cn/simple
---
### 默认规则如下
> 可以通过修改`config.yaml`文件改变以下配置
1. 非超级管理员问答分群设置和显示
2. 超级管理员设置的问题为全群
3. 只允许群管理或者超级管理员删除别人的问题
4. 群管理不允许删除超级管理员设置的问题
5. 删除回答时只删除一个 并且是最近设置的问题
6. 如果是管理员或者超级管理员删除回答时直接删除最近的一个
7. 只允许超级管理员清空一个问题的全部回答
8. 多个回答时 将优先自己的回答 如果自己的回答多个时则随机自己的回答
9. 群员可以查看别人设置的问答
10. 支持@某人作为问题
11. 支持图片作为问题
12. 支持命令作为回答
13. 支持正则表达式（默认配置下R作为前缀）

---
### 例子： 设置在默认的情况下
##### 设置一个问题：
- 大家说111回答222
- 我说333回答444
- 大家说@某人回答图1图2 文字
- 大家说图片回答图片
- 有人说R测试回答test


##### 查看个人设置的问题：
- 问答
- 问答@某人@某人2

##### 删除一个问答：
- 不要回答111

##### 清空一个问答：
- 清空回答111

##### 显示本群所有的问答：
- 全部问答
- 所有问答
