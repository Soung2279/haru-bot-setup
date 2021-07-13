# coding=utf-8
from .majsoul_Spider import *
import json,os
import base64
from PIL import ImageFont,ImageDraw,Image
from io import BytesIO


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

def chooseID(IDdata):
    message = ""
    for i in range(0,len(IDdata)):
        message = message + "【" + str(i+1) + "】"+str(IDdata[i]["nickname"])+"("+judgeLevel(str(IDdata[i]["level"]["id"]))+")\n"
    message = message + "若列表内没有您要找的昵称，请将昵称补全以便于查找"
    return message


def printBasicInfo(IDdata,room_level,num):
    message = "PS：本数据不包含金之间以下对局以及2019.11.29之前的对局\n"
    message = message + "昵称：" + str(IDdata["nickname"])+"  "
    score = int(IDdata["level"]["score"])+int(IDdata["level"]["delta"])
    message = message + processLevelInfo(score,str(IDdata["level"]["id"]))
    if num == "4":
        data_list = selectInfo(IDdata["id"],room_level)
        room = "四"
    else:
        data_list = select_triInfo(IDdata["id"], room_level)
        room = "三"
    if isinstance(data_list[0], urllib.error.URLError):
        message = message + "\n没有查询到在" + room + "人南的对局数据呢~\n"
    else:
        message = message + processBasicInfo(data_list[0], room_level, room + "人南",num)+"\n"
    if isinstance(data_list[2], urllib.error.URLError):
        message = message + "\n没有查询到在" + room + "人东的对局数据呢~\n"
    else:
        message = message + processBasicInfo(data_list[2], room_level, room + "人东",num)+"\n"
    pic = ImgText(message)
    return pic.draw_text()


def printExtendInfo(IDdata,room_level,num):
    message = "PS：本数据不包含金之间以下对局以及2019.11.29之前的对局\n"
    message = message + "昵称：" + str(IDdata["nickname"]) + "  "
    score = int(IDdata["level"]["score"]) + int(IDdata["level"]["delta"])
    message = message + processLevelInfo(score, str(IDdata["level"]["id"]))
    if num == "4":
        data_list = selectInfo(IDdata["id"],room_level)
        room = "四"
    else:
        data_list = select_triInfo(IDdata["id"], room_level)
        room = "三"
    if isinstance(data_list[0], urllib.error.URLError):
        message = message + "\n没有查询到在"+ judgeRoom(room_level) + room + "人南的对局数据呢~\n"
    else:
        message = message + processBasicInfo(data_list[0], room_level, room +"人南",num)
        message = message + processExtendInfo(data_list[1], room_level, room +"人南")
    if isinstance(data_list[2], urllib.error.URLError):
        message = message + "\n没有查询到在"+ judgeRoom(room_level) + room +"人东的对局数据呢~\n"
    else:
        message = message + processBasicInfo(data_list[2], room_level, room +"人东",num)
        message = message + processExtendInfo(data_list[3], room_level, room +"人东")
    pic = ImgText(message)
    return pic.draw_text()

def printRecordInfo(IDdata,num):
    message = "PS：本数据不包含金之间以下对局以及2019.11.29之前的对局\n"
    message = message + "昵称：" + str(IDdata["nickname"]) + "  "
    score = int(IDdata["level"]["score"]) + int(IDdata["level"]["delta"])
    message = message + processLevelInfo(score, str(IDdata["level"]["id"]))
    record = selectRecord(IDdata["id"])
    if isinstance(record, urllib.error.URLError):
        message = message + "没有查询到在该玩家近期的对局数据呢~\n"
    else:
        message = message + processRecordInfo(record,num)
    pic = ImgText(message)
    return pic.draw_text()

def processExtendInfo(info,room_level,sessions):
    data = json.loads(info)
    message = "\n【" + judgeRoom(room_level)+ sessions + "进阶数据】\n"
    message = message + "和牌率：" + str(round(float(removeNull(data["和牌率"]))*100,2)) + "%  "
    message = message + "自摸率：" + str(round(float(removeNull(data["自摸率"]))*100,2)) + "%  "
    message = message + "默听率：" + str(round(float(removeNull(data["默听率"]))*100,2)) + "%  "
    message = message + "放铳率：" + str(round(float(removeNull(data["放铳率"]))*100,2)) + "%  \n"
    message = message + "副露率：" + str(round(float(removeNull(data["副露率"]))*100,2)) + "%  "
    message = message + "立直率：" + str(round(float(removeNull(data["立直率"]))*100,2)) + "%  "
    message = message + "流局率：" + str(round(float(removeNull(data["副露率"]))*100,2)) + "%  "
    message = message + "流听率：" + str(round(float(removeNull(data["流听率"]))*100,2)) + "%  \n"
    message = message + "一发率：" + str(round(float(removeNull(data["一发率"]))*100,2)) + "%  "
    message = message + "里宝率：" + str(round(float(removeNull(data["里宝率"]))*100,2)) + "%  "
    message = message + "先制率：" + str(round(float(removeNull(data["先制率"]))*100,2)) + "%  "
    message = message + "追立率：" + str(round(float(removeNull(data["追立率"]))*100,2)) + "%  \n"
    message = message + "平均打点：" + str(removeNull(data["平均打点"])) + "  "
    message = message + "平均铳点：" + str(removeNull(data["平均铳点"])) + "  "
    message = message + "最大连庄：" + str(removeNull(data["最大连庄"])) + "  "
    message = message + "和了巡数：" + str(round(float(removeNull(data["和了巡数"])),2)) + "  \n"
    return message

