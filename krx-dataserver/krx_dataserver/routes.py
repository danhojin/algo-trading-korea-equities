from sanic.response import json
from sanic.exceptions import ServerError
from sanic import Blueprint
from sanic.views import HTTPMethodView

from dateutil.parser import parse

from krx_dataserver.models import (
    asset,
    dailyprice,
)


bp_dailyprices = Blueprint('bp_dailyprice', url_prefix='/dailyprices')


@bp_dailyprices.route('/')
async def get_dailyprices_list(request):
    query = dailyprice.select() \
        .distinct(dailyprice.c.asset)
    scraped = await request.app.db.fetch_all(query=query)

    query = asset.select() \
        .where(asset.c.code.in_(s['asset'] for s in scraped))
    rows = await request.app.db.fetch_all(query=query)

    return json({row['code']:row['name'] for row in rows})


@bp_dailyprices.route('/<asset>/<start>/<stop>')
async def get_dailyprices(request, asset, start, stop):
    # need to check the existence of asset
    try:
        start = parse(start).date()
        stop = parse(stop).date()
    except ValueError:
        # 416 Range Not Satisfiable
        raise ServerError('Date error', status_code=416)

    query = dailyprice.select() \
        .where(dailyprice.c.asset == asset) \
        .where(dailyprice.c.date >= start) \
        .where(dailyprice.c.date < stop) \
        .order_by(dailyprice.c.date)

    rows = await request.app.db.fetch_all(query=query)

    return json({row['date']: (
        row['open'],
        row['high'],
        row['low'],
        row['close'],
        row['volume'],
    ) for row in rows})


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
