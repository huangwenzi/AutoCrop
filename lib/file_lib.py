import os
import platform
sysstr = platform.system()

# 文件操作

# 文件类
class FileObj():
    file_name = ""  # 文件名
    file_key = ""   # 文件key 去掉前面目录
    file_path = ""  # 文件地址
    mtime = 0       # 文件更新时间
    
    def __init__(self, file_name, file_key, file_path):
        self.file_name = file_name
        self.file_key = file_key
        self.file_path = change_path_of_sys(file_path)
        self.mtime = os.stat(self.file_path).st_mtime
        
## 获取函数
# 获取文件名
def get_file_name(path):
    begin_idx = 0
    if sysstr == "Windows":
        begin_idx = path.rfind("\\") + 1
    else:
        begin_idx = path.rfind("/") + 1
    end_idx = path.rfind(".")
    return path[begin_idx:end_idx]
        
## 检查函数

        
        
        
## 修改函数  
# 根据系统转换斜杆
def change_path_of_sys(path):
    if sysstr == "Windows":
        return path.replace('/', '\\')
    else:
        return path.replace('\\', '/')


    
