import sys
# 避免递归达到1000上限
sys.setrecursionlimit(90000000)




# 图片处理工具
class ImageTool(object):
    pass

    # 获取图片名
    def getImageName(self, path):
        begin_idx = path.rfind("/")
        end_idx = path.rfind(".")
        name = path[begin_idx + 1 : end_idx]
        return name

    # 判断是否有像素点
    # data ： 像素数据
    def checkPixel(self, tmp): 
        if (tmp[0] == 0 and tmp[1] == 0 and tmp[2] == 0) or tmp[3] == 0 :
            return False
        return True

    # 判断数组是否有像素点
    # data ： 像素数据
    def checkRowPixel(self, data): 
        for tmp in data:
            if self.checkPixel(tmp):
                return True
        return False

    # 像素数组顺时针旋转90度
    # data ： 像素数据
    # row_max ： row数
    def pixelClockwise90(self, data, row_max):
        ret = []
        data_len = len(data)
        col_max = data_len//row_max
        for idx in range(0, data_len):
            # 对应的位置
            pos = (idx%row_max)*row_max + idx//row_max
            ret.append(data[pos])
        return ret

    # 二维数组顺时针旋转xy
    # data ： 像素数据
    def twoArrClockwiseXY(self, two_data):
        ret = []
        col_max = len(two_data)
        row_max = len(two_data[0])
        data_len = col_max * row_max
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
    def dataToTwoArr(self, data, row_max):
        two_data = []
        data_len = len(data)
        col_max = data_len//row_max
        for idx in range(0, col_max):
            two_data.append(data[idx*row_max : idx*row_max + row_max])
        # 这时拿到的是(y,x)类型
        # 进行二维数组旋转
        ret = self.twoArrClockwiseXY(two_data)
        return ret

    # 获取起始处开始的有效像素行
    # im1 ： 图片资源
    # data ： 像素数据
    # begin ： 开始位置
    # effective ： 是否有效 True：有像素点 False：无像素点
    def getPixelRow(self, im1, data, begin, effective):
        row_Max = im1.size[0]
        col_Max = im1.size[1]
        # 遍历查找有效像素行
        for col_idx in range(begin, col_Max + 1):
            begin_idx = col_idx*row_Max
            has_pixel = self.checkRowPixel(data[begin_idx : begin_idx + row_Max])
            if effective == has_pixel:
                return col_idx
        return None

    # 是否在区域内
    # pos ： 判断点 [x,y]
    # skip_region ： 跳过的区域数组 [[x1,y1,x2,y2],....]
    def inSkipRegion(self, pos, skip_region):
        for tmp_region in skip_region:
            if pos[0] >= tmp_region[0] and pos[0] <= tmp_region[2] and pos[1] >= tmp_region[1] and pos[1] <= tmp_region[3]:
                return True
        return False
        

    # 遍历相接的点是否有效点
    # pos ： 起始点
    # data ： 像素数据(二维)
    # pass_pos ： 跳过的点
    # range_arr ： 截图范围
    # find_pos ： 需要查找的点
    def checkPosAround(self, pos, data, row_Max, col_Max, pass_pos, range_arr, find_pos):
        # 遍历每个需要查找的点
        next_pos = []
        for tmp_pos in find_pos:
            # 是否跳过
            if tmp_pos in pass_pos:
                continue
            # 加入跳过的点
            pass_pos.append(tmp_pos)
            # 是否有效点,超出图片范围
            if tmp_pos[0] < 0 or tmp_pos[1] < 0 or tmp_pos[0] >= row_Max or tmp_pos[1] >= col_Max:
                continue
            # 是否有效像素
            if not self.checkPixel(data[tmp_pos[0]][tmp_pos[1]]):
                continue
            # 刷新range_arr
            if tmp_pos[0] < range_arr[0]:
                range_arr[0] = tmp_pos[0]
            if tmp_pos[1] < range_arr[1]:
                range_arr[1] = tmp_pos[1]
            if tmp_pos[0] > range_arr[2]:
                range_arr[2] = tmp_pos[0]
            if tmp_pos[1] > range_arr[3]:
                range_arr[3] = tmp_pos[1]
            # 遍历周围，发展下线
            next_pos.append([tmp_pos[0]-1, tmp_pos[1]-1])
            next_pos.append([tmp_pos[0], tmp_pos[1]-1])
            next_pos.append([tmp_pos[0]+1, tmp_pos[1]-1])
            next_pos.append([tmp_pos[0]-1, tmp_pos[1]])
            next_pos.append([tmp_pos[0]+1, tmp_pos[1]])
            next_pos.append([tmp_pos[0]-1, tmp_pos[1]+1])
            next_pos.append([tmp_pos[0], tmp_pos[1]+1])
            next_pos.append([tmp_pos[0]+1, tmp_pos[1]+1])
        return next_pos

    # 获取起始处开始的有效像素行
    # pos ： 起始点
    # data ： 像素数据(二维)
    def getImageRange(self, pos, data, row_Max, col_Max):
        # 已经找过的点 [x,y], {"x,y" = 1}后者比较省查找时间,前者简便
        pass_pos = []
        range_arr = [pos[0],pos[1],pos[0],pos[1]]   # 截图范围  
        # key = "%d,%d"%(pos[0],pos[1])
        find_pos = [pos]  # 需要查找的点 [x,y],{"x,y" = 1}

        while True:
            ret_pos = self.checkPosAround([pos[0], pos[1]], data, row_Max, col_Max, pass_pos, range_arr, find_pos)
            if len(ret_pos) == 0:
                break
            find_pos = ret_pos
        
        if range_arr[0] != range_arr[2] or range_arr[1] != range_arr[3]:
            return range_arr
        return None

imageTool = ImageTool()
