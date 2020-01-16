from PIL import Image
import time


from imageTool import imageTool as imageTool


# 图片截取
class CropMgr(object):
    pass

    # 截取图片
    # image_path ： 图片地址
    # row ： 行
    # col ： 列
    def crop(self, image_path, row, col):
        im1 = Image.open(image_path)
        image_name = imageTool.getImageName(image_path)
        print(im1.size)
        # 获取行和列的距离
        col_size = im1.size[1]/row
        row_size = im1.size[0]/col

        # 遍历行
        for row_idx in range(1, row+1):
            # 遍历列
            for col_idx in range(1, col+1):
                box = [(row_idx-1)*row_size, (col_idx-1)*col_size, row_idx*row_size, col_idx*col_size]
                save_path = "./crop/image/%s_%d_%d.png"%(image_name, row_idx, col_idx)
                im_crop = im1.crop(box)
                im_crop.save(save_path)
        
    # 九宫格自动解析
    # image_path ： 图片地址
    def AutoCrop(self, image_path):
        im1 = Image.open(image_path)
        im1 = im1.convert('RGBA')
        data = im1.getdata()
        data = list(data)
        row_Max = im1.size[0]
        col_Max = im1.size[1]
        image_name = imageTool.getImageName(image_path)


        # 遍历行（上面函数反了，效果差不多，不改了）
        col_idx = 0     # 当前行
        col_range = []  # [[begin,end],[begin, end]]
        while True:
            # 开始行
            begin_col = imageTool.getPixelRow(im1, data, col_idx, True)
            # 如果开始为空，说明到最后一行
            if begin_col == None:
                break
            # 结束行
            end_col = imageTool.getPixelRow(im1, data, begin_col, False)
            # 如果结束为空，说明到最后一行
            if end_col == None:
                end_col = col_Max - 1
                col_range.append([begin_col, end_col])
                break
            # 添加col范围
            col_range.append([begin_col, end_col])
            col_idx = end_col

        # 遍历列
        row_idx = 0     # 当前列
        row_range = []  # [[begin,end],[begin, end]]
        row_data = imageTool.pixelClockwise90(data, row_Max)
        while True:
            # 开始列
            begin_row = imageTool.getPixelRow(im1, row_data, row_idx, True)
            # 如果开始为空，说明到最后一列
            if begin_row == None:
                break
            # 结束列
            end_row = imageTool.getPixelRow(im1, row_data, begin_row, False)
            # 如果结束为空，说明到最后一列
            if end_row == None:
                end_row = row_Max - 1
                row_range.append([begin_row, end_row])
                break
            # 添加row范围
            row_range.append([begin_row, end_row])
            row_idx = end_row

        print(col_range)
        print(row_range)

        # 根据范围剪切
        for tmp_col in col_range:
            for tmp_row in row_range:
                box = [tmp_row[0], tmp_col[0], tmp_row[1], tmp_col[1]]
                save_path = "./crop/image/%s_%d_%d.png"%(image_name, tmp_row[0], tmp_col[0])
                im_crop = im1.crop(box)
                im_crop.save(save_path)
        
    # 不规则切图(单点扩散)
    def AutoCropIrregularity(self, image_path):
        begin_time = time.time()
        im1 = Image.open(image_path)
        im1 = im1.convert('RGBA')
        data = im1.getdata()
        data = list(data)
        data_len = len(data)
        row_Max = im1.size[0]
        col_Max = im1.size[1]
        image_name = imageTool.getImageName(image_path)
        tow_data = imageTool.dataToTwoArr(data, row_Max)

        # 遍历每个像素点
        skip_region = []    # 跳过的区域,同时也是截取的范围
        for idx in range(0,data_len):
            pos = [idx%row_Max, idx//row_Max]
            # 跳过已有区域
            if imageTool.inSkipRegion(pos, skip_region):
                continue
            # print(pos)
            range_arr = imageTool.getImageRange(pos, tow_data, row_Max, col_Max)
            if range_arr:
                skip_region.append(range_arr)
        
        # 保存图片
        for tmp_region in skip_region:
            save_path = "./crop/image/%s_%d_%d.png"%(image_name, tmp_region[0], tmp_region[1])
            im_crop = im1.crop(tmp_region)
            im_crop.save(save_path)
        end_time = time.time()
        print("AutoCropIrregularity %s consume:%f"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end_time - begin_time))

    # 不规则切图(描边算法)
    def AutoCropIrregularity_1(self, image_path):
        begin_time = time.time()
        im1 = Image.open(image_path)
        im1 = im1.convert('RGBA')
        data = im1.getdata()
        data = list(data)
        data_len = len(data)
        row_Max = im1.size[0]
        col_Max = im1.size[1]
        image_name = imageTool.getImageName(image_path)
        tow_data = imageTool.dataToTwoArr(data, row_Max)
    
        # 遍历每个像素点
        skip_region = []    # 跳过的区域,同时也是截取的范围
        for idx in range(0,data_len):
            pos = [idx%row_Max, idx//row_Max]
            # 跳过已有区域
            if imageTool.inSkipRegion(pos, skip_region):
                continue
            # print(pos)
            range_arr = imageTool.getImageRange_1(pos, tow_data, row_Max, col_Max)
            if range_arr:
                skip_region.append(range_arr)

        skip_region = imageTool.merge_image_range(skip_region)
        
        # 保存图片
        for tmp_region in skip_region:
            save_path = "./crop/image/%s_%d_%d.png"%(image_name, tmp_region[0], tmp_region[1])
            im_crop = im1.crop(tmp_region)
            im_crop.save(save_path)
        end_time = time.time()
        print("AutoCropIrregularity_1 %s consume:%f"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end_time - begin_time))



cropMgr = CropMgr()
# cropMgr.AutoCropIrregularity("activity.png")
cropMgr.AutoCropIrregularity_1("activity.png")
    

    
