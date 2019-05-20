from sanic.response import json
from sanic.exceptions import ServerError
from sanic import Blueprint
from sanic.views import HTTPMethodView

from dateutil.parser import parse

from krx_dataserver.models import (
    dailyprice,
)


bp_dailyprices = Blueprint('bp_dailyprice', url_prefix='/dailyprices')


@bp_dailyprices.route('/<asset>/<start>/<stop>')
async def get_dailyprices(request, asset, start, stop):
    try:
        start = parse(start).date()
        stop = parse(stop).date()
    except ValueError:
        raise ServerError('Date error', status_code=500)

    query = dailyprice.select() \
        .where(dailyprice.c.asset == asset) \
        .where(dailyprice.c.date >= start) \
        .where(dailyprice.c.date < stop) \
        .order_by(dailyprice.c.date.desc())

    rows = await request.app.db.fetch_all(query=query)

    return json({row['date']: row['close'] for row in rows})


class MarketDataDailyPriceView(HTTPMethodView):

    async def get(self, request, asset):
        query = dailyprice.select()
        row = await request.app.db.fetch_one(query=query)
        print(row['asset'])
        return json({'received': True, 'asset': asset})

    def post(self, request, asset):
        pass


def setup_routes(app):

    @app.route('/hello')
    def hello(request):
        return json({'hello': 'world'})

    app.add_route(
        MarketDataDailyPriceView.as_view(),
        '/marketdata/dailyprices/<asset>')

    app.blueprint(bp_dailyprices)
