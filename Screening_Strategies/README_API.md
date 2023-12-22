# API定义

## API FOR USER

````
api_save(camera_id, time_msg, bboxs_list, pic) # 存储算法分类结果
input : {
    camera_id : int # 摄像头编号
    time_msg : str # 时间信息 参考格式：2023-12-31 23:59:59
    bboxs_list : dict # 算法输出的框信息(dict, key为label, value为对应bbox)
    pic : ndarray # 基准图片
}
output : {
    res : tuple(list[], ndarray) # 返回一个二元元组，前一部分为垃圾对应的框信息，后者为图片
}

api_search(camera_id, time_msg) # 查询对应时间相关摄像头的信息
input : {
    camera_id : int # 摄像头编号
    time_msg : str # 时间信息 参考格式：2023-12-31 23:59:59
}
output : {
    res : tuple(list[], ndarray) # 返回一个二元元组，前一部分为垃圾对应的框信息，后者为图片
}

api_clear(camera_id, time_msg) # 将对应摄像头对应时间的分类结果的黑名单结果全部改为白名单
input : {
    camera_id : int # 摄像头编号
    time_msg : str # 时间信息 参考格式：2023-12-31 23:59:59
}
output : {
    res : tuple(list[], ndarray) # 返回一个二元元组，前一部分为垃圾对应的框信息，后者为图片
}

api_wblist_change(camera_id, label, wb, tag) # 修改摄像头黑白名单
input : {
    camera_id : int # 摄像头编号
    label : str # 要进行操作的标签
    wb: int # 0为对白名单进行操作,1为对黑名单进行操作
    tag: bool # 操作类型,True为添加,False为删除
}
output : {
    res : None
}
````