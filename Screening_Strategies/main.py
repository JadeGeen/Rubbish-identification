from flask import Flask, request
from secne_class import single_scene, scene_group
app = Flask(__name__)

ALL_SCENE_GROPU = []

@app.route('/url', methods=['GET'])
def return_scene()->single_scene:
    searchlists = request.get_json()
    # TODO: 重新封装
    return searchlists

if __name__ == '__main__':
    new_data = app.run()
    if len(ALL_SCENE_GROPU) == 0:
        new_scene_group = scene_group(new_data.camera_no)
        new_scene_group.add_scene(new_data)
        ALL_SCENE_GROPU.append(new_scene_group)
    else:
        flag = False
        for i in ALL_SCENE_GROPU:
            if i.no == new_data.camera_no:
                i.add_scene(new_data)
                flag == True
                break
        if flag == False:
            new_scene_group = scene_group(new_data.camera_no)
            new_scene_group.add_scene(new_data)
            ALL_SCENE_GROPU.append(new_scene_group)