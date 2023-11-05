from match import img_similarity
class single_scene():
    def __init__(self,time,table,camera_no,**args) -> None:
        self.time = time
        self.table = table
        self.camera_no = camera_no
        self.clear = False
        self.other_args = []
    def clear_judge(self, env, clear_scene):
        # TODO: jugde if clear or not
        '''
        根据上下文，以及对照图（如果有的话）
        暂且拟定于基于时间，基于图片相似度，基于用户命令进行判断，
        等待获取算法服务器所传输json结构后实现
        ''' 
        pass

class scene_group():
    def __init__(self, camera_no, clear_scene=None) -> None:
        self.no = camera_no
        self.scenes = []
        self.clear_scene = clear_scene

    def group_sorted(self):
        self.scenes = sorted(self.scenes, lambda x:x.time)

    def add_scene(self, new_scene: single_scene) ->None:
        if new_scene.no != self.camera_no:
            return 
        else:
            self.scenes.append(single_scene)
            self.group_sorted()
            new_scene.clear_judge(self.scenes, self.clear_scene)
    