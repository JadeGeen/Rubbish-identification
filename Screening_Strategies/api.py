from database import data_save, data_load, data_relabel
from Strategies import screening_startegies, my_struct
from init import myconfig
import numpy as np


def api_save(camera_id:int, time_msg:str, bboxs_list : dict, pic:np.ndarray):
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    :bboxs_list: 框信息(dict, key为label, value为对应bbox)
    :pic: 图片转换的numpy数组
    :return: tuple,
    """
    black_label_list = myconfig.camera_list_black[camera_id]
    white_label_list = myconfig.camera_list_white[camera_id]
    black_items_bboxs = []
    for i in black_label_list:
        black_items_bboxs += bboxs_list[i]
    white_items_bboxs = []
    for i in white_label_list:
        white_items_bboxs += bboxs_list[i]
    data = my_struct(camera_id, time_msg, [], [], None)
    # 获取相关摄像头之前的黑白名单
    ctex_white, ctex_black, Pic = data_load(camera_id)
    ctext = []
    for i in ctex_white:
        box_label = i.append('white')
        ctext.append(box_label)
    for i in ctex_black:
        box_label = i.append('black')
        ctext.append(box_label)
    # 筛选获取新label
    screening_startegies(data, white_items_bboxs, black_items_bboxs, ctext)
    # 存储筛选后的数据
    data_save(data)
    return data.black_item_bbox, data.pic_array

# 用于用户查询数据库
def api_search(camera_id:int, time_msg:str):
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    :return: 黑名单框以及图片信息，根据后续要求更改
    """

    white_bbox_list, black_bbox_list, pic = data_load(camera_id, time_msg)
    return (black_bbox_list, pic)

def api_clear(camera_id:int, time_msg:str):
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    """
    data_relabel(camera_id, 'black', time_msg)
    white_bbox_list, black_bbox_list, pic = data_load(camera_id, time_msg)
    return (black_bbox_list, pic)

def api_wblist_change(camera_id:int, label, wb:int, tag:bool):
    """
    :param camera_id: 摄像头编号
    :param label: 要进行操作的标签
    :param wb: 0为对白名单进行操作,1为对黑名单进行操作
    :param tag: 操作类型,True为添加,False为删除
    逐个增添或删改任意摄像头的黑白名单
    """
    target_list = myconfig.camera_list_white if wb == 0 else myconfig.camera_list_black
    if tag == True:
        if camera_id in target_list.keys():
            target_list[camera_id].append(label)
        else:
            target_list[camera_id] = [label]
    else:
        if camera_id in target_list.keys():
            target_list[camera_id].remove(label)