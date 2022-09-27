

import lib.file_lib as fileLibMd
import lib.crop_mgr as cropMgrMd
import lib.time_tool as timeToolMd
time_tool = timeToolMd.time_tool


## n宫图切割
# path = "需要处理/1.png"
path = "需要处理/不规则.png"
path = "需要处理/activity.png"
path = fileLibMd.change_path_of_sys(path)
# time_tool.consume_time_begin("AutoCrop")
# cropMgrMd.AutoCrop(path)
# time_tool.consume_time_end("AutoCrop")

## 不规则切图(单点扩散)
# time_tool.consume_time_begin("auto_crop_irregularity")
# cropMgrMd.auto_crop_irregularity(path)
# time_tool.consume_time_end("auto_crop_irregularity")

# time_tool.consume_time_begin("auto_crop_irregularity_1")
# cropMgrMd.auto_crop_irregularity_1(path)
# time_tool.consume_time_end("auto_crop_irregularity_1")

## 不规则切图(单点扩散) 占用点保存，切的图也是不规则的
time_tool.consume_time_begin("auto_crop_irregularity_2")
cropMgrMd.auto_crop_irregularity_2(path)
time_tool.consume_time_end("auto_crop_irregularity_2")
