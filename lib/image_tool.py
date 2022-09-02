import os
from PIL import Image
import lib.file_lib as file_lib
import lib.util_lib as util_lib
import numpy as np
import copy

# 周围八点
# 左下角起，顺时针
_around_pos = [
    [-1, -1],[-1, 0],[-1, +1],
    [0, +1],[+1, +1],[+1, 0],
    [+1, -1],[0, -1],
]
# 背景像素误差值
_bg_fault_val = 10


## 获取函数
# 获取与像素检查结果相同的位置
def get_ret_pixel_idx(data, begin, effective):
    data_len = len(data)
    for idx in range(begin, data_len):
        if effective == check_pixel(data[idx]):
            return idx

# 获取某一行的像素数组
def get_col_pixel(tow_data, col):
    row_len = len(tow_data)
    ret_list = []
    for tmp_x in range(0, row_len):
        ret_list.append(tow_data[tmp_x][col])
    return ret_list
# 获取某一列的像素数组
def get_row_pixel(tow_data, row):
    col_len = len(tow_data[0])
    ret_list = []
    for tmp_y in range(0, col_len):
        ret_list.append(tow_data[tmp_y][row])
    return ret_list

# 获取起始处开始的有效像素行(单点扩散)
# pos ： 起始点
# data ： 像素数据(二维)
def get_image_range(pos, data, pass_pos):
    range_arr = [pos[0], pos[1], pos[0], pos[1]]   # 截图范围  
    find_pos = [pos]  # 需要查找的点 [x,y],{"x,y" = 1}
    row_max = len(data)
    col_max = len(data[0])

    while True:
        ret_pos = check_pos_around(data, pass_pos, range_arr, find_pos, row_max, col_max)
        # 没有新的有效像素点
        if len(ret_pos) == 0:
            break
        find_pos = ret_pos
    
    # 范围有变化
    if range_arr[0] != range_arr[2] or range_arr[1] != range_arr[3]:
        return range_arr
    return None

# 获取起始处开始的有效像素行(描边)
# pos ： 起始点
# data ： 像素数据(二维)
def get_image_range_1(pos, data, row_max, col_max):
    range_arr = [pos[0],pos[1],pos[0],pos[1]]   # 截图范围
    tmp_pos = [pos[0], pos[1]]  # 当前点
    begin_idx = 0 # 开始的相对角度

    # 检查是否有效点
    # 是否有效点,超出图片范围
    if not check_pixel_and_range(data[tmp_pos[0]][tmp_pos[1]], tmp_pos, row_max, col_max):
        return None

    # 循环一周
    while True:
        # 主要逻辑
        # 查找周围的有效像素点,顺序很重要
        eff_pos = []
        for tmp_idx in range(8):
            # (idx+4)%8
            around_idx = (begin_idx+tmp_idx)%8 # 周围点idx
            tmp_around = _around_pos[around_idx]
            check_pos = [tmp_pos[0]+tmp_around[0], tmp_pos[1]+tmp_around[1]]
            # 是否有效点,超出图片范围
            if check_pos[0] < 0 or check_pos[1] < 0 or check_pos[0] >= row_max or check_pos[1] >= col_max:
                continue
            if check_pixel_and_range(data[check_pos[0]][check_pos[1]], check_pos, row_max, col_max):
                add_pos_info = {"pos":check_pos, "idx":around_idx}
                eff_pos.append(add_pos_info)
        # print(eff_pos)
        # 如果小于等于零退出
        if len(eff_pos) <= 0:
            return None

        # 刷新range_arr
        if tmp_pos[0] < range_arr[0]:
            range_arr[0] = tmp_pos[0]
        if tmp_pos[1] < range_arr[1]:
            range_arr[1] = tmp_pos[1]
        if tmp_pos[0] > range_arr[2]:
            range_arr[2] = tmp_pos[0]
        if tmp_pos[1] > range_arr[3]:
            range_arr[3] = tmp_pos[1]

        # 查找下一个点
        tmp_pos = eff_pos[0]["pos"]
        begin_idx = eff_pos[0]["idx"] + 5
        # 判断是否一周
        if tmp_pos[0] == pos[0] and tmp_pos[1] == pos[1]:
            break
    
    if range_arr[0] != range_arr[2] and range_arr[1] != range_arr[3]:
        return range_arr
    return None

