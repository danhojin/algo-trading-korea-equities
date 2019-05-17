from sanic.response import json, text
from sanic.views import HTTPMethodView

from broker.sapp.api import quotes


def setup_routes(app, q):
    @app.route('/hello')
    async def hello(request):
        return json({
            'hello': 'world'
        })

    @app.route('/codes/<code_id>')
    async def codes_handler(request, code_id):
        q.put(code_id)
        print(f's:{code_id}')
        return text(f'done: {code_id}')

    app.blueprint(quotes.bp, url_prefix='/api')

    for handler, (rule, router) in app.router.routes_names.items():
        print(rule)