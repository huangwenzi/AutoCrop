import copy





# 两个数组是否一样
def arr_same(a_list, b_list):
    if len(a_list) != len(b_list):
        return False
    for item in range(len(a_list)):
        if a_list[item] != b_list[item]:
            return False
    return True

# 把三维数组变二维
def list_three_to_two(data):
    data_1 = []
    for item in data:
        for item_1 in item:
            tmp_1 = []
            for item_2 in item_1:
                tmp_1.append(item_2)
            data_1.append(tmp_1)
    return data_1

# 把二维数组变三维
def list_two_to_three(data, data_len, def_add):
    data_1 = []
    while True:
        add_list = data[:data_len]
        data = data[data_len:]
        # 截取完了
        if len(data) == 0:
            # 补全
            for item in range(data_len - len(add_list)):
                add_list.append(copy.copy(def_add))
            data_1.append(add_list)
            break
        data_1.append(add_list)
    return data_1






