## 检查函数
# 判断是否有像素点
# data ： 像素数据
def check_pixel(pixel): 
    # 黑底
    black = 0 + _bg_fault_val
    if (pixel[0] <= black and pixel[1] <= black and pixel[2] <= black) or pixel[3] == 0 :
        return False
    # 白底
    white = 255 - _bg_fault_val
    if (pixel[0] >= white and pixel[1] >= white and pixel[2] >= white) or pixel[3] == 0 :
        return False
    return True
# 判断是否有像素点(加范围判断)
# data ： 像素数据
def check_pixel_and_range(pixel, tmp_pos, row_max, col_max): 
    # 是否有效点,超出图片范围
    if tmp_pos[0] < 0 or tmp_pos[1] < 0 or tmp_pos[0] >= row_max or tmp_pos[1] >= col_max:
        return False
    # 检查像素
    return check_pixel(pixel)
# 判断数组是否有像素点
# data ： 像素数据
def check_row_pixel(data): 
    for tmp in data:
        if check_pixel(tmp):
            return True
    return False

# 是否在区域内
# pos ： 判断点 [x,y]
# skip_region ： 跳过的区域数组 [[x1,y1,x2,y2],....]
def in_skip_region(pos, skip_region):
    for tmp_region in skip_region:
        if pos[0] >= tmp_region[0] and pos[0] <= tmp_region[2] and pos[1] >= tmp_region[1] and pos[1] <= tmp_region[3]:
            return True
    return False

# 目标点周围的有效像素点
# data ： 像素数据(二维)
# pass_pos ： 跳过的点
# range_arr ： 截图范围
# find_pos ： 需要查找的点
def check_pos_around(data, pass_pos, range_arr, find_pos, row_max, col_max):
    # 遍历每个需要查找的点
    next_pos = []
    for tmp_pos in find_pos:
        # 是否跳过
        key = "%d,%d"%(tmp_pos[0],tmp_pos[1])
        if key in pass_pos:
            continue
        # 加入跳过的点
        pass_pos[key] = 1
        # 检查像素是否有效
        if tmp_pos[0] >= row_max or tmp_pos[1] >= col_max:
            continue
        if not check_pixel_and_range(data[tmp_pos[0]][tmp_pos[1]], tmp_pos, row_max, col_max):
            continue
        
        # 刷新range_arr
        # x
        if tmp_pos[0] < range_arr[0]:
            range_arr[0] = tmp_pos[0]
        elif tmp_pos[0] > range_arr[2]:
            range_arr[2] = tmp_pos[0]
        # y
        if tmp_pos[1] < range_arr[1]:
            range_arr[1] = tmp_pos[1]
        elif tmp_pos[1] > range_arr[3]:
            range_arr[3] = tmp_pos[1]

        # 遍历周围，发展下线
        for tmp_around in _around_pos:
            add_pos_x = tmp_pos[0]+tmp_around[0]
            add_pos_y = tmp_pos[1]+tmp_around[1]
            key = "%d,%d"%(add_pos_x, add_pos_y)
            if key in pass_pos:
                continue
            next_pos.append([add_pos_x, add_pos_y])
    return next_pos

# 两个范围是否有交集
def check_contact(range_1, range_2):
    # 2包含1的左上角
    if range_1[0] >= range_2[0] and range_1[0] <= range_2[2] and range_1[1] >= range_2[1] and range_1[1] <= range_2[3]:
        return True
    # 2包含1的右下角
    if range_1[2] >= range_2[0] and range_1[2] <= range_2[2] and range_1[3] >= range_2[1] and range_1[3] <= range_2[3]:
        return True
    # 1包含2的左上角
    if range_2[0] >= range_1[0] and range_2[0] <= range_1[2] and range_2[1] >= range_1[1] and range_2[1] <= range_1[3]:
        return True
    # 1包含2的右下角
    if range_2[2] >= range_1[0] and range_2[2] <= range_1[2] and range_2[3] >= range_1[1] and range_2[3] <= range_1[3]:
        return True
    return False




