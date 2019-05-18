from sanic import Sanic

from databases import Database

from environs import Env
from krx_dataserver.settings import Settings
from krx_dataserver.db import setup_database
from krx_dataserver.routes import setup_routes



app = Sanic(__name__)


def init():
    env = Env()
    env.read_env()

    app.config.from_object(Settings)

    setup_database(app)
    setup_routes(app)

    if app.config.DEBUG:
        for handler, (rule, router) in app.router.routes_names.items():
            print(rule, handler)

    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
    )
