import json

import lib.file_lib as file_lib
import lib.image_tool as image_tool
            
# 读取文件列表
file_list = file_lib.get_file_name_by_dir("./压缩(需压缩)")
for path in file_list:
    file_name, suffix_name = file_lib.get_file_name_and_suffix(path)
    image,image_pos = image_tool.compress_image(path)
    image.save("./压缩(已压缩)/%s%s"%(file_name,suffix_name))
    image_pos.save("./压缩(已压缩)/pos_%s%s"%(file_name,suffix_name))
            















