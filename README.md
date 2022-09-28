# 使用 
1.需要剪切的文件放在文件夹：需要处理  
2.处理完毕的文件放在文件夹：处理完毕  
3.修改main.py 里的图片地址  
4.在cmd使用 python main.py  



# ps：处理以白底或黑底为标准
AutoCrop 只适用在行列对齐的图片，速度最快  
auto_crop_irregularity    速度慢，对图片边缘不规则度接受高  
auto_crop_irregularity_1  速度中, 太复杂图片不准确  
auto_crop_irregularity_2  速度满, 对复杂图像兼容度高，推荐  

# 例如
原图：  
![](https://github.com/huangwenzi/AutoCrop/tree/master/activity.png)  
切割后：  
![](https://github.com/huangwenzi/AutoCrop/tree/master/show_2.png)  
