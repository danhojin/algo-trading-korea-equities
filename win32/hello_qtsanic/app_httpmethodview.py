from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text

app = Sanic(__name__)


class TestView(HTTPMethodView):

    def get(self, request, name):
        return text(f'get method {name}')

    def post(self, request, name):
        return text(f'post method {name}')

    def delete(self, request, name):
        return text(f'delete method {name}')


app.add_route(TestView.as_view(), '/tests/<name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)