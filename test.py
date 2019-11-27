import time


int_arr = []
str_arr = {}

for idx in range(0, 10000000):
    int_arr.append(str(idx))
    str_arr[str(idx)] = 1

begin_time = time.time()
if "5000000" in int_arr:
    end_time = time.time()
    print("int_arr consume:%f"%(end_time - begin_time))

begin_time = time.time()
if "5000000" in str_arr:
    end_time = time.time()
    print("str_arr consume:%f"%(end_time - begin_time))