## 修改函数
# 像素数组顺时针旋转90度
# data ： 像素数据
# row_max ： row数
def pixelClockwise90(data, row_max):
    ret = []
    data_len = len(data)
    for idx in range(0, data_len):
        # 对应的位置
        pos = (idx%row_max)*row_max + idx//row_max
        ret.append(data[pos])
    return ret

# 二维数组顺时针旋转xy
# data ： 像素数据
def twoArrClockwiseXY(two_data):
    ret = []
    col_max = len(two_data)
    row_max = len(two_data[0])
    # 行
    for row_idx in range(0, row_max):
        col_arr = []
        # 列
        for col_idx in range(0, col_max):
            col_arr.append(two_data[col_idx][row_idx])
        ret.append(col_arr)
    return ret

# 像素数组转二维
# data ： 像素数据
# row_max ： row数
# ps : 
def data_to_two_arr(data, row_max):
    two_data = []
    data_len = len(data)
    col_max = data_len//row_max
    for idx in range(0, col_max):
        two_data.append(data[idx*row_max : idx*row_max + row_max])
    # 这时拿到的是(y,x)类型
    # 进行二维数组旋转
    ret = twoArrClockwiseXY(two_data)
    return ret

# 合并两个范围
def merge_range(range_1, range_2):
    now_range = []
    # 加入左上角x
    now_range.append(min(range_1[0], range_2[0]))
    # 加入左上角y
    now_range.append(min(range_1[1], range_2[1]))
    # 加入右上角x
    now_range.append(max(range_1[2], range_2[2]))
    # 加入右上角y
    now_range.append(max(range_1[3], range_2[3]))
    return now_range

# 合并有交集的范围
def merge_image_range(arr):
    while True:
        # 初始长度
        arr_len = len(arr)
        # 需要删除的序号(吧包含的加到最后那个)
        remove_idx = []

        # 当前序号
        idx_1 = 0
        for range_1 in arr:
            idx_2 = 0
            for range_2 in arr:
                if idx_1 == idx_2:
                    # 相同跳过
                    pass
                else:
                    # 是否有接触点
                    if check_contact(range_1, range_2):
                        # 不同合并，并把前一个加入删除列表,后一个更新范围
                        now_range = merge_range(range_1, range_2)
                        if idx_2 > idx_1:
                            remove_idx.append(idx_1)
                            arr[idx_2] = now_range
                        else:
                            remove_idx.append(idx_2)
                            arr[idx_1] = now_range
                idx_2 += 1
            idx_1 += 1
        
        # 没有需要删除就退出
        if len(remove_idx) <= 0:
            return arr

        # 删除
        now_arr = []
        idx_1 = 0
        for range_1 in arr:
            if idx_1 not in remove_idx:
                now_arr.append(range_1)
            idx_1 += 1
        arr = now_arr

# 删除四周空白行
def remove_blank_data(im1, tow_data):
    row_len = len(tow_data)
    col_len = len(tow_data[0])
    
    # 有效像素的行
    new_y = 0
    for tmp_y in range(0, col_len):
        for tmp_x in range(0, row_len):
            if check_pixel(tow_data[tmp_x][tmp_y]):
                new_y = tmp_y
                break
        if new_y > 0:
            break
    new_y_1 = 0
    for tmp_y in range(0, col_len):
        tmp_y = col_len - tmp_y - 1
        for tmp_x in range(0, row_len):
            if check_pixel(tow_data[tmp_x][tmp_y]):
                new_y_1 = tmp_y
                break
        if new_y_1 > 0:
            break
    # 有效像素的列
    new_x = 0
    for tmp_x in range(0, row_len):
        for tmp_y in range(0, col_len):
            if check_pixel(tow_data[tmp_x][tmp_y]):
                new_x = tmp_x
                break
        if new_x > 0:
            break
    new_x_1 = 0
    for tmp_x in range(0, row_len):
        tmp_x = row_len - tmp_x - 1
        for tmp_y in range(0, col_len):
            if check_pixel(tow_data[tmp_x][tmp_y]):
                new_x_1 = tmp_x
                break
        if new_x_1 > 0:
            break
    return im1.crop([new_x, new_y, new_x_1, new_y_1])
               
