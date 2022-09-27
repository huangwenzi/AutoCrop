import os
import numpy as np
from PIL import Image
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


def save_imaae(image_path, skip_region, im1, data = []):
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
        # tmp_region是[begin_y,begin_x,end_y,end_x]
        # crop是[begin_x,begin_y,end_x,end_y]
        tmp_region_1 = [tmp_region[1],tmp_region[0],tmp_region[3],tmp_region[2]]
        # 保存图片
        save_path = "./处理完毕/%s/_%d_%d.png"%(image_name, tmp_region_1[0], tmp_region_1[1])
        # 是否有占用点
        if len(tmp_region) >= 5:
            # 创建占用数组
            tmp_y = tmp_region[2] - tmp_region[0] + 1
            tmp_x = tmp_region[3] - tmp_region[1] + 1
            dt = []
            for tmp_y_1 in range(tmp_y):
                row_data = []
                for tmp_x_1 in range(tmp_x):
                    row_data.append([0,0,0,255])
                dt.append(row_data)
            # 填充占用点
            for item in tmp_region[4]:
                tmp_y_1 = item[0] - tmp_region[0]
                tmp_x_1 = item[1] - tmp_region[1]
                dt[tmp_y_1][tmp_x_1] = data[tmp_y_1 + tmp_region[0]][tmp_x_1 + tmp_region[1]]
            dt = np.asarray(dt, dtype=np.uint8)
            im_crop = Image.fromarray(dt)
            im_crop.save(save_path)
        else:
            im_crop = im1.crop(tmp_region_1)
            im_crop.save(save_path)