from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

bp = Blueprint('bp')

@bp.route('/realtime')
async def get_watching_list(request):
    return json({'get': 'list'})

@bp.route('/realtime', methods=['POST'])
async def set_watching_list(request):
    # assets = request.json['assets'].split(';')
    print(request.json['assets'])
    print(request.json['assets'].split(';'))
    request.app.message_queue['realtime'].put(
        request.json['assets']
    )
    return json({'rq': request.json})