import os
import requests
from flask import Flask, session,  render_template, request, jsonify
from flask import Flask
from flask_socketio import SocketIO, emit
# print('hello')
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

global Names
Names = []
global Channels
Channels = []
global univdict
univdict = {}
global lastchannel
lastchannel = "Choose..."


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/channels", methods=["GET"])
def channels():
    global Channels
    return jsonify(Channels)

@app.route("/channeladd", methods=["POST"])
def addchannel():
    global univdict
    global Channels
    channelname = request.form.get('name')
    Channels.append(channelname)
    univdict[channelname] = []  
    # print(univdict)
    return jsonify(Channels)

@app.route("/channelset", methods=["POST"])
def loadmessage():
    global univdict
    global lastchannel
    name = request.form.get('channel')
    lastchannel = name
    nowcase = univdict[name]
    # print(nowcase)
    return jsonify(nowcase)

@app.route("/sendname", methods=["POST"])
def send():
    global lastchannel
    print(lastchannel, "hi")
    return jsonify(lastchannel, )

@app.route("/lastchannel", methods=["POST"])
def last_channel():
    global univdict
    lastchannel1 = request.form.get('channel2')
    # print(lastchannel1)
    nowcase = univdict[lastchannel1]
    # print(nowcase)
    return jsonify(nowcase)

@app.route("/delete", methods=["POST"])
def delete():
    global univdict
    message = request.form.get('message')
    channel = request.form.get('channel') 
    time = request.form.get('time') 
    user = request.form.get('user') 
    dictnow =  {"message": message, 'user': user, 'time': time, 'channel':channel}
    univdict[channel].remove(dictnow)
    print('message removed from server')


@socketio.on('send_message')
def post(data):
    global univdict
    message = data['message']
    channel = data['channel']
    # print(channel) 
    time = data['time']
    user = data['user']
    univdict[channel].append({"message": message, 'user': user, 'time': time, 'channel':channel})
    if len(univdict[channel]) > 100:
        univdict[channel] = univdict[channel][1:]
    emit('announce message', {"message": message, 'user': user, 'time': time, 'channel': channel}, broadcast=True)
    return None
    # print("messages for {} is {}".format(channel, univdict[channel]))

@socketio.on('delete')
def delete2(info):
    channelnow = info['channel']
    print(channelnow, 'hihola')
    emit('reload message', {'channel': channelnow}, broadcast=True)
    return None

# @socketio.on('hello')
# def see(data):
#     print(data["message"])
#     emit('announce message', {"message": data["message"]}, broadcast=True)