import logging

from flask_socketio import Namespace, emit

logger = logging.getLogger(__name__)

class SocketEventHandlerNamepsace(Namespace):
    def on_connect(self):
        logger.info('Client connected to Socket.IO')

    def on_disconnect(self):
        logger.info('Client disconnected')

    def emit_scraper_update(self, scraper_id, state):
        self.emit(
            'scraper_update',
            {'scraper_id': scraper_id, 'state': state.value},
            namespace='/socket_io'
        )

socketio_events = SocketEventHandlerNamepsace('/socket_io')