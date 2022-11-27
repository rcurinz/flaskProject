from ast import literal_eval

from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def hello_world():  # put application's code here
    return render_template('/mp-view.html', data="data1111")

@app.route('/mp-temuco')
def mp_temuco():
    return render_template('/mp-temuco.html', data="data1111")


@app.route('/datos', methods=['POST'])
def GetData():  # put application's code here
    data = request.data.decode('utf-8')
    data = literal_eval(data)
    #print(data)
    m1 = data['01']
    m2 = data['25']
    m3 = data['10']
    te = data['te']
    print(m1, m2, m3, te)
    return "OK"
    #return render_template('/mp-view.html', data=data)
    #print(m1, m2, m3, te)


@app.route('/estacion1', methods=['POST'])
def esta1():  # put application's code here
    data = request.data.decode('utf-8')
    data = literal_eval(data)
    #print(data)
    m1 = data['01']
    m2 = data['25']
    m3 = data['10']
    te = data['te']
    print(m1, m2, m3, te)
    return jsonify(data)
    #return render_template('/mp-view.html', data=data)
    #print(m1, m2, m3, te)


@socketio.on('estacion1')
def event(data):
    print('Estacion 1 ' + str(data))


@socketio.on('estacion2')
def event(data):
    print('Estacion 2 ' + str(data))


@socketio.on('estacion3')
def event(data):
    print('Estacion 3 ' + str(data))


@socketio.on('estacion4')
def event(data):
    print('Estacion 4 ' + str(data))

@socketio.on('estacion5')
def event(data):
    print('Estacion 5 ' + str(data))


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5050,threaded=True,debug=True, use_reloader=True)
    #app.run(host='0.0.0.0',port=5050,threaded=True,debug=True, use_reloader=True)



#https://python-forum.io/thread-35536.html