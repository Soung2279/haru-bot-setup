import psutil
import requests
import os
import time
from datetime import datetime
import hoshino
from hoshino import log

logger = log.new_logger('check')

class Check():
    def __init__(self, request_name_list={}):
        self.request_name_list = request_name_list
        self.cpu_percent = 0
        self.memory_percent = 0
        self.disk_percent = 0
        self.boot_time = 0
        self.send = 0
        self.recv = 0
        self.sent_now = 0
        self.recv_now = 0
        self.unit_now = []
        self.packets_sent = 0
        self.packets_recv = 0
        self.packet_lost = 0
        self.baidu = 404
        self.google = 404
        self.process_name_list = []
        self.process_status_list = []
        self.user_list =[]
        self.run_all_check()

    def run_all_check(self):
        self.get_performance_check()
        self.get_process_status(self.request_name_list)
        self.get_users_check()

    async def get_check_info(self):
        self.run_all_check()
        putline = []
        putline.append("--Performance--\n[Cpu] {}%\n[Memory] {}%\n[Disk] {}%\n[Boot time] {}\n--Network--\n[Send now] {}{}\n[Recv now] {}{}\n[Send all] {}GB\n[Recv all] {}GB\n[Packets sent] {}\n[Packets recv] {}\n[Packets lost] {}%".format(self.cpu_percent, self.memory_percent, self.disk_percent, self.boot_time, self.sent_now, self.unit_now, self.recv_now, self.unit_now, self.send, self.recv, self.packets_sent, self.packets_recv, self.packet_lost))        
        if self.process_name_list:
            putline.append("--Process--")
            for name, status in zip(self.process_name_list, self.process_status_list):
                putline.append("[{}] {}".format(name, status))      
        if self.user_list:
            putline.append("--Users--")
            for user in self.user_list:
                putline.append("[{}] {}".format(user['name'], user['started']))       
        return "\n".join(putline)

    async def get_check_easy(self, max_performance_percent=[92,92,92]):
        self.run_all_check()
        putline = []
        putline.append("当前服务器状态：\nCpu：{}%\n内存：{}%\n丢包率: {}%".format(self.cpu_percent, self.memory_percent, self.packet_lost))
        check_list = await self.get_check_simple()
        if sum(check_list) != 0:
            hoshino.logger.error("System problem detected. check code: {}".format(check_list))
            if sum(check_list) == 5:
                putline.append("※服务器已经安详地去了。")
            if sum(check_list) == 4:
                putline.append("※请检查服务器状态！")
            if sum(check_list[:3]) != 0:
                putline.append("※服务器国内线路异常。")
            if sum(check_list[:4]) != 0:
                putline.append("※服务器国际线路异常。")
            if sum(check_list[3:4]) == 2:
                putline.append("※网络异常。")
        else:
            putline.append("※请留意服务器的网络状态")
        return "\n".join(putline)

    async def get_check_simple(self, max_performance_percent=[92,92,92]) -> list:
        check_list = [0,0,0,0,0]
        self.run_all_check()
        if self.cpu_percent > max_performance_percent[0]:
            check_list[0] = 1
        if self.memory_percent > max_performance_percent[1]:
            check_list[1] = 1
        if self.disk_percent > max_performance_percent[2]:
            check_list[2] = 1
        if self.baidu != 200:
            check_list[3] = 1
        if self.google != 200:
            check_list[4] = 1
        for status in self.process_status_list:
            if status != 'running':
                check_list[4] = 1
                break      
        return check_list

    def get_performance_check(self):
        self.cpu_percent = psutil.cpu_percent()
        self.memory_percent = psutil.virtual_memory().percent
        self.disk_percent = psutil.disk_usage("/").percent
        self.boot_time = datetime.fromtimestamp(
        psutil.boot_time()).strftime("%Y-%m-%d %H: %M: %S")

    def get_users_check(self):
        user_list = []
        suser_l = psutil.users()

        for suser in suser_l:
            user = {
                'name': suser.name, 
                'started': datetime.fromtimestamp(suser.started).strftime("%Y-%m-%d %H:%M:%S")}
            user_list.append(user)

        self.user_list = user_list

    def get_process_status(self, request_name_list: set):
        if not request_name_list:
            return None
        
        self.process_name_list = []
        self.process_status_list = []
        
        for p_n in request_name_list:
            p_l = self.get_sname_process_list(p_n)
            if len(p_l) == 1:
                self.process_name_list.append(p_n)
                self.process_status_list.append(p_l[0].status())
            else:
                for i, p in enumerate(p_l):
                    self.process_name_list.append(p_n+" ({})".format(i))
                    self.process_status_list.append(p.status())

    @staticmethod
    def get_sname_process_list(name: str) -> list:
        p_l = []
        pids  = psutil.pids()

        for pid in pids:
            p = psutil.Process(pid)
            if (p.name() == name):
                p_l.append(p)

        return p_l
