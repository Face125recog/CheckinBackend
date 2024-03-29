import flask
from flask import *
import json
from utility import *
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route("/admin/login", methods=["POST"])
# 只接受POST方法访问
def admin_login():
    payload = request.json
    print(payload)
    if payload["name"] == "admin" and payload["password"] == "12345":
        return flask.jsonify({
            "data": "12345-12345-12345-12345"
        })
    else:
        return flask.jsonify({
            "errty": "未知名称或者密码不匹配",
            "errmsg": "error"
        }), 401


@app.route("/check_in", methods=["POST"])
def face_match():
    # 默认返回内容
    return_dict = {'data': {
        'name': 'None',
        'identity': None
    },
        'errty': 'null',
        'errmsg': "Null"}

    get_Data = request.get_data()
    get_Data = json.loads(get_Data)

    face = get_Data['face']

    mini_confidence = get_Data['min_confidence']
    print(mini_confidence)
    photo = FaceProcess(face)  # 图片修改
    photo.FaceTrans()
    tuple_name_i, confidence = photo.user_identity()  # 返回id
    if float(0.75) >= confidence:
        return_dict['errty'] = 'Low confidence'
        return_dict['errmsg'] = 'This is  a picture with  low confidence to be anyone in database'
        return json.dumps(return_dict, ensure_ascii=False)
    del photo
    data = {'name': tuple_name_i[0],
            'identity': tuple_name_i[1]
            }
    return json.dumps({"data": data}, ensure_ascii=False)


@app.route("/user/all/count", methods=["GET"])
def count_user():
    user = UserImformation()
    data = user.count_user()
    print(data)
    del user
    return json.dumps({"data": data}, ensure_ascii=False)


@app.route("/user/all", methods=["GET"])
def get_all_user():
    user = UserImformation()
    data = user.return_all_user()
    del user
    return json.dumps({"data": data})


@app.route("/user_register/upload", methods=["POST"])
def user_register_upload():
    # 默认返回内容
    get_Data = request.get_data()
    get_Data = json.loads(get_Data)
    faces = get_Data['faces']
    user = get_Data['user']
    # print(faces)
    # print(user)
    user_faces = FacesStorge(int(user['identity']), user['name'], faces)
    data = user_faces.add_user()
    if data == 1:
        return_dict = {'data': None,
                       'errty': 'id重复',
                       'errmsg': "id重复，写入数据失败"}
        return json.dumps({"data": return_dict})
    else:
        user_faces.write_images()

    del user_faces
    train_model()
    return json.dumps({"data": None})


@app.route("/user/delete", methods=["POST"])
def delete_user_by_id():
    args = request.args.get('uid', '')
    delete_user(args)
    train_model()
    return json.dumps({"data": None})


@app.route("/")
def welcome():
    return "AAA"


if __name__ == "__main__":
    #app.run(host='192.168.1.118', debug=True)
    #app.run(host='10.194.0.180', debug=True)
    app.run(debug=True)
