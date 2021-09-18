# wordcloud-hoshino
感谢othinus001做出的指令优化和功能添加，终于可以分群查询词云了<br> 
指令 `生成今日词云` `生成昨日词云`可以查询本群词云，<br>
指令`查询某月某日词云`可以查询全服词云
可以查询单独群内的词云也可以查询公共的词云<br> 
对指令，单字，语气词进行剔除，如需增加不需要的词汇请在tyc.txt自己新开一行加<br> 
使用前请先确保你的gocq允许保存聊天记录（info)<br> 
并安装wordcloud库和jieba库<br>
## 部署方法<br>
1.新建一个文件夹wordcloud在里面`git clone https://github.com/erweixi/wordcloud-hoshino.git`<br>
2.修改里面路径和QQ号<br>
3.将tyc.txt和ttf字体文件丢进load_path并安装字体<br> 
tyc里是不想要的词，可以自己一行一行加<br> 

