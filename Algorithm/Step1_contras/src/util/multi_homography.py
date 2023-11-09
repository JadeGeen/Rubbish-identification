import math

import cv2
import numpy as np
import sys

def get_multi_homography(pts_src, pts_dst,threshold=3.0,outlier_proportion=0.5,min_macth_num=3):
    # 总关键点数
    total_num = len(pts_src)
    outliers_num = total_num
    matched_pts_src = []
    matched_pts_des = []
    m_arr = []
    # 当outlier的比例大于阈值时，需要对outlier重新找单应性矩阵区域
    # 是不是可能会有重合区域啊？
    while(outliers_num/total_num>outlier_proportion):
        M, Mask = cv2.findHomography(pts_src,pts_dst,cv2.RANSAC,threshold)
        m_arr.append(M)
        new_pts_src = []
        new_pts_dst = []
        matched_src = []
        matched_dst = []
        for i in range(1,len(Mask)):
            if(Mask[i]==0):
                # 未匹配成功
                new_pts_src.append(pts_src[i])
                new_pts_dst.append(pts_dst[i])
            else:
                # 匹配成功
                matched_src.append(pts_src[i])
                matched_dst.append(pts_dst[i])
        # 如果某次匹配成功的关键点小于min_match_num
        if len(matched_src) < min_macth_num:
            break
        matched_pts_src.append(matched_src)
        matched_pts_des.append(matched_dst)
        # 将未匹配成功的点重新赋值
        pts_src =  np.array(new_pts_src)
        pts_dst =  np.array(new_pts_dst)
        outliers_num = len(pts_src)

    return matched_pts_src,matched_pts_des,m_arr

# region 四个维度分别是 xMin,xMax,yMin,yMax
# pt 两个纬度分别是 x，y
def get_idx(pt,regions):
    x,y=pt[0],pt[1]
    idx = -1
    min_distance = sys.float_info.max
    for i in range(len(regions)):
        tmp_distance = 0
        # 如果在该区域内，则直接返回
        # 否则，通过计算到该区域的distance
        x_min,x_max,y_min,y_max = regions[i][0],regions[i][1],regions[i][2],regions[i][3]
        # 在该区域内
        if((x>=x_min) & (x<=x_max) & (y>=y_min) & (y<=y_max)):
            return i
        y_distance = min(abs(y_min-y),abs(y_max-y))
        x_distance = min(abs(x_min-x),abs(x_max-x))
        if((x>=x_min) & (x<=x_max)):
            tmp_distance = y_distance
        elif((y>=y_min) & (y<=y_max)):
            tmp_distance = x_distance
        else:
            tmp_distance = math.sqrt(math.pow(x_distance,2)+math.pow(y_distance,2))
        if(tmp_distance < min_distance):
            min_distance = tmp_distance
            idx = i
    return idx