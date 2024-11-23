from flask_socketio import SocketIO, emit

def init_socketio(socketio: SocketIO):
    """Set up WebSocket event handlers."""

    @socketio.on('connect')
    def handle_connect():
        print('Client connected to WebSocket')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected from WebSocket')

    @socketio.on('progress')
    def handle_progress(data):
        print(f"Progress event received: {data}")
        # You can emit progress or any other events here.
        emit('progress_update', {'progress': data['progress']})
        
