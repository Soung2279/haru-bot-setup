# coding=utf-8
from bs4 import BeautifulSoup
from os.path import dirname,join
import urllib.request
import urllib.error
import urllib.parse
import json
import time

baseurl = "https://ak-data-2.sapk.ch/api/v2/pl4"
tribaseurl = "https://ak-data-2.sapk.ch/api/v2/pl3"
path = dirname(__file__)


def getURL(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    try:
        response = urllib.request.Request(url=url, headers=headers, method="GET")
        req = urllib.request.urlopen(response,timeout=3)
        info = str(BeautifulSoup(req.read().decode('utf-8'), "html.parser"))
    except urllib.error.URLError as e:
        return e
    return info

def getID(nickname):#获取牌谱屋角色ID
    nickname = urllib.parse.quote(nickname) #UrlEncode转换
    url = baseurl + "/search_player/"+nickname+"?limit=9"
    data = getURL(url)
    if isinstance(data,urllib.error.URLError):
        return -404
    datalist = json.loads(data)
    if datalist == [] :
        return -1
    return datalist

def getTriID(nickname):#获取牌谱屋角色ID
    nickname = urllib.parse.quote(nickname) #UrlEncode转换
    url = tribaseurl + "/search_player/"+nickname+"?limit=9"
    data = getURL(url)
    if isinstance(data,urllib.error.URLError):
        return -404
    datalist = json.loads(data)
    if datalist == [] :
        return -1
    return datalist

def selectRecord(id):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳

    basicurl = baseurl + "/player_stats/" + str(id) + "/1262304000000/" + urltime + "?mode=16.12.9.15.11.8"
    data = getURL(basicurl)
    if isinstance(data , urllib.error.URLError):
        return -1
    count = str(json.loads(data)["count"])
    recordurl = baseurl + "/player_records/"+str(id)+"/"+urltime+"/1262304000000?limit=2&mode=16.12.9.15.11.8&descending=true&tag="+count
    record = getURL(recordurl)
    if isinstance(record , urllib.error.URLError):
        return -1
    return record

def selectTriRecord(id):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳
    basicurl = tribaseurl + "/player_stats/" + str(id) + "/1262304000000/" + urltime + "?mode=22.24.26.21.23.25"
    data = getURL(basicurl)
    if isinstance(data , urllib.error.URLError):
        return -1
    count = str(json.loads(data)["count"])
    recordurl = tribaseurl + "/player_records/"+str(id)+"/"+urltime+"/1262304000000?limit=2&mode=22.24.26.21.23.25&descending=true&tag="+count
    record = getURL(recordurl)
    if isinstance(record , urllib.error.URLError):
        return -1
    return record

def localLoad():
    with open(join(path,'account.json'),encoding='utf-8') as fp:
        data = json.load(fp)
    #print(data[0]["uuid"])
    return data

def localTriLoad():
    with open(join(path,'tri_account.json'),encoding='utf-8') as fp:
        data = json.load(fp)
    return data

def jsonWriter(Record,gid,id):
    localdata = localLoad()
    data = json.loads(Record)
    datalist = []
    for i in range(0,len(localdata)):
        if localdata[i]["gid"] == str(gid) and localdata[i]["id"] == id:
            return False
        datalist.append(localdata[i])
    binds = {
        "id": id,
        "uuid": str(data[0]["uuid"]),
        "endTime": int(data[0]["endTime"]),
        "gid": str(gid),
        "record_on": True,
    }
    datalist.append(binds)
    with open(join(path,'account.json'),'w',encoding='utf-8') as fp:
        json.dump(datalist,fp,indent=4)
    return True

def jsonTriWriter(Record,gid,id):
    localdata = localTriLoad()
    data = json.loads(Record)
    datalist = []
    for i in range(0,len(localdata)):
        if localdata[i]["gid"] == str(gid) and localdata[i]["id"] == id:
            return False
        datalist.append(localdata[i])
    binds = {
        "id": id,
        "uuid": str(data[0]["uuid"]),
        "endTime": int(data[0]["endTime"]),
        "gid": str(gid),
        "record_on": True,
    }
    datalist.append(binds)
    with open(join(path,'tri_account.json'),'w',encoding='utf-8') as fp:
        json.dump(datalist,fp,indent=4)
    return True
