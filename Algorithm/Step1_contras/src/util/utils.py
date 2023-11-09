# coding:utf-8
import random
import numpy as np
import cv2


# K-means 聚类
# in:二维数据点 xMax,yMax：边界最大值（图像尺寸）
# from scipy.misc import imresize


def Kmeans(input, k, xMax, yMax):
    # 加上分类信息
    keyPoint = [[0 for x in range(3)] for y in range(len(input))]
    for i in range(len(keyPoint)):
        keyPoint[i][0] = input[i][0]
        keyPoint[i][1] = input[i][1]
        keyPoint[i][2] = 999
    # 初始化 k 个中心点
    center = [[0 for x in range(3)] for y in range(k)]
    # radious = [0 for x in range(k)]
    for i in range(k):
        center[i][0] = random.randint(0, xMax)
        center[i][1] = random.randint(0, yMax)

    # 停止迭代的三个条件
    time = 0  # 迭代次数
    timeMax = 30
    changed = 0  # 重新分配
    a = 0.01  # 最小移动与图像尺度的比例
    move = 0  # 所有类中心移动距离小于moveMax
    moveMax = a * xMax

    # 未到最大迭代次数
    while time < timeMax:
        time = time + 1
        # 计算每个点的最近分类
        for i in range(len(keyPoint)):
            dis = -1
            for j in range(k):
                x = keyPoint[i][0] - center[j][0]
                y = keyPoint[i][1] - center[j][1]
                disTemp = x * x + y * y
                # 更新当前最近分类并标记
                if (disTemp < dis) | (dis == -1):
                    dis = disTemp
                    keyPoint[i][2] = j
        # 更新类中心点坐标
        for i in range(k):
            xSum = 0
            ySum = 0
            num = 0
            for j in range(len(keyPoint)):
                if keyPoint[j][2] == i:
                    xSum = xSum + keyPoint[j][0]
                    ySum = ySum + keyPoint[j][1]
                    num = num + 1
            if num != 0:
                center[i][0] = xSum / num
                center[i][1] = ySum / num
    # 记录每个分类的点数量
    for i in range(len(keyPoint)):
        center[keyPoint[i][2]][2] = center[keyPoint[i][2]][2] + 1
    return center


def print_black(width, height, points, interval):
    img = np.zeros([height, width, 3], np.uint8)
    for i in range(len(points)):
        point = points[i]
        x0 = int(point[0] - interval / (2 * np.sqrt(2)))
        y0 = int(point[1] - interval / (2 * np.sqrt(2)))
        cv2.rectangle(img, (x0, y0), (int(x0 + interval), int(y0 + interval)), (255, 255, 255), -1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    num, labels, stats, centroid = cv2.connectedComponentsWithStats(th)
    ######根据外接矩形重新计算面积
    box_list = []
    for info in stats:
        area = info[2] * info[3]
        if area > width * height * 0.01 and area < width * height * 0.8:
            box_list.append(info[:4])
    return box_list


def print_pca_black(res):
    width = len(res[0])
    height = len(res)
    res = res.astype(np.uint8)
    num, labels, stats, centroid = cv2.connectedComponentsWithStats(res)
    ######根据外接矩形重新计算面积
    box_list = []
    for info in stats:
        area = info[2] * info[3]
        if area > width * height * 0.01 and area < width * height * 0.8:
            box_list.append(info[:4])
    return box_list


def resize_img(image1):
    ## 先进行放缩,将图片缩小三倍，把图片缩小到1k以内。
    l = max(image1.shape)
    upperbound = 1000
    if l > upperbound:
        multiple = l / 1000
        new_size = np.array(image1.shape) / multiple
    else:
        new_size = np.array(image1.shape)
    # print(new_size)

    new_size = new_size / 5
    new_size = new_size.astype(int) * 5
    # image1 = imresize(image1, (new_size))
    return image1

# 十二色相环
# RGB_LIST = [[255,0,0],[255,51,0],[255,102,0],[255,153,0],[255,255,0],
#             [153,255,0],[0,255,0],[0,255,255],[0,0,255],[102,0,255],
#             [255,0,255],[255,0,102]]
RGB_LIST = [[0,255,0],[255,0,0],[0,0,255],[255,255,0],[0,255,255],]

# kp_list1, kp_list2 是匹配好的关键点list
def drawMatches(img1, kp_list1, img2, kp_list2):
    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for j in range(len(kp_list1)):
        kp1 = kp_list1[j]
        kp2 = kp_list2[j]
        # 每个list采用一种颜色
        rgb = RGB_LIST[j % len(RGB_LIST)]
        a = int(rgb[2])
        b = int(rgb[1])
        c = int(rgb[0])
        for i in range(len(kp1)):
            # x - columns
            # y - rows
            (x1,y1) = (kp1[i][0][0],kp1[i][0][1])
            (x2,y2) = (kp2[i][0][0],kp2[i][0][1])

            # Draw a small circle at both co-ordinates
            # radius 4
            # thickness
            cv2.circle(out, (int(np.round(x1)),int(np.round(y1))), 2, (a, b, c), 1)      #画圆，cv2.circle()参考官方文档
            cv2.circle(out, (int(np.round(x2)+cols1),int(np.round(y2))), 2, (a, b, c), 1)

            # Draw a line in between the two points
            # thickness = 1
            # colour blue
            cv2.line(out, (int(np.round(x1)),int(np.round(y1))), (int(np.round(x2)+cols1),int(np.round(y2))), (a, b, c), 1)  #画线，cv2.line()参考官方文档

    # Also return the image if you'd like a copy
    return out