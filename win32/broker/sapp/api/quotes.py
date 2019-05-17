from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

bp = Blueprint('bp')

@bp.route('/quotes')
async def index(request):
    return json({'get': 'list'})


class QuoteView(HTTPMethodView):

    def get(self, request, code):
        return json({'qv': f'get {code}'})

    def post(self, request, code):
        return json({'qv': 'post'})

    def delete(self, request, code):
        return json({'qv': 'delete'})


bp.add_route(QuoteView.as_view(), '/quotes/<code>')