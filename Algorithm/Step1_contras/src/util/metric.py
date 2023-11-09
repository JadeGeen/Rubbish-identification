import numpy as np

def cal_intersection(box1,box2):
    # box: x1,y1,w,h
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[0]+box1[2], box2[0]+box2[2])
    y2 = min(box1[1]+box1[3], box2[1]+box2[3])
    # cal intersection
    intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    return intersection

def cal_area(box_list1,box_list2):
    # box: x1,x2,w,h
    total_area1 = 0
    total_area2 = 0
    inter_area = 0
    for box1 in box_list1:
        total_area1 += box1[2]*box1[3]
        for box2 in box_list2:
            inter_area += cal_intersection(box1,box2)

    for box2 in box_list2:
        total_area2 += box2[2]*box2[3]
    return total_area1,total_area2,inter_area


def cal_area_with_img(box_list1,box_list2,width,height):
    arr1 = np.zeros((width,height))
    arr2 = np.zeros((width,height))
    for box in box_list1:
        arr1[box[0]:box[0]+box[2],box[1]:box[1]+box[2]]=1
    for box in box_list2:
        arr2[box[0]:box[0]+box[2],box[1]:box[1]+box[2]]=1
    area1 = sum(sum(arr1))
    area2 = sum(sum(arr2))
    
    intersection = arr1*arr2
    iou = sum(sum(intersection))
    return area1,area2,iou
    
