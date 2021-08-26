import importlib
from io import BytesIO

import pygtrie
import requests
from fuzzywuzzy import fuzz, process
from PIL import Image

import hoshino
from hoshino import R, log, sucmd, util
from hoshino.typing import CommandSession

from . import _song_data

logger = log.new_logger('muse_dash_wiki', hoshino.config.DEBUG)
UNKNOWN = 1000

class Roster:

    def __init__(self):
        self._roster = pygtrie.CharTrie()
        self.update()
    

    def update(self):
        importlib.reload(_song_data)
        self._roster.clear()
        for idx, values in _song_data.SONG_DATA.items():
            sname = values[0]  #下标0是字典的歌曲原名
            #hname = values[8]  #下标8是字典的查询名
            n = util.normalize_str(sname)
  
            if n not in self._roster:
                    self._roster[n] = idx
            else:
                    logger.warning(f'MuseDash:chara: 出现重名{n}于id{idx}与id{self._roster[n]}')
                    pass

        self._all_name_list = self._roster.keys()

    def get_id(self, name):
        name = util.normalize_str(name)
        return self._roster[name] if name in self._roster else UNKNOWN


    def guess_id(self, name):
        """@return: id, name, score"""
        name, score = process.extractOne(name, self._all_name_list)#, #processor=util.normalize_str)
        #print(self._roster[name], name, score)
        return self._roster[name], name, score


roster = Roster()

def name2id(name):
    return roster.get_id(name)

def fromid(id_):
    return Chara(id_)

def fromname(name):
    id_ = name2id(name)
    return Chara(id_)

def guess_id(name):
    return roster.guess_id(name)

class Chara:

    def __init__(self, id_):
        self.id = id_

    @property
    def name(self):
        return _song_data.SONG_DATA[self.id][0] if self.id in _song_data.SONG_DATA else _song_data.SONG_DATA[UNKNOWN][0]
