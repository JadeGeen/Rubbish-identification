from match import img_similarity
import numpy as np
class my_struct:
    def __init__(self, camera_id, time_msg, bboxs_list, pic_array):
        self.camera_id = camera_id
        self.time = time_msg
        self.bboxs_list = bboxs_list
        self.pic_array = pic_array


def screening_startegies(pic : my_struct, ctex:my_struct)->None:
# TODO：筛选策略，具体参数和返回值待定
    match_bboxes(pic.bboxs_list, ctex.bboxs_list)

def Iou(box1, box2, wh=False):
    if wh == False:
        xmin1, ymin1, xmax1, ymax1 = box1
        xmin2, ymin2, xmax2, ymax2 = box2
    else:
        xmin1, ymin1 = int(box1[0]-box1[2]/2.0), int(box1[1]-box1[3]/2.0)
        xmax1, ymax1 = int(box1[0]+box1[2]/2.0), int(box1[1]+box1[3]/2.0)
        xmin2, ymin2 = int(box2[0]-box2[2]/2.0), int(box2[1]-box2[3]/2.0)
        xmax2, ymax2 = int(box2[0]+box2[2]/2.0), int(box2[1]+box2[3]/2.0)
    # 获取矩形框交集对应的左上角和右下角的坐标（intersection）
    xx1 = np.max([xmin1, xmin2])
    yy1 = np.max([ymin1, ymin2])
    xx2 = np.min([xmax1, xmax2])
    yy2 = np.min([ymax1, ymax2])	
    # 计算两个矩形框面积
    area1 = (xmax1-xmin1) * (ymax1-ymin1) 
    area2 = (xmax2-xmin2) * (ymax2-ymin2)
    inter_area = (np.max([0, xx2-xx1])) * (np.max([0, yy2-yy1]))
    iou = inter_area / (area1+area2-inter_area+1e-6)
    return iou

def match_bboxes(bboxes1, bboxes2):
    for box1 in bboxes1:
        max_iou = 0
        match = None
        for box2 in bboxes2:
            BOX1 = (box1[0], box1[1], box1[0]+box1[2], box1[1]+box1[3])
            BOX2 = (box2[0], box2[1], box2[0]+box2[2], box2[1]+box2[3])
            iou = Iou(BOX1, BOX2)
            if iou > max_iou:
                max_iou = iou
                match = box2

        if max_iou > 0.8:
            box1[4] = match[4]