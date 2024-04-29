# -*- coding: utf-8 -*-
import cv2
import numpy as np

cv2.ocl.setUseOpenCL(False)
import math
import time
from Step1_contras.src.util.utils import print_black
from Step1_contras.src.util import multi_homography


def main(img1, img2, get_kp_and_des, get_des_from_kp,threshold = 550, func = 2):
    # 直方图均衡化 + 转换为灰度图
    # img1 = cv2.equalizeHist(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))
    # img2 = cv2.equalizeHist(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY))

    # 高斯滤波
    img1 = cv2.GaussianBlur(img1, (5, 5), 0)
    img2 = cv2.GaussianBlur(img2, (5, 5), 0)

    # 检测关键点
    kp1, des1 = get_kp_and_des(img1)
    kp2, des2 = get_kp_and_des(img2)

    # 关键点匹配
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=6)
    search_params = dict(checks=10)

    # 快速最近邻搜索
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(np.asarray(des1, np.float32), np.asarray(des2, np.float32), k=2)

    # 去除错误匹配
    good = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)

    # 把good中的左右点分别提出来找单应性变换
    pts_src = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    pts_dst = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    if len(pts_src) < 5:
        return []

    # 单应性变换
    # M, mask = cv2.findHomography(pts_src, pts_dst, cv2.RANSAC, 5.0)
    # matched_pts_src,matched_pts_dst, m_arr = get_multi_homography(pts_src,pts_dst,5.0)
    matched_pts_src, matched_pts_dst, m_arr = multi_homography.get_multi_homography(pts_src, pts_dst,outlier_proportion=0.25)



    # 输出匹配结果 ********************************************************
    if func == 0:
        # 输出图片初始化
        height = max(img1.shape[0], img2.shape[0])
        width = img1.shape[1] + img1.shape[1]
        output = np.zeros((height, width, 3), dtype=np.uint8)
        output[0:img1.shape[0], 0:img1.shape[1]] = img1
        output[0:img2.shape[0], img2.shape[1]:] = img2[:]

        # 把点画出来
        _1_255 = np.expand_dims(np.array(range(0, 256), dtype='uint8'), 1)
        _colormap = cv2.applyColorMap(_1_255, cv2.COLORMAP_HSV)


        for j in range(len(matched_pts_src)):
            matched_src = matched_pts_src[j]
            matched_dst = matched_pts_dst[j]
            for i in range(len(matched_src)):
                left = matched_src[i][0]
                colormap_idx = int((left[0] - img1.shape[1] * .5 + left[1] - img1.shape[0] * .5) * 256. / (
                        img1.shape[0] * .5 + img1.shape[1] * .5))
                color = tuple(map(int, _colormap[colormap_idx, 0, :]))
                if i % 2 == 0:
                    cv2.circle(output, (int(matched_src[i][0][0]), int(matched_src[i][0][1])), 2, color, 2)
                    cv2.circle(output, (int(matched_dst[i][0][0]) + img1.shape[1], int(matched_dst[i][0][1])), 2, color,
                               2)
                    cv2.line(output, (matched_src[i][0][0], matched_src[i][0][1]),
                             (int(matched_dst[i][0][0] + img1.shape[1]), matched_dst[i][0][1]), color, 1, 0)

        # 最终结果输出
        a = 1
        outputN = cv2.resize(output, (int(img1.shape[1] * 2 * a), int(img1.shape[0] * a)),
                             interpolation=cv2.INTER_CUBIC)

    # 存储每个匹配成功区域的 x_min,x_max,y_min,y_max
    regions = []

    # 输出差异识别结果 ********************************************************
    if (func == 1) | (func == 2):
        #  图像的长宽
        height, width, channel = img1.shape
        # height,width = img1.shape

        # 设定关键点的尺度
        size = int(width * 0.01)

        # 自动选择采样点的位置范围
        xMinLeft = width
        xMaxLeft = 0
        yMinLeft = height
        yMaxLeft = 0

        # 用当前匹配成功的点集分析合适的检测范围
        for i in range(len(matched_pts_src)):
            matched_src = matched_pts_src[i]
            tmp_x_min = width
            tmp_x_max = 0
            tmp_y_min = height
            tmp_y_max = 0
            for j in range(len(matched_src)):
                if matched_src[j][0][1] < tmp_y_min:
                    tmp_y_min = matched_src[j][0][1]
                if matched_src[j][0][1] > tmp_y_max:
                    tmp_y_max = matched_src[j][0][1]
                if matched_src[j][0][0] < tmp_x_min:
                    tmp_x_min = matched_src[j][0][0]
                if matched_src[j][0][0] > tmp_x_max:
                    tmp_x_max = matched_src[j][0][0]
            # 把该region的四维坐标添加到regions
            regions.append([tmp_x_min, tmp_x_max, tmp_y_min, tmp_y_max])
            xMinLeft = min(xMinLeft, tmp_x_min)
            xMaxLeft = max(xMaxLeft, tmp_x_max)
            yMinLeft = min(yMinLeft, tmp_y_min)
            yMaxLeft = max(yMaxLeft, tmp_y_max)

        # 用所有关键点来确定检测范围
        # for i in range(len(pts_src)):
        #     if pts_src[i][0][1] < yMinLeft:
        #         yMinLeft = pts_src[i][0][1]
        #     if pts_src[i][0][1] > yMaxLeft:
        #         yMaxLeft = pts_src[i][0][1]
        #     if pts_src[i][0][0] < xMinLeft:
        #         xMinLeft = pts_src[i][0][0]
        #     if pts_src[i][0][0] > xMaxLeft:
        #         xMaxLeft = pts_src[i][0][0]

        # 检测范围确定
        interval = 2.5 * size  # 监测点间隔

        searchWidth = int((xMaxLeft - xMinLeft) / interval)
        searchHeight = int((yMaxLeft - yMinLeft) / interval)
        searchNum = searchWidth * searchHeight
        demo_src = np.float32([[0] * 2] * searchNum * 1).reshape(-1, 1, 2)

        # i是列，j是行
        for i in range(searchWidth):
            for j in range(searchHeight):
                demo_src[i + j * searchWidth][0][0] = xMinLeft + i * interval
                demo_src[i + j * searchWidth][0][1] = yMinLeft + j * interval
                # demo_src[i + j * searchWidth][0][0] = xMin + i * interval
                # demo_src[i + j * searchWidth][0][1] = yMin + j * interval

        # 对所有关键点进行分类
        region_points = [[] for i in range(len(regions))]
        for i in range(len(demo_src)):
            idx = multi_homography.get_idx(demo_src[i][0],regions)
            region_points[idx].append(demo_src[i])


        # 单应性变换 左图映射到右图的位置，其中M是单应性矩阵
        final_src = []
        final_dst = []
        for i in range(len(region_points)):
            if len(region_points[i])==0:
                continue
            final_src.extend(region_points[i])
            tmp_dst = cv2.perspectiveTransform(np.array(region_points[i]),m_arr[i])
            final_dst.extend(tmp_dst[:])

        final_src = np.array(final_src)
        final_dst = np.array(final_dst)

        # 把差异点画出来
        heightO = max(img1.shape[0], img2.shape[0])
        widthO = img1.shape[1] + img1.shape[1]
        output = np.zeros((heightO, widthO,channel), dtype=np.uint8)
        output[0:img1.shape[0], 0:img1.shape[1]] = img1
        output[0:img2.shape[0], img2.shape[1]:] = img2[:]
        # output2
        output2 = output

        # 转换成KeyPoint类型
        kp_src = [cv2.KeyPoint(final_src[i][0][0], final_src[i][0][1], size)
                  for i in range(final_src.shape[0])]
        kp_dst = [cv2.KeyPoint(final_dst[i][0][0], final_dst[i][0][1], size)
                  for i in range(final_dst.shape[0])]


        # 计算这些关键点的描述子
        descriptors_image1 = get_des_from_kp(img1,kp_src)
        descriptors_image2 = get_des_from_kp(img2,kp_dst)
        # _, descriptors_image1 = orb.compute(img1, kp_src)
        # _, descriptors_image2 = orb.compute(img2, kp_dst)
        # descriptors_image1 = np.asarray(descriptors_image1, np.float32)
        # descriptors_image2 = np.asarray(descriptors_image2, np.float32)

        # 差异点
        diffLeft = []
        diffRight = []
        # 分析差异
        searchNum = min(len(descriptors_image1), len(descriptors_image2))
        for i in range(searchNum):
            difference = math.sqrt(np.sum(np.square(descriptors_image1[i] - descriptors_image2[i])))

            # 右图关键点位置不超出范围
            if (final_src[i][0][1] >= 0) & (final_src[i][0][0] >= 0):
                if difference <= threshold:  # 这里是画绿点
                    cv2.circle(output, (int(final_src[i][0][0]), int(final_src[i][0][1])), 1, (0, 255, 0), 2)
                    cv2.circle(output, (int(final_dst[i][0][0] + width), int(final_dst[i][0][1])), 1, (0, 255, 0), 2)
                if difference > threshold:  # 这里是画红点
                    if func == 1:
                        cv2.circle(output, (int(final_src[i][0][0]), int(final_src[i][0][1])), 1, (0, 0, 255), 2)
                        cv2.circle(output, (int(final_dst[i][0][0] + width), int(final_dst[i][0][1])), 1, (0, 0, 255),
                                   2)
                    if func == 2:
                        diffLeft.append([final_src[i][0][0], final_src[i][0][1]])
                        diffRight.append([final_dst[i][0][0], final_dst[i][0][1]])

        diffLeft = np.array(diffLeft)
        box_list = print_black(width, height, diffLeft, np.ceil(interval))
        # diffRight = np.array(diffRight)
        # box_list = print_black(width, height, diffRight, np.ceil(interval))
        return box_list


