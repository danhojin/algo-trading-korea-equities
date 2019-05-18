from sanic.response import json
from sanic.views import HTTPMethodView


class MarketDataDailyPriceView(HTTPMethodView):

    def get(self, request):
        pass

    def post(self, request):
        pass


def setup_routes(app):

    @app.route('/hello')
    def hello(request):
        return json({'hello': 'world'})

    app.add_route(
        MarketDataDailyPriceView.as_view(),
        '/marketdata/dailyprices')
