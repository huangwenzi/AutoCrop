from PIL import Image
import time
import os

import lib.image_tool as imageToolMd
import lib.file_lib as fileLibMd
import lib.crop_mgr as cropMgrMd



## n宫图切割
path = "需要处理/1.png"
path = fileLibMd.change_path_of_sys(path)
cropMgrMd.AutoCrop(path)