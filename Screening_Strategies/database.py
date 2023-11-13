import mysql.connector
import numpy as np
import json

from Strategies import  my_struct

user =  'root'
password = 'password'
host = 'localhost'
database = 'database'
# 检查数据表是否创建
def table_check():
    conn = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)
    # 创建一个游标对象
    cursor = conn.cursor()
    # 定义要检查是否存在的表名
    table_name = 'pic_table'
    # 查询 information_schema 中的表信息
    check_table_query = f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table_name}'"
    # 执行查询
    cursor.execute(check_table_query)
    # 获取查询结果
    result = cursor.fetchone()
    if not result:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pic_table (
                camera_id INT,
                time_str VARCHAR(200),
                label INT,
                bboxs_list TEXT,
                pic_array BLOB,
                PRIMARY KEY (camera_id, time_str)
            )
        ''')

        # 提交更改
        conn.commit()
    conn.close()
  
def data_save(data:my_struct)->None:
    """
    :param data: 自定义数据结构
    """
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
    insert_query = 'INSERT INTO pic_table (camera_id, time_str, label, bboxs_list, pic_array) VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(insert_query, (data.camera_id, data.time, data.label, list_value, data.pic_array.tobytes()))

    conn.commit()
    conn.close()

def data_load(camera_id, time = None):
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息, 当未给出时进行摄像头单主键查询
    :return: 自定义数据结构
    """
    conn = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database
)

    cursor = conn.cursor()
    if time != None:
        # 查询数据
        select_query = 'SELECT * FROM pic_table WHERE camera_id = %s AND time_str = %s'
        cursor.execute(select_query, (camera_id, time))

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
            return my_struct(result[0],result[1],result[2],bbox_list,pic_array)
        else:
            return None
    else:
        # 查询数据
        select_query = 'SELECT * FROM pic_table WHERE camera_id = %s'
        cursor.execute(select_query, (camera_id,))

        # 获取查询结果
        result = cursor.fetchall()
        conn.close()
        if result:
            datalist = []
            for _ in result:
                list_value = _[3]
                bbox_list = json.loads(list_value)
                array_str = _[4]
                element_size = np.dtype(np.int32).itemsize  # 这里假设数组是 int32 类型的
                buffer_size = len(array_str)
                adjusted_buffer_size = (buffer_size // element_size) * element_size  # 确保长度是元素大小的整数倍
                # 将调整后的字节串转换为 NumPy 数组
                pic_array = np.frombuffer(array_str[:adjusted_buffer_size], dtype=np.int32)
                tmp = my_struct(_[0],_[1],_[2],bbox_list,pic_array)
                datalist.append(tmp)
            return datalist
        else:
            return None