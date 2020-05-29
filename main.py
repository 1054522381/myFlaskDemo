from flask import Flask, request, jsonify
from werkzeug.datastructures import EnvironHeaders

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/testapi')
def test_api():
    """
    请求头：
    Authorization string 必填 eg.'XDS 7.dVkI-SQWxjICYXD_TE54hZGIZwVud18LfXew-Ioorg0'

    请求参数：
    p1 number 必填 取值1、2、3
    p2 string 必填

    返回：
    code number
    data string
    status boolean
    """
    try:
        authorization = request.headers['Authorization']
        if authorization is None or authorization == '' or authorization.isspace():
            raise KeyError
    except KeyError as e:
        return jsonify(code=0, status=False, data='请求授权头是必需的')

    p1 = request.args.get("p1")
    if p1 is None or p1 == '' or p1.isspace():
        return jsonify(code=1, status=False, data='参数p1是必需的，值取1、2、3')
    try:
        p1 = int(p1)
        if p1 not in [1, 2, 3]:
            raise ValueError()
    except ValueError as e:
        return jsonify(code=1, status=False, data='参数p1的值只能取1、2、3')

    p2 = request.args.get("p2")
    if p2 is None or p2 == '' or p2.isspace():
        return jsonify(code=1, status=False, data='参数p2是必需的')

    return jsonify(code=100, status=True, data='请求处理成功')


# 定义door接口，参数p值为"open"时返回开门，为"close"时返回关门
@app.route('/door', methods=["GET"])
def door():
    p = request.args.get("p")
    print(f'type p => {type(p)}')
    if p is None or p == '' or p.isspace():
        return jsonify(code=3, msg="参数p是必需的，值为open或者close")
    if p == 'open':
        return jsonify(code=0, msg="开门")
    elif p == 'close':
        return jsonify(code=1, msg="关门")
    else:
        return jsonify(code=2, msg="参数p值只能选择open或者close")


if __name__ == '__main__':
    # 解决中文乱码的问题，将json数据内的中文正常显示
    app.config['JSON_AS_ASCII'] = False
    app.run()
