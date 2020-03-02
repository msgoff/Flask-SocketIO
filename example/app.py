#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import (
    SocketIO,
    emit,
    join_room,
    leave_room,
    close_room,
    rooms,
    disconnect,
)

import pprint
import json
from tatsu import parse
import tatsu
from tatsu.util import asjson

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def valid_expression(expression):
    try:
        grammar = open("grammars/calc.ebnf").read()
        parser = tatsu.compile(grammar)
        ast = parser.parse(expression)
        return ast
    except:
        return False


def store_results(data):
    import redis
    import json

    r = redis.StrictRedis()
    r.execute_command("JSON.SET", "doc", ".", json.dumps(data))
    # reply = json.loads(r.execute_command('JSON.GET', 'doc'))


def parse_expression(expression):
    # if expression is valid, return ast
    ast = valid_expression(expression)
    if ast:
        # pprint.pprint(ast, indent=2, width=20)
        data = json.dumps(asjson(ast), indent=2)
        store_results(data)
        return data


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit(
            "my_response",
            {"data": "Server generated event", "count": count},
            namespace="/test",
        )


@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)


@socketio.on("my_event", namespace="/test")
def test_message(message):
    data = parse_expression(message["data"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("my_response", {"data": data, "count": session["receive_count"]})


@socketio.on("my_broadcast_event", namespace="/test")
def test_broadcast_message(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        broadcast=True,
    )


@socketio.on("join", namespace="/test")
def join(message):
    join_room(message["room"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": "In rooms: " + ", ".join(rooms()), "count": session["receive_count"]},
    )


@socketio.on("leave", namespace="/test")
def leave(message):
    leave_room(message["room"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": "In rooms: " + ", ".join(rooms()), "count": session["receive_count"]},
    )


@socketio.on("close_room", namespace="/test")
def close(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {
            "data": "Room " + message["room"] + " is closing.",
            "count": session["receive_count"],
        },
        room=message["room"],
    )
    close_room(message["room"])


@socketio.on("my_room_event", namespace="/test")
def send_room_message(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        room=message["room"],
    )


@socketio.on("disconnect_request", namespace="/test")
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session["receive_count"] = session.get("receive_count", 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit(
        "my_response",
        {"data": "Disconnected!", "count": session["receive_count"]},
        callback=can_disconnect,
    )


@socketio.on("my_ping", namespace="/test")
def ping_pong():
    emit("my_pong")


@socketio.on("connect", namespace="/test")
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit("my_response", {"data": "Connected", "count": 0})


@socketio.on("disconnect", namespace="/test")
def test_disconnect():
    print("Client disconnected", request.sid)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
