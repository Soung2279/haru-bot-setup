from typing import List, Set

MAX_PERFORMANCE_PERCENT: List[int] = [90,90,90] # 自检功能中的服务器占用比率最高值，顺序分别对应CPU、内存和硬盘
PROCESS_NAME_LIST: Set[str] = {} # 自检功能里需要提供的格外检查的进程名
