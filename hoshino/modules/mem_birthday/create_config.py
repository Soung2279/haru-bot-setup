import yaml

# 创建Data，并加入群组数据
async def create_yml(_bot, _current_dir):
    glist_info = await _bot.get_group_list()
    data = {'Info': {}}
    for each_g in glist_info:
        group_id = each_g['group_id']
        data['Info'].setdefault(group_id,[])
        data = await write_info(_bot, data, group_id)
    with open(_current_dir, "w", encoding="UTF-8") as f:
        yaml.dump(data, f,allow_unicode=True)

# 加上个人数据后写入文件，若隐藏生日显示则为0
async def write_info(_bot, data, gid):
    '''
    Q：为什么要获取 member_list 再查一遍 stranger_info 呢？

    A：
    这里对于go-cqhttp的小可爱可能就是无用步骤了，
    但是对于部分因为 mirai-native 的原 酷Q用户来说，dll 类型的插件从酷Q用到现在一直不想换掉。
    但是 cqhttp-mirai 也就是现在的 onebot-mirai 的作者，
    非常忙以至于没时间更新 onebot-mirai ，所以未跟进 mirai v2.1 后的部分API
    仔细翻阅 Issue 后发现 0.3.5 版本虽然暂未发布(不知道他要啥时候发)，但其不完全的版本已经实现了
    用 stranger_info 获取年龄和性别的API，才有这么一步对 onebot-mirai 来说不可或缺的多余步骤
    '''
    group_info = await _bot.get_group_member_list(group_id = gid, no_cache = True)
    for each_mem in group_info:
        uid = each_mem['user_id']
        # 这个区间的几个B是QQ自己的机器人，不会有人还用这个机器人吧
        if uid < 2854196300 or uid > 2854196399:
            mem_info = await _bot.get_stranger_info(user_id = uid, no_cache = True)
            age = mem_info['age']
            mem_data = {
                'member':{
                    'user_id': uid,
                    'yes_age': age, 
                    'tod_age': age
                }
            }
            data['Info'][gid].append(mem_data)
    return data
