from PIL import Image
import time
import os

import lib.image_tool as imageToolMd
import lib.file_lib as fileLibMd


# n宫格自动解析 每张图片xy对齐的场景
# image_path ： 图片地址
def AutoCrop(image_path):
    im1 = Image.open(image_path)
    im1 = im1.convert('RGBA')
    data = list(im1.getdata())
    row_Max = im1.size[0]
    col_Max = im1.size[1]
    tow_data = imageToolMd.data_to_two_arr(data, row_Max)
    
    # 删除上方和左方空白行
    im2 = imageToolMd.remove_blank_data(im1, tow_data)
    im2 = im2.convert('RGBA')
    data = list(im2.getdata())
    row_Max = im2.size[0]
    col_Max = im2.size[1]
    tow_data = imageToolMd.data_to_two_arr(data, row_Max)

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
            im_crop = im2.crop(box)
            im_crop.save(save_path)
    
# 不规则切图(单点扩散)
def AutoCropIrregularity(image_path):
    begin_time = time.time()
    im1 = Image.open(image_path)
    im1 = im1.convert('RGBA')
    data = im1.getdata()
    data = list(data)
    data_len = len(data)
    row_Max = im1.size[0]
    col_Max = im1.size[1]
    tow_data = imageToolMd.data_to_two_arr(data, row_Max)

    # 遍历每个像素点
    skip_region = []    # 跳过的区域,同时也是截取的范围
    for idx in range(0,data_len):
        pos = [idx%row_Max, idx//row_Max]
        # 是否有效像素
        if not imageToolMd.check_pixel(tow_data[pos[0], pos[1]]):
            continue
        # 跳过已有区域
        if imageToolMd.in_skip_region(pos, skip_region):
            continue
        
        range_arr = imageToolMd.getImageRange(pos, tow_data)
        if range_arr:
            skip_region.append(range_arr)
    
    # 保存图片
    image_name = imageToolMd.getImageName(image_path)
    for tmp_region in skip_region:
        save_path = "./crop/image/%s_%d_%d.png"%(image_name, tmp_region[0], tmp_region[1])
        im_crop = im1.crop(tmp_region)
        im_crop.save(save_path)
    end_time = time.time()
    print("AutoCropIrregularity %s consume:%f"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end_time - begin_time))

# 不规则切图(描边算法)
def AutoCropIrregularity_1(image_path):
    begin_time = time.time()
    im1 = Image.open(image_path)
    im1 = im1.convert('RGBA')
    data = im1.getdata()
    data = list(data)
    data_len = len(data)
    row_Max = im1.size[0]
    col_Max = im1.size[1]
    image_name = imageToolMd.getImageName(image_path)
    tow_data = imageToolMd.data_to_two_arr(data, row_Max)

    # 遍历每个像素点
    skip_region = []    # 跳过的区域,同时也是截取的范围
    for idx in range(0,data_len):
        pos = [idx%row_Max, idx//row_Max]
        # 跳过已有区域
        if imageToolMd.in_skip_region(pos, skip_region):
            continue
        # print(pos)
        range_arr = imageToolMd.getImageRange_1(pos, tow_data, row_Max, col_Max)
        if range_arr:
            skip_region.append(range_arr)

    skip_region = imageToolMd.merge_image_range(skip_region)

    # 保存图片
    save_dir_path = "./处理完毕/%s"%(image_name)
    if not os.path.exists(save_dir_path):
        os.makedirs(save_dir_path)
        
    for tmp_region in skip_region:
        save_path = "%s/%s_%d_%d.png"%(save_dir_path, image_name, tmp_region[0], tmp_region[1])
        print(save_path)
        if save_path == "./处理完毕/city_1/city_1_170_592.png":
            a = 1
        im_crop = im1.crop(tmp_region)
        im_crop.save(save_path)
    end_time = time.time()
    print("AutoCropIrregularity_1 %s consume:%f"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end_time - begin_time))

# 通过目录地址获取文件列表
def get_file_name_by_dir(dirname):
    file_list = []
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            tmp_file_path = os.path.join(root, name)
            file_list.append(tmp_file_path)
    return file_list





# AutoCropIrregularity("activity.png")
# AutoCropIrregularity_1("activity.png")
# AutoCropIrregularity_1("city_1.jpg")
# AutoCropIrregularity_1("city.jpg")

# # 目录批量处理
# file_list = get_file_name_by_dir("./需要处理")
# for tmp_name in file_list:
#     AutoCropIrregularity_1(tmp_name)