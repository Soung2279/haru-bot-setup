import websocket
import brotli
import json
import threading
from nonebot import get_bot
import asyncio

clear_list = ['Track Lost', 'Normal Clear', 'Full Recall', 'Pure Memory', 'Easy Clear', 'Hard Clear']
diff_list = ['PST', 'PRS', 'FTR', 'BYD']

f = open('arc_namecache.txt', 'w')
f.close()


def load_cache():
    cache = {}
    f = open('arc_namecache.txt', 'r')
    for line in f.readlines():
        ls = line.replace('\n', '').split(' ')
        cache[ls[0]] = ls[1]
    f.close()
    return cache


def put_cache(d: dict):
    f = open('arc_namecache.txt', 'w')
    for key in d:
        f.write('%s %s\n' % (key, d[key]))


def cmp(a):
    return a['rating']


def calc(ptt, s):
    brating = 0
    for i in range(0, 30):
        try:
            brating += s[i]['rating']
        except IndexError:
            break
    brating /= 30
    rrating = 4 * (ptt - brating * 0.75)
    return brating, rrating


def lookup(nickname: str):
    ws = websocket.create_connection("wss://arc.estertion.win:616/")
    ws.send("lookup " + nickname)
    buffer = ""
    while buffer != "bye":
        buffer = ws.recv()
        if type(buffer) == type(b''):
            obj2 = json.loads(str(brotli.decompress(buffer), encoding='utf-8'))
            id = obj2['data'][0]['code']
            cache = load_cache()
            cache[nickname] = id
            put_cache(cache)
            return id

def query(id: str):
    s = ""
    song_title, userinfo, scores = _query(id)
    b, r = calc(userinfo['rating'] / 100, scores)
    s += "Player: %s\nPotential: %.2f\nBest 30: %.5f\nRecent Top 10: %.5f\n\n" % (userinfo['name'], userinfo['rating'] / 100, b, r)
    score = userinfo['recent_score'][0]
    s += "Recent Play: \n%s  %s %.1f  \n%s\nPure: %d(%d)\nFar: %d\nLost: %d\nScore: %d\nRating: %.2f" % (song_title[score['song_id']]['en'], diff_list[score['difficulty']], score['constant'], clear_list[score['clear_type']],
              score["perfect_count"], score["shiny_perfect_count"], score["near_count"], score["miss_count"], score["score"], score["rating"])
    return s


def best(id: str, num: int):
    if num < 1:
        return []
    if num > 30:
        return []    
    result = []
    s = ""
    song_title, userinfo, scores = _query(id)
    s += "%s's Top %d Songs:\n" % (userinfo['name'], num)
    for j in range(0, int((num - 1) / 15) + 1):
        for i in range(15 * j, 15 * (j + 1)):
            if i >= num:
                break
            try:
                score = scores[i]
            except IndexError:
                break
            s += "#%d  %s  %s %.1f  \n\t%s\n\tPure: %d(%d)\n\tFar: %d\n\tLost: %d\n\tScore: %d\n\tRating: %.2f\n" % (i+1, song_title[score['song_id']]['en'], diff_list[score['difficulty']], score['constant'], clear_list[score['clear_type']],
                  score["perfect_count"], score["shiny_perfect_count"], score["near_count"], score["miss_count"], score["score"], score["rating"])
        result.append(s[:-1])
        s = ""
    return result

def _query(id: str):
    cache = load_cache()
    # print(cache)
    try:
        id = cache[id]
    except KeyError:
        pass
    ws = websocket.create_connection("wss://arc.estertion.win:616/")
    ws.send(id)
    buffer = ""
    scores = []
    userinfo = {}
    song_title = {}
    while buffer != "bye":
        try:
            buffer = ws.recv()
        except websocket._exceptions.WebSocketConnectionClosedException:
            ws = websocket.create_connection("wss://arc.estertion.win:616/")
            ws.send(lookup(id))
        if type(buffer) == type(b''):
            # print("recv")
            obj = json.loads(str(brotli.decompress(buffer), encoding='utf-8'))
            # al.append(obj)
            if obj['cmd'] == 'songtitle':
                song_title = obj['data']
            elif obj['cmd'] == 'scores':
                scores += obj['data']
            elif obj['cmd'] == 'userinfo':
                userinfo = obj['data']
    scores.sort(key=cmp, reverse=True)
    return song_title, userinfo, scores


class QueryThread(threading.Thread):
    def __init__(self, cmd, ctx, bot, state):
        threading.Thread.__init__(self)
        self.operation = cmd.name[0]
        self.ctx = ctx
        self.bot = bot
        self.state = state

    def run(self):
        funcs = []
        if self.operation == 'arcaea':
            try:
                message = query(self.state['id'])
            except Exception as e:
                message = "An exception occurred: %s" % repr(e)
            funcs.append(self.bot.send(self.ctx, message=message))
        elif self.operation == 'best':
            try:
                s = best(self.state['id'], self.state['num'])
            except Exception as e:
                s = ["An exception occurred: %s" % repr(e)]
            for elem in s:
                funcs.append(self.bot.send(self.ctx, message=elem))
        loop = asyncio.new_event_loop()
        loop.run_until_complete(asyncio.wait(funcs))
        loop.close()