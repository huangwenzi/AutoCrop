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
def get_file_name_and_suffix(path):
    begin_idx = 0
    if sysstr == "Windows":
        begin_idx = path.rfind("\\") + 1
    else:
        begin_idx = path.rfind("/") + 1
    end_idx = path.rfind(".")

    return path[begin_idx:end_idx], path[end_idx:]

# 获取文件目录
def get_file_dir(path):
    end_idx = 0
    if sysstr == "Windows":
        end_idx = path.rfind("\\")
    else:
        end_idx = path.rfind("/")
    
    return path[:end_idx]

# 通过目录地址获取文件列表
def get_file_name_by_dir(dirname):
    file_list = []
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            tmp_file_path = os.path.join(root, name)
            file_list.append(tmp_file_path)
    return file_list
        
## 检查函数

        
        
        
## 修改函数  
# 根据系统转换斜杆
def change_path_of_sys(path):
    if sysstr == "Windows":
        return path.replace('/', '\\')
    else:
        return path.replace('\\', '/')

# 创建目录
def crate_dir(path):
    path = change_path_of_sys(path)
    path_dir = get_file_dir(path)
    # 目录是否存在
    if path_dir != "" and not os.path.exists(path_dir):
        os.makedirs(path_dir)


def save_imaae(image_path, skip_region, im1):
    # 保存图片
    image_name,_suffix_name = get_file_name_and_suffix(image_path)
    save_dir_path = "./处理完毕/%s"%(image_name)
    if not os.path.exists(save_dir_path):
        os.makedirs(save_dir_path)
    for tmp_region in skip_region:
        # 范围是否有效
        if tmp_region[0] == tmp_region[2] or tmp_region[1] == tmp_region[3]:
            continue
        # 跳过面积过小的图像
        if (tmp_region[2] - tmp_region[0]) * (tmp_region[3] - tmp_region[1]) < 5*5:
            continue
        save_path = "./处理完毕/%s/_%d_%d.png"%(image_name, tmp_region[0], tmp_region[1])
        im_crop = im1.crop(tmp_region)
        im_crop.save(save_path)