# 修改图片大小
def change_size(im, size):
    out = im.resize((size[0],size[1]))
    return out

# 压缩图片
def compress_image(path):
    im = Image.open(path)
    # 读取图片 转二维数组
    # im = im.convert('RGBA')
    data = np.asarray(im, np.uint8)
    data_1 = util_lib.list_three_to_two(data)
    print("not compress image len:%s"%(len(data_1)))

    # 计算计数
    data_2 = []
    data_pos_2 = []
    last_pos = copy.copy(data_1[0])
    pos_len = len(last_pos)
    pos_num = 0
    pos_sum = 0
    idx = 0
    for item in data_1:
        idx += 1
        if util_lib.arr_same(item, last_pos):
            pos_num += 1
            if pos_num == 255:
                data_pos_2.append(pos_num)
                data_2.append(last_pos)
                pos_sum += pos_num
                pos_num = 0
                last_pos = copy.copy(item)
        else:
            pos_num += 1
            data_pos_2.append(pos_num)
            pos_sum += pos_num
            data_2.append(last_pos)
            pos_num = 0
            last_pos = copy.copy(item)
    # 剩余的加进去
    data_pos_2.append(pos_num)
    data_2.append(last_pos)
    pos_sum += pos_num
    print("compress image len:%s, pos_sum:%s"%(len(data_2), pos_sum))

    # 转回三维
    def_add = util_lib.get_def_list(data_1[0])
    x_len = len(data[0])
    data_3 = util_lib.list_up_dimension(data_2, x_len, def_add)
    
    # 返回图片
    data_4_1 = np.asarray(data_3, np.uint8)
    image = Image.fromarray(data_4_1)
    
    # 像素数量转另一张图片
    def_add = []
    for item in range(3):
        def_add.append(0)
    data_pos_3 = util_lib.list_up_dimension(data_pos_2, 3, 0)
    data_pos_4 = util_lib.list_up_dimension(data_pos_3, x_len, def_add)
    data_pos_4_1 = np.asarray(data_pos_4, np.uint8)
    image_pos = Image.fromarray(data_pos_4_1)
    return image,image_pos
    
# 解压图片
def decompress_image(path, pos_path):
    im = Image.open(path)
    # 逆推成原图
    # im = im.convert('RGBA')
    data = np.asarray(im, np.uint8)
    data_1 = util_lib.list_three_to_two(data)
    
    
    # 位置图
    pos_im = Image.open(pos_path)
    pos_data = np.asarray(pos_im, np.uint8)
    pos_data_1 = util_lib.list_three_to_two(pos_data)
    pos_data_2 = util_lib.list_down_dimension(pos_data_1)
    
    # 根据数量扩展
    idx = 0
    data_2 = []
    add_pos = 0
    for pos_num in pos_data_2:
        if pos_num == 0:
            continue
        for item in range(pos_num):
            add_pos += 1
            data_2.append(copy.copy(data_1[idx]))
        idx += 1
    print("decompress_image add_pos:%s"%(add_pos))
    
    # 转对应三维数组
    x_len = len(data[0])
    def_add = util_lib.get_def_list(data_1[0])
    data_3 = util_lib.list_up_dimension(data_2, x_len, def_add)
    data_4 = np.asarray(data_3, np.uint8)
    image = Image.fromarray(data_4)
    return image




