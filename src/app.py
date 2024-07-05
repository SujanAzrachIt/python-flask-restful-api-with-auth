import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")


def __db_setup(_app, _app_setting, db_pg: bool = False):
    if db_pg:
        _app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Simple#123@localhost:5432/app_base"
        _app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 10, 'max_overflow': 20}
    else:
        _app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{_app_setting.data_dir}/data.db?timeout=60'
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['SQLALCHEMY_ECHO'] = False
    return _app


def create_app(app_setting) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if app_setting.prod else 'development')
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app_setting = app_setting.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors.init_app(app)
    db.init_app(__db_setup(app, app_setting, True))
    socketio.init_app(app)

    def setup(self):
        gunicorn_logger = logging.getLogger('gunicorn.error')
        self.logger.handlers = gunicorn_logger.handlers
        self.logger.setLevel(gunicorn_logger.level)
        self.logger.info(self.config['SQLALCHEMY_DATABASE_URI'])

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        # cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def register_router(_app) -> Flask:
        from src.routes import bp_qrcode, bp_org, bp_role, bp_user, bp_auth
        _app.register_blueprint(bp_org)
        _app.register_blueprint(bp_qrcode)
        _app.register_blueprint(bp_role)
        _app.register_blueprint(bp_user)
        _app.register_blueprint(bp_auth)

        from src.utils.socketio_events import socketio_events
        socketio.on_namespace(socketio_events)

        return _app

    setup(app)
    return register_router(app)
