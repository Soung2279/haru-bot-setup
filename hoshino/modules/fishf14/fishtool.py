from .fishdata import fishinfo, areainfo
from . import sv


def find(target, dictData):
    ''' 查找单个键 '''
    queue = [dictData]
    while len(queue) > 0:
        data = queue.pop()
        for key, value in data.items():
            if key == target:
                return value
            elif type(value) == dict:
                queue.append(value)
    return '没找到'


def findAll(target, dictData):
    ''' 有多个同名键在字典里时，可以用这个方法 '''
    queue = [dictData]
    result = []
    notFound = []
    while len(queue) > 0:
        data = queue.pop()
        for key, value in data.items():
            if key == target:
                result.append(value)
            elif type(value) == dict:
                queue.append(value)
    if not result:
        result = notFound
    return result


class Fish:
    def __init__(self):
        self.fishlist = fishinfo
        self.arealist = areainfo

    def search_fish(self, fishname):
        try:
            result = self.fishlist[fishname]
            time = result['time']
            weather = result['weather']
            is_king = result['is_king'] if result['is_king'] != '' else '否'
            tug = result['tug']
            folklore = result['folklore']
            hookset = result['hookset']
            pweather = result['pweather']
            fish_eyes_skill = result['fish_eyes_skill']
            collect = result['collect']
            gyotaku = result['gyotaku']
            aquarium = result['aquarium']
            double_hooking = result['double_hooking']
            baits = ''
            for v in result['baits']:
                baitname = v['baitname']
                probability = v['probability']
                baits += f'{baitname}：{probability}，'
            areas = '，'.join(str(v) for v in result['areas'])
            msg = f'''
名称：{fishname}
时间：{time}
竿型：{tug}
鱼王：{is_king}
挂钩技能：{hookset}
鱼眼技能：{fish_eyes_skill}
传承录：{folklore}
鱼拓：{gyotaku}
水族箱：{aquarium}
收藏品：{collect}
双重提勾：{double_hooking}
前置天气：{pweather}
天气：{weather}
区域：{areas}
选饵：{baits}
'''.strip()
            return msg
        except Exception as ex:
            sv.logger.error(ex)
            return None

    def search_area(self, areaname):
        result = find(areaname, self.arealist)
        if isinstance(result, str):
            sv.logger.info('area is string')
            return None
        elif isinstance(result, dict):
            msg = ''
            for index in result:
                area_name = result[index]['area_name']
                level = result[index]['level']
                fishinfo = '，'.join(result[index]['fishs'])
                msg += f'''
钓场：{area_name}
等级：{level}
种类：{fishinfo}
===========>
                '''
            return msg
        else:
            sv.logger.info(type(result))
            return None
