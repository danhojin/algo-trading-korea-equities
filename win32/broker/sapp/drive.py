from sanic import Sanic

from environs import Env
from broker.sapp.settings import Settings
from broker.sapp.routes import setup_routes


def sapp_create(q):
    app = Sanic(__name__)

    env = Env()
    env.read_env()
    app.config.from_object(Settings)

    setup_routes(app, q)

    return app