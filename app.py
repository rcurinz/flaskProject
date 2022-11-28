from ast import literal_eval

from flask import Flask, request, render_template, jsonify,Response, stream_with_context
from flask_socketio import SocketIO, emit
from threading import Lock
import json
import random as ra
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins="*")
ra.seed()

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

def Generate():
    dData = {                           # Datos Ambientales
        '01': ra.randint(+0o5, +20),    # MP 1.0 ug/m3
        '25': ra.randint(+0o5, +20),    # MP 2.5 ug/m3
        '10': ra.randint(+0o5, +20),    # MP 10 ug/m3
        'te': ra.randint(-10, +10),     # Temperatura °C
    }

    return dData

@app.route('/')
def hello_world():  # put application's code here
    return render_template('/mp-view.html', data="data1111")

@app.route('/mp-temuco')
def mp_temuco():
    return render_template('/mp-temuco.html', data="data1111")

@app.route('/mapas')
def mapas():
    return render_template('/mapas.html', data="data1111")


@app.route("/pregunta1", methods=['GET','POST'])
def pregunta1():
    data = request.data.decode('utf-8')
    data = literal_eval(data)
    return data

@app.route("/pregunta_1")
def pregunta_1():
    return render_template('/pregunta1.html', data = "data1111")



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
    #print(m1, m2, m3, te)
    return "OK"

@app.route('/chart-data',methods=['GET','POST'])
def chart_data():
    def generate_random_data():
        while True:
            data = Generate()
            json_data = json.dumps(
                {'mp1': data['01'],
                 'mp2': data['25'],
                 'mp3': data['10'],
                 'te': data['te'],
                 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            )
            yield f"data:{json_data}\n\n"
            time.sleep(5)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


@socketio.on('estacion1')
def event(data):
    print('Estacion 1 ' + str(data))
    emit('estacion_1', {'data':data}, broadcast=True)


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