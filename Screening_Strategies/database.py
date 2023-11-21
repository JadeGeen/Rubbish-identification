import mysql.connector
import numpy as np
import json

from Strategies import  my_struct

user =  'root'
password = 'password'
host = 'localhost'
database = 'database'
# 检查数据表是否创建
def table_check(camera_id : int):
    conn = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)
    # 创建一个游标对象
    cursor = conn.cursor()
    # 定义要检查是否存在的表名
    table_name = f'camera_table_{camera_id}'
    # 查询 information_schema 中的表信息
    check_table_query = f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table_name}'"
    # 执行查询
    cursor.execute(check_table_query)
    # 获取查询结果
    result = cursor.fetchone()
    if not result:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT,
                time_str VARCHAR(200),
                bboxs_list TEXT,
                pic_array BLOB,
                PRIMARY KEY (id, time_str)
            )
        ''')

        # 提交更改
        conn.commit()
    conn.close()
  
def data_save(data:my_struct)->None:
    """
    :param data: 自定义数据结构
    """
    # 检查表格是否已经创立
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
    list_value = json.dumps(data.bboxs_list)
    table_name = f'camera_table_{data.camera_id}'
    insert_query = f'INSERT INTO {table_name} (time_str, bboxs_list, pic_array) VALUES (%s, %s, %s)'
    cursor.execute(insert_query, (data.time, list_value, data.pic_array.tobytes()))

    conn.commit()
    conn.close()

def data_load(camera_id, time = None):
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息, 当未给出时进行摄像头单主键查询
    :return: 自定义数据结构
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
        select_query = f'SELECT * FROM {table_name} WHERE time_str = %s'
        cursor.execute(select_query, (time,))

        # 获取查询结果
        result = cursor.fetchone()
        conn.close()
        if result:
            list_value = result[2]
            bbox_list = json.loads(list_value)
            array_str = result[3]
            # pic_array = np.frombuffer(array_str)

            # 计算 NumPy 数据类型的元素大小
            element_size = np.dtype(np.int32).itemsize  # 这里假设数组是 int32 类型的
            buffer_size = len(array_str)
            adjusted_buffer_size = (buffer_size // element_size) * element_size  # 确保长度是元素大小的整数倍
            # 将调整后的字节串转换为 NumPy 数组
            pic_array = np.frombuffer(array_str[:adjusted_buffer_size], dtype=np.int32)
            return my_struct(camera_id, time, bbox_list,pic_array)
        else:
            return None
    else:
        # 查询最后插入的一行数据
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = (SELECT MAX(id) FROM {table_name})")

        # 获取查询结果
        result = cursor.fetchone()
        conn.close()
        if result:
            list_value = result[2]
            bbox_list = json.loads(list_value)
            array_str = result[3]
            # pic_array = np.frombuffer(array_str)

            # 计算 NumPy 数据类型的元素大小
            element_size = np.dtype(np.int32).itemsize  # 这里假设数组是 int32 类型的
            buffer_size = len(array_str)
            adjusted_buffer_size = (buffer_size // element_size) * element_size  # 确保长度是元素大小的整数倍
            # 将调整后的字节串转换为 NumPy 数组
            pic_array = np.frombuffer(array_str[:adjusted_buffer_size], dtype=np.int32)
            return my_struct(camera_id,result[1],bbox_list,pic_array)
        else:
            return None
        
def data_relabel(camera_id, time)->my_struct:
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息, 当未给出时进行摄像头单主键查询
    :return: 自定义数据结构
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
    select_query = f'SELECT * FROM {table_name} WHERE time_str = %s'
    cursor.execute(select_query, (time,))
    # 获取查询结果
    result = cursor.fetchone()
    
    if result:
        list_value = result[2]
        bbox_list = json.loads(list_value)
        for i in bbox_list:
            i[4] = 0
        list_value = json.dumps(bbox_list)
        update_query = f'UPDATE {table_name} SET bboxs_list= %s WHERE time_str=%s'
        cursor.excute(update_query,(list_value,time))
        conn.close()
        array_str = result[3]
        element_size = np.dtype(np.int32).itemsize  # 这里假设数组是 int32 类型的
        buffer_size = len(array_str)
        adjusted_buffer_size = (buffer_size // element_size) * element_size  # 确保长度是元素大小的整数倍
        # 将调整后的字节串转换为 NumPy 数组
        pic_array = np.frombuffer(array_str[:adjusted_buffer_size], dtype=np.int32)
        return my_struct(camera_id, time, bbox_list,pic_array)
    else:
        conn.close()
        return None