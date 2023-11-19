from database import table_check, data_save, data_load, data_relabel
from Strategies import screening_startegies, my_struct
import numpy as np


def api(camera_id:int, time_msg:str, label, bboxs_list : list, pic:np.ndarray)->my_struct:
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    :bboxs_list: 框信息(包含x坐标,y坐标,长,宽以及label)
    :pic: 图片转换的numpy数组
    :return: 自定义数据结构
    """
    data = my_struct(camera_id=camera_id, time_msg=time_msg, bboxs_list= bboxs_list, pic_array=pic)
    # 获取相关摄像头的上一条存储信息
    ctext = data_load(data.camera_id)
    # 筛选获取新label
    screening_startegies(data, ctext)
    # 存储筛选后的数据
    data_save(data)
    return data

# 用于用户查询数据库
def api_search(camera_id:int, time_msg:str)->my_struct:
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    :return: 框信息，根据后续要求更改
    """
    result = data_load(camera_id=camera_id, time=time_msg)
    return result.bboxs_list

def api_clear(camera_id:int, time_msg:str)->my_struct:
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    """
    result = data_relabel(camera_id=camera_id, time=time_msg)
    return result.bboxs_list
