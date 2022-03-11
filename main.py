from PIL import Image
import time
import os

import lib.image_tool as imageToolMd
import lib.file_lib as fileLibMd
import lib.crop_mgr as cropMgrMd
import lib.time_tool as timeToolMd
time_tool = timeToolMd.time_tool


## n宫图切割
path = "需要处理/商店.jpg"
path = fileLibMd.change_path_of_sys(path)
# time_tool.consume_time_begin("AutoCrop")
# cropMgrMd.AutoCrop(path)
# time_tool.consume_time_end("AutoCrop")

time_tool.consume_time_begin("auto_crop_irregularity")
cropMgrMd.auto_crop_irregularity(path)
time_tool.consume_time_end("auto_crop_irregularity")

# time_tool.consume_time_begin("auto_crop_irregularity_1")
# cropMgrMd.auto_crop_irregularity_1(path)
# time_tool.consume_time_end("auto_crop_irregularity_1")