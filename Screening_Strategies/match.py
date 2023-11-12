import cv2
# 基于ORB自定义计算两个图片相似度函数
def img_similarity(img1:cv2.UMat, img2:cv2.UMat):
    """
    :param img1: 图片1
    :param img2: 图片2
    :return: 图片相似度
    """
    
    # 转换为灰度图像（如果不是灰度图）
    if len(img1.shape) > 2:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    if len(img2.shape) > 2:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
 
 
    # 初始化ORB检测器
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # 提取并计算特征点
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)
    good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    similary = float(len(good))/len(matches)
    # print("两张图片相似度为:%s" % similary)
    return similary