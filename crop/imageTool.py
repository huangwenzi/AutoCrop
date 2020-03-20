import sys
# 避免递归达到1000上限
sys.setrecursionlimit(90000000)


# 周围八点
_around_pos = [
    [-1, -1],
    [-1, 0],
    [-1, +1],
    [0, +1],
    [+1, +1],
    [+1, 0],
    [+1, -1],
    [0, -1],
]

# 图片处理工具
class ImageTool(object):
    pass

    # 获取图片名
    def getImageName(self, path):
        # begin_idx = path.rfind("/")
        begin_idx = path.rfind("\\")
        end_idx = path.rfind(".")
        name = path[begin_idx + 1 : end_idx]
        return name

    # 判断是否有像素点
    # data ： 像素数据
    def checkPixel(self, tmp): 
        if (tmp[0] == 0 and tmp[1] == 0 and tmp[2] == 0) or tmp[3] == 0 :
            return False
        return True
    # 判断是否有像素点(加范围判断)
    # data ： 像素数据
    def checkPixelAndRange(self, pixel, tmp_pos, row_Max, col_Max): 
        # 是否有效点,超出图片范围
        if tmp_pos[0] < 0 or tmp_pos[1] < 0 or tmp_pos[0] >= row_Max or tmp_pos[1] >= col_Max:
            return False
        if (pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0) or pixel[3] == 0 :
            return False
        if (pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255) or pixel[3] == 0 :
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
            key = "%d,%d"%(tmp_pos[0],tmp_pos[1])
            if key in pass_pos:
                continue
            # 加入跳过的点
            pass_pos[key] = 1
            # pass_pos.append(tmp_pos)
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
            for tmp_around in _around_pos:
                self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0]+tmp_around[0], tmp_pos[1]+tmp_around[1]])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0]-1, tmp_pos[1]-1])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0], tmp_pos[1]-1])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0]+1, tmp_pos[1]-1])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0]-1, tmp_pos[1]])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0]+1, tmp_pos[1]])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0]-1, tmp_pos[1]+1])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0], tmp_pos[1]+1])
            # self.checkPosAround_addPos(next_pos, pass_pos, [tmp_pos[0]+1, tmp_pos[1]+1])
        return next_pos
    # 上面专用
    # next_pos ： 加入数组
    # pass_pos ： 跳过的点
    # pos ： 加入的点
    def checkPosAround_addPos(self, next_pos, pass_pos, pos):
        key = "%d,%d"%(pos[0],pos[1])
        if key in pass_pos:
            return
        next_pos.append(pos)

    # 获取起始处开始的有效像素行(单点扩散)
    # pos ： 起始点
    # data ： 像素数据(二维)
    def getImageRange(self, pos, data, row_Max, col_Max):
        # 已经找过的点 [x,y], {"x,y" = 1}后者比较省查找时间,前者简便
        pass_pos = {}
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

    # 获取相对的位置
    def getPosIdx(self, idx):
        return (idx+4)%8

    # 获取起始处开始的有效像素行(描边)
    # pos ： 起始点
    # data ： 像素数据(二维)
    def getImageRange_1(self, pos, data, row_Max, col_Max):
        range_arr = [pos[0],pos[1],pos[0],pos[1]]   # 截图范围
        tmp_pos = [pos[0], pos[1]]  # 当前点
        begin_idx = 0 # 开始的相对角度

        # 检查是否有效点
        # 是否有效点,超出图片范围
        if not self.checkPixelAndRange(data[tmp_pos[0]][tmp_pos[1]], tmp_pos, row_Max, col_Max):
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
                if check_pos[0] < 0 or check_pos[1] < 0 or check_pos[0] >= row_Max or check_pos[1] >= col_Max:
                    continue
                if self.checkPixelAndRange(data[check_pos[0]][check_pos[1]], check_pos, row_Max, col_Max):
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

    # 两个范围是否有交集
    def check_contact(self, range_1, range_2):
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

    # 合并两个范围
    def merge_range(self, range_1, range_2):
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
    def merge_image_range(self, arr):
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
                        if self.check_contact(range_1, range_2):
                            # 不同合并，并把前一个加入删除列表,后一个更新范围
                            now_range = self.merge_range(range_1, range_2)
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

imageTool = ImageTool()
