import mysql.connector
import numpy as np
import json
from init import myconfig
from Strategies import  my_struct

user =  myconfig.user
password = myconfig.password
host = myconfig.host
database = myconfig.database
def table_check(camera_id : int):
    """
    :param camera_id: 摄像头id
    检测表是否存在以建表
    """
    conn = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)
    cursor = conn.cursor()
    table_name = f'camera_table_{camera_id}'
    check_table_query = f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table_name}'"
    cursor.execute(check_table_query)
    result = cursor.fetchone()
    if not result:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT,
                time_str VARCHAR(255),
                label VARCHAR(255),
                bboxs_list TEXT,
                pic_array BLOB,
                PRIMARY KEY (id, time_str, label)
            )
        ''')

        conn.commit()
    conn.close()
  
def data_save(data:my_struct)->None:
    """
    :param data: 自定义数据结构
    """
    table_check(data.camera_id)
    
    conn = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)
    cursor = conn.cursor()
    # 插入数据
    # 将嵌套列表转换为JSON字符串进行存储
    white_list_value = json.dumps(data.white_item_bbox)
    black_list_value = json.dumps(data.black_item_bbox)
    table_name = f'camera_table_{data.camera_id}'
    insert_query1 = f'INSERT INTO {table_name} (time_str, label, bboxs_list, pic_array) VALUES (%s, %s, %s, %s)'
    cursor.execute(insert_query1, (data.time, 'white', white_list_value, data.pic_array.tobytes()))
    insert_query2 = f'INSERT INTO {table_name} (time_str, label, bboxs_list, pic_array) VALUES (%s, %s, %s, %s)'
    cursor.execute(insert_query2, (data.time, 'black', black_list_value, data.pic_array.tobytes()))

    conn.commit()
    cursor.close()
    conn.close()

def data_load(camera_id, label, time=None):
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息, 当未给出时进行摄像头单主键查询
    :return: 框以及图片
    """
    table_check(camera_id)

    conn = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)
    table_name = f'camera_table_{camera_id}'
    cursor = conn.cursor()
    if time != None:
        # 查询数据
        select_query = f'SELECT * FROM {table_name} WHERE time_str = %s AND label = %s'
        cursor.execute(select_query, (time,label))
        # 获取查询结果
        result = cursor.fetchone()
        conn.close()
        if result:
            list_value = result[3]
            bbox_list = json.loads(list_value)
            array_str = result[4]
            # pic_array = np.frombuffer(array_str)
            # 计算 NumPy 数据类型的元素大小
            element_size = np.dtype(np.int32).itemsize  # 这里假设数组是 int32 类型的
            buffer_size = len(array_str)
            adjusted_buffer_size = (buffer_size // element_size) * element_size  # 确保长度是元素大小的整数倍
            # 将调整后的字节串转换为 NumPy 数组
            pic_array = np.frombuffer(array_str[:adjusted_buffer_size], dtype=np.int32)
            return bbox_list, pic_array
        else:
            return None
    else:
        # 查询该标签下最后插入的一行数据
        cursor.execute(f"SELECT id FROM {table_name} WHERE label = %s ORDER BY id DESC LIMIT 1", label)
        # 获取查询结果
        result = cursor.fetchone()
        conn.close()
        if result:
            list_value = result[3]
            bbox_list = json.loads(list_value)
            array_str = result[4]
            # pic_array = np.frombuffer(array_str)
            # 计算 NumPy 数据类型的元素大小
            element_size = np.dtype(np.int32).itemsize  # 这里假设数组是 int32 类型的
            buffer_size = len(array_str)
            adjusted_buffer_size = (buffer_size // element_size) * element_size  # 确保长度是元素大小的整数倍
            # 将调整后的字节串转换为 NumPy 数组
            pic_array = np.frombuffer(array_str[:adjusted_buffer_size], dtype=np.int32)
            return bbox_list, pic_array
        else:
            return None
        
def data_relabel(camera_id, time):
    """
    :param camera_id: 摄像头编号
    :param label: 相关标签
    :param time: 时间信息, 当未给出时进行摄像头单主键查询
    :return: None
    更新对应黑名单物品为白名单物品
    """
    table_check(camera_id)

    conn = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)
    table_name = f'camera_table_{camera_id}'
    cursor = conn.cursor()
    # delete_query = f"DELETE FROM {table_name} WHERE time_str = %s AND label = %s"
    # cursor.execute(delete_query, (time, label))
    # conn.commit()
    # cursor.close()
    # conn.close()

    select_query = f'SELECT * FROM {table_name} WHERE time_str = %s AND label = %s'
    cursor.execute(select_query, (time, 'black'))
    result1 = cursor.fetchone()
    cursor.execute(select_query, (time, 'white'))
    result2 = cursor.fetchone()
    
    if result1:
        black_list_value = result1[3]
        black_bbox_list = json.loads(black_list_value)
        white_list_value = result2[3]
        white_bbox_list = json.loads(white_list_value)
        white_bbox_list += black_bbox_list
        black_bbox_list = []
        white_list = json.dumps(white_bbox_list)
        black_list = json.dumps(black_bbox_list)
        update_query = f"UPDATE {table_name} SET bboxs_list = %s WHERE id = %s"
        cursor.execute(update_query, (black_list, result1[0]))
        cursor.execute(update_query, (white_list, result2[0]))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        cursor.close()
        conn.close()