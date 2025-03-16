from flask import Flask, render_template, request, jsonify
import paramiko
import psutil
import flask_socketio

app = Flask(__name__)
socketio = flask_socketio.SocketIO(app)

# SSH Connection Function
def ssh_connect(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client

if __name__ == '__main__':
    socketio.run(app)