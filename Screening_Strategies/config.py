class config:
    def __init__(self) -> None:
        # IOU 界
        self.IOU = 0.8
        # 数据库链接配置
        self.user =  'root'
        self.password = 'password'
        self.host = 'localhost'
        self.database = 'database'
        # 摄像头黑白名单
        self.camera_list_white = {}
        self.camera_list_black = {}
        # 摄像头黑白名单初始化路径
        self.camera_wb_path = 'path'