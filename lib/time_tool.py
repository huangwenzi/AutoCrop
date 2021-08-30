# 官方模块
import time


# 时间工具模块
class TimeTool():
    # 时间消耗标志字典
    consume_time_dict = {}  # {key = begin_time}
    # 累计时间消耗标志字典
    acc_consume_time_dict = {}  # {key = [acc_time, begin_time]}

    def __init__(self):
        self.consume_time_dict = {}

    # 消耗记时开始
    def consume_time_begin(self, Type):
        self.consume_time_dict[Type] = time.time()

    # 消耗记时结束
    def consume_time_end(self, Type):
        consume = time.time() - self.consume_time_dict[Type]
        # 大于0.001秒才打印
        if consume > 0.001:
            print("consume_time Type : {0}, {1}".format(Type, consume))
    
    # 累计消耗记时创建
    def acc_consume_time_crate(self, Type):
        self.consume_time_dict[Type] = [0, 0]

    # 累计消耗记时开始
    def acc_consume_time_begin(self, Type):
        self.consume_time_dict[Type][1] = time.time()

    # 累计消耗记时开始
    def acc_consume_time_end(self, Type):
        self.consume_time_dict[Type][0] += (time.time() - self.consume_time_dict[Type][1])
    
    # 累计消耗记时打印
    def acc_consume_time_print(self, Type):
        print("consume_time Type : {0}, {1}".format(Type, self.consume_time_dict[Type][0]))
    


time_tool = TimeTool()












