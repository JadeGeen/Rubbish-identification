import mysql.connector
from .config import config

import sys

# 初始化参数
myconfig = config()

conn = mysql.connector.connect(
    host = myconfig.host,
    user = myconfig.user,
    password = myconfig.password
)

# 创建一个数据库
mycursor = conn.cursor()
mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {myconfig.database}")
conn.close()
print(sys.path)
with open('./Screening_Strategies/data.txt', 'r') as file:
    for line in file:
        cont = list(line.strip().split())
        camera_id = int(cont[0])
        myconfig.camera_list_white[camera_id] = cont[2].split(',')
        myconfig.camera_list_black[camera_id] = cont[3].split(',')