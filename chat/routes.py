import uuid

from flask import request, render_template, Blueprint, session, flash, redirect, url_for
from flask_socketio import SocketIO, emit

from chat.room import Room, ROOMS

router = Blueprint('main', __name__)
socketio = SocketIO()

SECRET = 'secret'


@router.route('/', methods=['GET', 'POST'])
def index():
    print(ROOMS)
    return render_template('index.html')


@router.route('/enter', methods=['GET', 'POST'])
def create_room():
    if request.method == "POST":
        room_pass = request.form.get('passphrase')
        new_room = Room.create_room(room_pass)
        user_id = str(uuid.uuid4())
        new_room.add_user(user_id)
        session['user_id'] = user_id
        session['room_name'] = new_room.name
        flash('Room created successfully', 'info')
        return redirect(url_for('main.chat_page'))
    else:
        return render_template('create_room.html')


@router.route('/join', methods=['GET', 'POST'])
def join_room():
    if request.method == "POST":
        room_pass = request.form.get('passphrase')
        for room in ROOMS:
            if room.passphrase == room_pass:
                user_id = str(uuid.uuid4())
                room.add_user(user_id)
                session['user_id'] = user_id
                session['room_name'] = room.name
                return redirect(url_for('main.chat_page'))
        flash('Room not found', 'error')
        return render_template('join_room.html')
    else:
        return render_template('join_room.html')


@router.route('/leave', methods=['POST'])
def leave_room():
    user_id = session.pop('user_id', None)
    room_name = session.pop('room_name', None)
    if not room_name or not user_id:
        return redirect(url_for('main.index'))
    for room in ROOMS:
        if room.name == room_name:
            room.remove_user(user_id)
            if len(room.users) == 0:
                Room.destroy_room(room)
            return redirect(url_for('main.index'))


@router.route('/chat', methods=['GET', 'POST'])
def chat_page():
    return render_template('chat_page.html')


@socketio.on('connect')
def handle_connect():
    user_id = session['user_id']
    print(f'Client {user_id} connected')
    emit('user_connected',user_id)


@socketio.on('send_message')
def handle_send_message(json):
    if json['user_id'] != session['user_id']:
        flash('User ID mismatch')
        return redirect(url_for('main.index'))
    emit('send_message', json, broadcast=True)


@socketio.on('send_user_id')
def send_user_id():
    print('Sending user ID')
    emit('user_id', {'user_id': session['user_id']})

