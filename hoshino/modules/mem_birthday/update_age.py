import os 
import yaml

# 获取文件中的数据并删除旧版数据
def get_tod(gid, uid):
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    for user in config['Info'][gid]:
        user_id = int(user['member']['user_id'])
        if user_id == uid:
            yes_age = int(user['member']['yes_age'])
            tod_age = int(user['member']['tod_age'])
            mem_data = {
                'member':{
                    'user_id': uid,
                    'yes_age': yes_age, 
                    'tod_age': tod_age
                }
            }
            config['Info'][gid].remove(mem_data)
            return current_dir, config, tod_age

# 写入新的数据，将tod_age移到yes_age
async def repalce_age(bot, gid):
    group_info = await bot.get_group_member_list(group_id = gid, no_cache = True)
    for each_mem in group_info:
        uid = each_mem['user_id']
        # 这个区间的几个B是QQ自己的机器人，不会有人还用这个机器人吧
        if uid < 2854196300 or uid > 2854196399:
            current_dir, config, yes_age = get_tod(gid, uid)
            mem_info = await bot.get_stranger_info(user_id = uid, no_cache = True)
            age = mem_info['age']
            mem_data = {
                'member':{
                    'user_id': uid,
                    'yes_age': yes_age, 
                    'tod_age': age
                }
            }
            config['Info'][gid].append(mem_data)
            with open(current_dir, "w", encoding="UTF-8") as f:
                yaml.dump(config, f,allow_unicode=True)
