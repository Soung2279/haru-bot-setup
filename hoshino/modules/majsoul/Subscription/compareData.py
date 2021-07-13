from .RecordLoader import *
import base64
from PIL import ImageFont,ImageDraw,Image
from io import BytesIO
import json,os

FILE_PATH = os.path.dirname(os.path.dirname(__file__))

class ImgText:
    FONTS_PATH = os.path.join(FILE_PATH,'fonts')
    FONTS = os.path.join(FONTS_PATH,'msyh1.otf')
    font = ImageFont.truetype(FONTS, 14)
    def __init__(self, text):
        # 预设宽度 可以修改成你需要的图片宽度
        self.width = 600
        # 文本
        self.text = text
        # 段落 , 行数, 行高
        self.duanluo, self.note_height, self.line_height, self.drow_height = self.split_text()
    def get_duanluo(self, text):
        txt = Image.new('RGBA', (400, 800), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 0
        for char in text:
            width, height = draw.textsize(char, ImgText.font)
            sum_width += width
            if sum_width > self.width: # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count
    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_duanluo(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        drow_height = total_lines * line_height
        return allText, total_height, line_height, drow_height
    def draw_text(self):
        """
        绘图以及文字
        :return:
        """
        im = Image.new("RGB", (600, self.drow_height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        # 左上角开始
        x, y = 0, 0
        for duanluo, line_count in self.duanluo:
            draw.text((x, y), duanluo, fill=(0, 0, 0), font=ImgText.font)
            y += self.line_height * line_count
        bio  = BytesIO()
        im.save(bio, format='PNG')
        base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
        mes  = f"[CQ:image,file={base64_str}]"
        return mes


def updateData(record,gid,id):
    localdata = localLoad()
    data = json.loads(record)
    datalist = []
    message = ""
    for i in range(0,len(localdata)):
        if data[0]["uuid"] != localdata[i]["uuid"] and gid == localdata[i]["gid"] and localdata[i]["id"] == id:
            localdata[i]["uuid"] = data[0]["uuid"]
            localdata[i]["endTime"] = data[0]["endTime"]
            if localdata[i]["record_on"]:
                message = message + processdata(data,4)
        datalist.append(localdata[i])
    with open(join(path,'account.json'),'w',encoding='utf-8') as fp:
        json.dump(datalist,fp,indent=4)
    return message

def updateTriData(record,gid,id):
    localdata = localTriLoad()
    data = json.loads(record)
    datalist = []
    message = ""
    for i in range(0,len(localdata)):
        if data[0]["uuid"] != localdata[i]["uuid"] and gid == localdata[i]["gid"] and localdata[i]["id"] == id:
            localdata[i]["uuid"] = data[0]["uuid"]
            localdata[i]["endTime"] = data[0]["endTime"]
            if localdata[i]["record_on"]:
                message = message + processdata(data,3)
        datalist.append(localdata[i])
    with open(join(path,'tri_account.json'),'w',encoding='utf-8') as fp:
        json.dump(datalist,fp,indent=4)
    return message

def processdata(data,num):
    message = "本群侦测到新的对局："
    message = message + "\n牌谱ID：" + str(data[0]["uuid"]) + "\n"
    for j in range(0, num):
        message = message + str(data[0]["players"][j]["nickname"]) + "(" + str(data[0]["players"][j]["score"]) + ")  "
    message = message + "\n"
    message = message + "对局开始时间：" + str(convertTime(data[0]["startTime"])) + "  "
    message = message + "对局结束时间：" + str(convertTime(data[0]["endTime"])) + "  \n"
    pic = ImgText(message)
    return pic.draw_text()

def convertTime(datatime):
    timeArray = time.localtime(datatime)
    Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return Time

def selectNickname(id):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳
    basicurl = baseurl + "/player_stats/" + str(id) + "/1262304000000/" + urltime + "?mode=16.12.9.15.11.8"
    data = getURL(basicurl)
    if isinstance(data,urllib.error.URLError):
        return -1
    else:
        nickname = str(json.loads(data)["nickname"])
    return nickname

def selectTriNickname(id):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳
    basicurl = tribaseurl + "/player_stats/" + str(id) + "/1262304000000/" + urltime + "?mode=22.24.26.21.23.25"
    data = getURL(basicurl)
    if isinstance(data,urllib.error.URLError):
        return -1
    else:
        nickname = str(json.loads(data)["nickname"])
    return nickname
