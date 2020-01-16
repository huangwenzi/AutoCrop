






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

        
# 合并前的数组
arr = [[473, 0, 578, 132], [2, 1, 469, 278], [474, 134, 564, 225], [499, 232, 542, 401], [548, 232, 591, 401], [197, 281, 348, 427], [354, 282, 491, 338], [2, 285, 45, 454], [51, 285, 94, 454], [100, 285, 143, 454], [149, 285, 192, 454], [355, 341, 492, 395], [473, 404, 517, 424], [359, 406, 482, 417], [197, 430, 633, 452], [199, 457, 631, 474], [2, 461, 45, 630], [51, 461, 94, 630], [100, 461, 143, 630], [149, 461, 192, 630], [243, 479, 389, 517], [438, 479, 584, 517], [591, 481, 628, 529], [197, 483, 249, 516], [392, 483, 444, 516], [198, 520, 391, 557], [394, 520, 447, 558], [489, 520, 587, 557], [452, 523, 485, 556], [197, 560, 248, 597], [247, 560, 391, 597], [535, 560, 585, 597], [587, 560, 637, 611], [439, 561, 538, 598], [393, 564, 445, 597]]
# 合并后的数组
merge_arr = []

print(len(arr))
merge_arr = merge_image_range(arr)
print(len(merge_arr))
print(merge_arr)
