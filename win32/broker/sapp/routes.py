from sanic.response import json, text


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