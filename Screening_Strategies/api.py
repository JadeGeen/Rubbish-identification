from database import table_check, data_save, data_load, data_relabel
from Strategies import screening_startegies, my_struct
from init import myconfig
import numpy as np


def api(camera_id:int, time_msg:str, bboxs_list : dict, pic:np.ndarray)->my_struct:
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    :bboxs_list: 框信息(dict, key为label, value为对应bbox)
    :pic: 图片转换的numpy数组
    :return: 自定义数据结构
    """
    black_label_list = myconfig.camera_list_black[camera_id]
    white_label_list = myconfig.camera_list_white[camera_id]
    black_items_bboxs = []
    for i in black_label_list:
        black_items_bboxs += bboxs_list[i]
    white_items_bboxs = []
    for i in white_label_list:
        white_items_bboxs += bboxs_list[i]
    data = my_struct(camera_id, time_msg, [], [], pic)
    # 获取相关摄像头之前的黑白名单
    ctex_white, Pic = data_load(camera_id, 'white')
    ctex_black, Pic = data_load(camera_id, 'black')
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
    return data

# 用于用户查询数据库
def api_search(camera_id:int, time_msg:str):
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    :return: 黑名单框以及图片信息，根据后续要求更改
    """
    # black_label_list = myconfig.camera_list_black[camera_id]
    # bbox_list = []
    # for i in black_label_list:
    #     result = data_load(camera_id=camera_id,label=i, time=time_msg)
    #     bbox_list.append(result)
    bbox_list, pic = data_load(camera_id, 'black', time_msg)
    return (bbox_list, pic)

def api_clear(camera_id:int, time_msg:str)->None:
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    """
    data_relabel(camera_id, 'black', time_msg)
