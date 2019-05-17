from sanic import Sanic
from databases import Database

from environs import Env
from broker.sapp.settings import Settings
from broker.sapp.routes import setup_routes


def setup_database(app):
    app.db = Database(app.config.DB_URL)

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await app.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.db.disconnect()


def sapp_create(q):
    app = Sanic(__name__)

    env = Env()
    env.read_env()
    app.config.from_object(Settings)

    setup_database(app)
    setup_routes(app, q)

    return app