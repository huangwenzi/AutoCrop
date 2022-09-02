

import lib.file_lib as file_lib
import lib.image_tool as image_tool

# 读取文件列表
file_list = file_lib.get_file_name_by_dir("./压缩(已压缩)")
for path in file_list:
    image = image_tool.decompress_image(path)
    file_name, suffix_name = file_lib.get_file_name_and_suffix(path)
    image.save("./压缩(已解压)/%s%s"%(file_name,suffix_name))