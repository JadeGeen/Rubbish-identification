#-*- coding: UTF-8 -*-
import os
import sys
import time
cwd = os.getcwd()
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),'SuperPointPretrainedNetwork'))
import cv2
from src.Deep import superpoint
cv2.ocl.setUseOpenCL(False)

if __name__ == '__main__':
    base_dir = '/home/yanghongchao/code/ChangeDetection/data/'
    img1_name = 'base.png'
    img2_name = 'change_1.png'
    base_img =cv2.imread(os.path.join(base_dir,img1_name))
    change_img =cv2.imread(os.path.join(base_dir,img2_name))
    # th1 越大，关键点越多
    th1 = 0.85
    # th2 越小，单应性估计时匹配成功的关键点越多
    th2 = 0.25
    # th3 越大，检测出变化的区域越少
    th3 = 620
    # box 四个维度分别为 x1,y1,w,h
    # 如果要多次调用 sp_detect, 且每次调用时 base_img 相同，则使用 keynet_detect方法
    # 如果多次 base_img 不同，则使用 keynet_detect_two 方法
    t1 = time.time()
    box_list = superpoint.sp_detect(base_img,change_img,th1,th2,th3)
    t2 = time.time()
    # box_list = superpoint.sp_detect_two(base_img,change_img,th1,th2,th3)
    print(box_list)
    print(t2-t1)


