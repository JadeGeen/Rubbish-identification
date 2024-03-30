import mysql.connector
import numpy as np
import json
from .init import myconfig
from .Strategies import  my_struct
from datetime import datetime, timedelta

user =  myconfig.user
password = myconfig.password
host = myconfig.host
database = myconfig.database
def table_check():
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
    # table_name = f'camera_table_{camera_id}'
    table_name = 'Last_info'
    check_table_query = f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table_name}'"
    cursor.execute(check_table_query)
    result = cursor.fetchone()
    if not result:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT PRIMARY KEY,
                white_bboxs_list TEXT,
                black_bboxs_list TEXT,
                pic_array BLOB
            )
        ''')
        conn.commit()
    conn.close()
  
def data_save(data:my_struct)->None:
    """
    :param data: 自定义数据结构
    """
    table_check()

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
    
    table_name = 'Last_info'
    update_query = f"UPDATE {table_name} SET white_bboxs_list = %s, black_bboxs_list = %s, pic_array = %s WHERE id = %s"
    cursor.execute(update_query, (white_list_value, black_list_value, data.pic_array.tobytes(), data.camera_id))
    # table_name = f'camera_table_{data.camera_id}'
    # formatted_time = datetime.strptime(data.time, '%Y-%m-%d %H:%M:%S')
    # table_name = f'camera_table_{data.camera_id}'
    # insert_query = f'INSERT INTO {table_name} (time_str, white_bboxs_list, black_bboxs_list, pic_array) VALUES (%s, %s, %s, %s)'
    # cursor.execute(insert_query, (formatted_time, white_list_value, black_list_value, data.pic_array.tobytes()))

    # cleanup_threshold = datetime.now() - timedelta(days=30)
    # delete_query = f"DELETE FROM {table_name} WHERE time_str < '{cleanup_threshold}'"
    # cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()

def data_load(camera_id):
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
    # table_name = f'camera_table_{camera_id}'
    cursor = conn.cursor()
    table_name = 'Last_info'
    cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (camera_id,))
    # 获取查询结果
    result = cursor.fetchone()
    conn.close()
    if result:
        list_value = result[1]
        white_bbox_list = json.loads(list_value)
        list_value_2 = result[2]
        black_bbox_list = json.loads(list_value_2)
        array_str = result[3]
        # pic_array = np.frombuffer(array_str)
        # 计算 NumPy 数据类型的元素大小
        element_size = np.dtype(np.int32).itemsize  # 这里假设数组是 int32 类型的
        buffer_size = len(array_str)
        adjusted_buffer_size = (buffer_size // element_size) * element_size  # 确保长度是元素大小的整数倍
        # 将调整后的字节串转换为 NumPy 数组
        pic_array = np.frombuffer(array_str[:adjusted_buffer_size], dtype=np.int32)
        return white_bbox_list, black_bbox_list, pic_array
    else:
        return None
        
def data_relabel(camera_id):
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
    table_name = 'Last_info'
    cursor = conn.cursor()
    # formatted_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    select_query = f'SELECT * FROM {table_name} WHERE id = %s'
    cursor.execute(select_query, (camera_id,))
    result = cursor.fetchone()
    
    if result:
        black_list_value = result[2]
        black_bbox_list = json.loads(black_list_value)
        white_list_value = result[1]
        white_bbox_list = json.loads(white_list_value)
        white_bbox_list += black_bbox_list
        black_bbox_list = []
        white_list = json.dumps(white_bbox_list)
        black_list = json.dumps(black_bbox_list)
        update_query = f"UPDATE {table_name} SET white_bboxs_list = %s, black_bboxs_list = %s WHERE id = %s"
        cursor.execute(update_query, (white_list, black_list, result[0]))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        cursor.close()
        conn.close()