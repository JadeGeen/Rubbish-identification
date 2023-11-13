#cv2 将图片分割成小块，分割参数为n*n,overlap为重叠部分,是一个0-1的小数
import cv2
import numpy as np  
from typing import List
import os
import sys


#输入为cv2的图片，分割参数，以及overlap
def clip_pic(picture: cv2.UMat, n: int, overlap: float) -> List[cv2.UMat]:
    #使用cv中的split函数进行分割
    #分割为n*n个小块
    #overlap为重叠部分

    #获取图片的长宽
    height, width = picture.shape[:2]
    #计算重叠部分的长度
    length_height = int(height / (1+(n-1)*(1-overlap)))
    length_width = int(width /(1+(n-1)*(1-overlap)))
    overlap_height = int(length_height * overlap)
    overlap_width = int(length_width * overlap)

    #初始化分割后的图片列表
    pic_list = []
    bias_list = []
    #进行分割
    for i in range(n):
        for j in range(n):
            pic_list.append(picture[i * length_height - i * overlap_height : (i + 1) * length_height - i * overlap_height, j * length_width - j * overlap_width : (j + 1) * length_width - j * overlap_width])
            bias_list.append([i * length_height - i * overlap_height,j * length_width - j * overlap_width ])
    return pic_list, bias_list