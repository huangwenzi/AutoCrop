from PIL import Image
import os

import lib.image_tool as imageToolMd
import lib.file_lib as fileLibMd
import lib.time_tool as timeToolMd
time_tool = timeToolMd.time_tool


# n宫格自动解析 每张图片xy对齐的场景
# image_path ： 图片地址
def AutoCrop(image_path):
    im1 = Image.open(image_path)
    im1 = im1.convert('RGBA')
    data = list(im1.getdata())
    row_max = im1.size[0]
    col_Max = im1.size[1]
    tow_data = imageToolMd.data_to_two_arr(data, row_max)
    
    # 删除上方和左方空白行
    im2 = imageToolMd.remove_blank_data(im1, tow_data)
    im2 = im2.convert('RGBA')
    data = list(im2.getdata())
    row_max = im2.size[0]
    col_Max = im2.size[1]
    tow_data = imageToolMd.data_to_two_arr(data, row_max)

    # 获取每一张图x占的范围 
    col_idx = 0
    col_range = []  # [[begin,end],[begin, end]]
    col_data = imageToolMd.get_col_pixel(tow_data, 0)
    while True:
        # 开始处
        begin_idx = imageToolMd.get_ret_pixel_idx(col_data, col_idx, True)
        # 如果开始为空，说明到最后一行
        if begin_idx == None:
            break
        # 结束行
        end_idx = imageToolMd.get_ret_pixel_idx(col_data, begin_idx, False)
        # 如果结束为空，说明到最后一行
        if end_idx == None:
            end_idx = col_Max - 1
            col_range.append([begin_idx, end_idx])
            break
        # 添加col范围
        col_range.append([begin_idx, end_idx])
        col_idx = end_idx
        
    # 获取每一张图y占的范围
    row_idx = 0
    row_range = []  # [[begin,end],[begin, end]]
    row_data = imageToolMd.get_row_pixel(tow_data, 0)
    while True:
        # 开始处
        begin_idx = imageToolMd.get_ret_pixel_idx(row_data, row_idx, True)
        # 如果开始为空，说明到最后一行
        if begin_idx == None:
            break
        # 结束行
        end_idx = imageToolMd.get_ret_pixel_idx(row_data, begin_idx, False)
        # 如果结束为空，说明到最后一行
        if end_idx == None:
            end_idx = col_Max - 1
            row_range.append([begin_idx, end_idx])
            break
        # 添加col范围
        row_range.append([begin_idx, end_idx])
        row_idx = end_idx

    # 根据范围剪切
    image_name = fileLibMd.get_file_name(image_path)
    for tmp_col in col_range:
        for tmp_row in row_range:
            box = [tmp_row[0], tmp_col[0], tmp_row[1], tmp_col[1]]
            save_path = "./处理完毕/%s/_%d_%d.png"%(image_name, tmp_row[0], tmp_col[0])
            fileLibMd.crate_dir(save_path)
            im_crop = im2.crop(box)
            im_crop.save(save_path)
    
# 不规则切图(单点扩散)
def auto_crop_irregularity(image_path):
    im1 = Image.open(image_path)
    im1 = im1.convert('RGBA')
    data = list(im1.getdata())
    data_len = len(data)
    row_max = im1.size[0]
    tow_data = imageToolMd.data_to_two_arr(data, row_max)

    # 遍历每个像素点
    skip_region = []    # 跳过的区域,同时也是截取的范围
    # 已经找过的点 [x,y], {"x,y" = 1}后者比较省查找时间,前者简便
    pass_pos = {}
    for idx in range(0,data_len):
        pos = [idx%row_max, idx//row_max]
        # 是否有效像素
        if not imageToolMd.check_pixel(tow_data[pos[0]][pos[1]]):
            continue
        # 跳过已有区域
        if imageToolMd.in_skip_region(pos, skip_region):
            continue
        # 是否跳过
        key = "%d,%d"%(pos[0],pos[1])
        if key in pass_pos:
            continue

        range_arr = imageToolMd.get_image_range(pos, tow_data, pass_pos)
        if range_arr:
            skip_region.append(range_arr)
    
    # 保存图片
    fileLibMd.save_imaae(image_path, skip_region, im1)
    
# 不规则切图(描边算法)
def auto_crop_irregularity_1(image_path):
    im1 = Image.open(image_path)
    im1 = im1.convert('RGBA')
    data = im1.getdata()
    data = list(data)
    data_len = len(data)
    row_max = im1.size[0]
    col_Max = im1.size[1]
    tow_data = imageToolMd.data_to_two_arr(data, row_max)

    # 遍历每个像素点
    skip_region = []    # 跳过的区域,同时也是截取的范围
    for idx in range(0,data_len):
        pos = [idx%row_max, idx//row_max]
        # 跳过已有区域
        if imageToolMd.in_skip_region(pos, skip_region):
            continue
        range_arr = imageToolMd.get_image_range_1(pos, tow_data, row_max, col_Max)
        if range_arr:
            skip_region.append(range_arr)
    skip_region = imageToolMd.merge_image_range(skip_region)

    # 保存图片
    # 保存图片
    fileLibMd.save_imaae(image_path, skip_region, im1)







# auto_crop_irregularity("activity.png")
# auto_crop_irregularity_1("activity.png")
# auto_crop_irregularity_1("city_1.jpg")
# auto_crop_irregularity_1("city.jpg")

# # 目录批量处理
# file_list = get_file_name_by_dir("./需要处理")
# for tmp_name in file_list:
#     auto_crop_irregularity_1(tmp_name)