def processBasicInfo(info,room_level,sessions,num):
    data = json.loads(info)
    message = "\n【" + judgeRoom(room_level)+ sessions + "基础数据】\n"
    message = message + "总场次：" + str(data["count"])+"\n"
    message = message + "一位率：" + str(round(float(data["rank_rates"][0])*100,2)) + "%  "
    message = message + "二位率：" + str(round(float(data["rank_rates"][1])*100,2)) + "%  \n"
    message = message + "三位率：" + str(round(float(data["rank_rates"][2])*100,2)) + "%  "
    if num=="4":
        message = message + "四位率：" + str(round(float(data["rank_rates"][3])*100,2)) + "%"
    return message

def processLevelInfo(score,level):
    message = ""
    intlevel = int(level)
    if score < 0:
        if intlevel % 10 ==1:
            intlevel = intlevel-98
            level = str(intlevel)
        else:
            level = str(intlevel-1)
        score = level_start(level)
    elif score >= level_max(level):
        if intlevel % 10 == 3:
            intlevel = intlevel+98
            level = str(intlevel)
        else:
            level = str(intlevel+1)
        score = level_start(level)
    message = message + "当前段位：" + judgeLevel(level)+"  "
    message = message + "当前pt数：" + str(score)+"\n"
    return message

def processRecordInfo(record,num):
    data = json.loads(record)
    message = "\n该玩家最近五场对局信息如下：\n"
    for i in range(0,5):
        message = message + "\n【" + str(i+1) + "】牌谱ID：" + str(data[i]["uuid"]) +"\n"
        for j in range(0,num):
            message = message + str(data[i]["players"][j]["nickname"]) + "(" + str(data[i]["players"][j]["score"])+")  "
        message = message + "\n"
        message = message + "对局开始时间：" + str(convertTime(data[i]["startTime"]))+"  "
        message = message + "对局结束时间：" + str(convertTime(data[i]["endTime"]))+"  \n"
    return message

def judgeLevel(level):
    if level == "10203" or level == "20203": return "雀士三"
    elif level == "10301" or level == "20301": return "雀杰一"
    elif level == "10302" or level == "20302": return "雀杰二"
    elif level == "10303" or level == "20303": return "雀杰三"
    elif level == "10401" or level == "20401": return "雀豪一"
    elif level == "10402" or level == "20402": return "雀豪二"
    elif level == "10403" or level == "20403": return "雀豪三"
    elif level == "10501" or level == "20501": return "雀圣一"
    elif level == "10502" or level == "20502": return "雀圣二"
    elif level == "10503" or level == "20503": return "雀圣三"
    elif level == "10601" or level == "20601": return "魂天"

def judgeRoom(room_level):
    if room_level == "0": return "总体"
    elif room_level == "1": return "金之间"
    elif room_level == "2": return "玉之间"
    elif room_level == "3": return "王座之间"

def removeNull(data):
    if data == None:
        return "0"
    else:
        return data

def convertTime(datatime):
    timeArray = time.localtime(datatime)
    Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return Time

def level_max(level):
    if level == "10203" or level == "20203": return 1000
    elif level == "10301" or level == "20301": return 1200
    elif level == "10302" or level == "20302": return 1400
    elif level == "10303" or level == "20303": return 2000
    elif level == "10401" or level == "20401": return 2800
    elif level == "10402" or level == "20402": return 3200
    elif level == "10403" or level == "20403": return 3600
    elif level == "10501" or level == "20501": return 4000
    elif level == "10502" or level == "20502": return 6000
    elif level == "10503" or level == "20503": return 9000
    elif level == "10601" or level == "20601": return 9999999

def level_start(level):
    if level == "10203" or level == "20203": return 500
    elif level == "10301" or level == "20301": return 600
    elif level == "10302" or level == "20302": return 700
    elif level == "10303" or level == "20303": return 1000
    elif level == "10401" or level == "20401": return 1400
    elif level == "10402" or level == "20402": return 1600
    elif level == "10403" or level == "20403": return 1800
    elif level == "10501" or level == "20501": return 2000
    elif level == "10502" or level == "20502": return 3000
    elif level == "10503" or level == "20503": return 4500
    elif level == "10601" or level == "20601": return 10000
