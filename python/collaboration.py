from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request

socketio = SocketIO(cors_allowed_origins="*")

# In-memory store for documents: {doc_id: content}
documents = {}

def init_collaboration(app):
    socketio.init_app(app)

    @socketio.on('connect')
    def handle_connect():
        pass

    @socketio.on('join_document')
    def on_join(data):
        room = data.get('doc_id', 'default')
        join_room(room)
        # Send current document state
        content = documents.get(room, "")
        emit('document_state', {'content': content}, room=request.sid)

    @socketio.on('update_document')
    def on_update(data):
        room = data.get('doc_id', 'default')
        content = data.get('content', '')
        documents[room] = content
        # Broadcast to others in the room
        emit('document_updated', {'content': content}, room=room, include_self=False)

    return socketio
